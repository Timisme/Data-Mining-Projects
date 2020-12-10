import torch 
import torch.nn as nn
from transformers import BertModel, BertTokenizer

class Bert_BiLstm_Crf(nn.Module):

	def __init__(self, n_tags, tokenizer, pretrained_model_name, hidden_dim=768):
		super(Bert_BiLstm_Crf, self).__init__()
		self.n_tags = n_tags
		self.lstm =  nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=hidden_dim//2, batch_first=True)
		self.transitions = nn.Parameter(torch.randn(
		    self.n_tags, self.n_tags
		))
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained(pretrained_model_name)
		# self.bert.eval()  # 知用来取bert embedding

		self.start_label_id = 25
		self.end_label_id = 26

		self.transitions.data[self.start_label_id, :] = -10000
		self.transitions.data[:, self.end_label_id] = -10000
		self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
		self.transitions.to(self.device)

	def init_hidden(self):
	# Two tensors to hold hidden states, one for each
	# LSTM direction with dimensions of (num_layers, 
	# minibatch, hidden_dim)
	# Minibatch small because small dataset below
		return (torch.randn(2, 1, self.hidden_dim // 2).to(device),
		torch.randn(2, 1, self.hidden_dim // 2).to(device))

	def _forward_alg(self, feats):
	
		# this also called alpha-recursion or forward recursion, to calculate log_prob of all barX 
		# 針對一個序列(句子) 計算所有路徑的總分數 = log sum exp of score(x, y)

		# T = self.max_seq_length
		max_seq_len = feats.shape[1]  
		batch_size = feats.shape[0]

		# alpha_recursion,forward, alpha(zt)=p(zt,bar_x_1:t)
		log_alpha = torch.Tensor(batch_size, 1, self.n_tags).fill_(-10000.).to(self.device)  #[batch_size, 1, n_tags]
		# normal_alpha_0 : alpha[0]=Ot[0]*self.PIs
		# self.start_label has all of the score. it is log,0 is p=1
		log_alpha[:, 0, self.start_label_id] = 0

		# feats: sentances -> word embedding -> lstm -> MLP -> feats
		# feats is the probability of emission, feat.shape=(1,tag_size)
		for t in range(1, max_seq_len):
		    log_alpha = (log_sum_exp_batch(self.transitions + log_alpha, axis=-1) + feats[:, t]).unsqueeze(1)

		# log_prob of all barX
		log_prob_all_barX = log_sum_exp_batch(log_alpha)
		return log_prob_all_barX

	def _score_sentence(self, feats, label_ids):
		T = feats.shape[1]
		batch_size = feats.shape[0]

		batch_transitions = self.transitions.expand(batch_size,self.n_tags, self.n_tags)
		batch_transitions = batch_transitions.flatten(1)

		score = torch.zeros((feats.shape[0],1)).to(self.device)
		# the 0th node is start_label->start_word,the probability of them=1. so t begin with 1.
		for t in range(1, T):
		    score = score + \
		        batch_transitions.gather(-1, (label_ids[:, t]*self.n_tags+label_ids[:, t-1]).view(-1,1)) \
		            + feats[:, t].gather(-1, label_ids[:, t].view(-1,1)).view(-1,1)
		return score

	def _viterbi_decode(self, feats):
		'''
		Max-Product Algorithm or viterbi algorithm, argmax(p(z_0:t|x_0:t))
		'''

		# T = self.max_seq_length
		T = feats.shape[1]
		batch_size = feats.shape[0]

		# batch_transitions=self.transitions.expand(batch_size,self.n_tags,self.tagset_size)

		log_delta = torch.Tensor(batch_size, 1, self.n_tags).fill_(-10000.).to(self.device)
		# log_delta[:, 0, self.start_label_id] = 0.

		# psi is for the vaule of the last latent that make P(this_latent) maximum.
		psi = torch.zeros((batch_size, T, self.n_tags), dtype=torch.long)  # psi[0]=0000 useless
		for t in range(1, T):
		    # delta[t][k]=max_z1:t-1( p(x1,x2,...,xt,z1,z2,...,zt-1,zt=k|theta) )
		    # delta[t] is the max prob of the path from  z_t-1 to z_t[k]
			log_delta, psi[:, t] = torch.max(self.transitions + log_delta, -1)
		    # psi[t][k]=argmax_z1:t-1( p(x1,x2,...,xt,z1,z2,...,zt-1,zt=k|theta) )
		    # psi[t][k] is the path choosed from z_t-1 to z_t[k],the value is the z_state(is k) index of z_t-1
			log_delta = (log_delta + feats[:, t]).unsqueeze(1)

		# trace back
		path = torch.zeros((batch_size, T), dtype=torch.long)

		# max p(z1:t,all_x|theta)
		max_logLL_allz_allx, path[:, -1] = torch.max(log_delta.squeeze(), -1)

		for t in range(T-2, -1, -1):
			# choose the state of z_t according the state choosed of z_t+1.
			path[:, t] = psi[:, t+1].gather(-1,path[:, t+1].view(-1,1)).squeeze()

		return max_logLL_allz_allx, path


	def _bert_enc(self, input_ids, attention_mask):
	    # x: [batchsize, sent_len]
	    # enc: [batch_size, sent_len, 768]
		with torch.no_grad():
			encoded_layer, _  = self.bert(input_ids, attention_mask)
			# enc = encoded_layer[-1]
			print('out encoded size from bert: {}'.format(encoded_layer.size()))
		return encoded_layer

	def _get_lstm_features(self, input_ids, attention_mask):
	    """sentence is the ids"""
	    # bert embeds: [batch_size, max_seq_len, 768]
	    # lstm_feats: [batch_size, max_seq_len, n_tags]

	    # self.hidden = self.init_hidden()
	    embeds = self._bert_enc(input_ids, attention_mask)
	    enc, _ = self.lstm(embeds)
	    lstm_feats = self.fc(enc)
	    return lstm_feats 

	def forward(self, input_ids, attention_mask):  # dont confuse this with _forward_alg above.
	    # Get the emission scores from the BiLSTM
		lstm_feats = self._get_lstm_features(input_ids, attention_mask) 

	    # Find the best path, given the features.
		score, tag_seq = self._viterbi_decode(lstm_feats)
		return score, tag_seq

	def neg_log_likelihood(self, input_ids, attention_mask, tags):
	    feats = self._get_lstm_features(input_ids, attention_mask)  #[batch_size, max_len, n_tags]
	    forward_score = self._forward_alg(feats)
	    gold_score = self._score_sentence(feats, tags)
	    return torch.mean(forward_score - gold_score)
