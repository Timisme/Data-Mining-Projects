import torch 
import torch.nn as nn 
from torchcrf import CRF
from transformers import BertModel

class model_crf(nn.Module):
	def __init__(self, n_tags, hidden_dim=768, train= True):
		super(model_crf, self).__init__()
		self.n_tags = n_tags
		self.lstm =  nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=hidden_dim//2, batch_first=True)		
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained('bert-base-chinese')
		if train:
			self.bert.train()
			self.lstm.train()

		# self.bert.eval()  # 知用来取bert embedding
		self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
		self.CRF = CRF(n_tags, batch_first= True)

	def init_hidden(self):
		return (torch.randn(4, 2, self.hidden_dim // 2).to(self.device),
				torch.randn(4, 2, self.hidden_dim // 2).to(self.device))

	def _bert_enc(self, input_ids, attention_mask):
	    # x: [batchsize, sent_len]
	    # enc: [batch_size, sent_len, 768]
		# with torch.no_grad():
		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
			# enc = encoded_layer[-1]
			# print('out encoded size from bert: {}'.format(encoded_layer.size()))
		return encoded_layer

	def _get_lstm_features(self, input_ids, attention_mask):
	    """sentence is the ids"""
	    # bert embeds: [batch_size, max_seq_len, 768]
	    # lstm_feats: [batch_size, max_seq_len, n_tags]

	    self.hidden = self.init_hidden()
	    embeds = self._bert_enc(input_ids, attention_mask)
	    enc, _ = self.lstm(embeds)
	    lstm_feats = self.fc(enc)

	    # data imbalance 處理

	    # lstm_feats[:,:,1:-1] = lstm_feats[:,:,1:-1]*0.001 

	    # print(lstm_feats)
	    return lstm_feats 

	def neg_log_likelihood(self, input_ids, attention_mask, tags):

		# feats : [batchsize, seq_len, n_tags]
		# tags : [batchsize, n_tags]
		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
		self.hidden = self.init_hidden()
		enc, _ = self.lstm(encoded_layer, self.hidden)
		lstm_feats = self.fc(enc)
		lstm_feats[:,:,1:-1] = lstm_feats[:,:,1:-1]*0.001

		loss = -self.CRF(lstm_feats, tags, attention_mask.bool())

		return loss 

	def forward(self, input_ids, attention_mask):

		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
		self.hidden = self.init_hidden()
		enc, _ = self.lstm(encoded_layer, self.hidden)
		lstm_feats = self.fc(enc)
		lstm_feats[:,:,1:-1] = lstm_feats[:,:,1:-1]*0.001

		return self.CRF.decode(emissions= lstm_feats, mask= attention_mask.bool())

if __name__ == '__main__':

	from torchsummary import summary
	device= 'cuda'

	model = model_crf(n_tags= 25).to(device)

	pred = model(torch.tensor([[24,24,23],[24,24,15]], dtype=torch.long).to(device),
		torch.tensor([[1,1,1],[1,1,0]], dtype= torch.bool).to(device))

	print(pred)

	# print(summary(model, [(128,200),(128,200)]))
	# print(model)
	# labels = torch.tensor([[24,24,23],[24,24,15]], dtype=torch.long).numpy()
	# masks = torch.tensor([[1,1,1],[1,1,0]], dtype= torch.long).numpy()
	# # masked_list = (labels*mask).numpy()

	# labels_nopad = []
	# for label , seq_mask in zip(labels, masks):

	# 	seq = [tag for tag, mask in zip(label, seq_mask) if mask == 1]
	# 	labels_nopad.append(seq)

	# print(labels_nopad)

	------------


class model_crf(nn.Module):
	def __init__(self, n_tags, hidden_dim=768, batchsize= 64):
		super(model_crf, self).__init__()
		self.n_tags = n_tags
		self.lstm =  nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=hidden_dim//2, dropout= 0.1, batch_first=True)		
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained('bert-base-chinese')
		# self.bert.eval()  # 知用来取bert embedding
		self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
		self.CRF = CRF(n_tags, batch_first= True)
		self.hidden = self.init_hidden(batchsize)

	def init_hidden(self, batchsize):
		return (torch.randn(2*2, batchsize, self.hidden_dim // 2).to(self.device),
				torch.randn(2*2, batchsize, self.hidden_dim // 2).to(self.device))

	def _bert_enc(self, input_ids, attention_mask):
	    # x: [batchsize, sent_len]
	    # enc: [batch_size, sent_len, 768]
		# with torch.no_grad():
		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
			# enc = encoded_layer[-1]
			# print('out encoded size from bert: {}'.format(encoded_layer.size()))
		return encoded_layer

	def _get_lstm_features(self, input_ids, attention_mask):
	    """sentence is the ids"""
	    # bert embeds: [batch_size, max_seq_len, 768]
	    # lstm_feats: [batch_size, max_seq_len, n_tags]

	    # self.hidden = self.init_hidden()
	    embeds = self._bert_enc(input_ids, attention_mask)
	    enc, _ = self.lstm(embeds)
	    lstm_feats = self.fc(enc)

	    # data imbalance 處理

	    # lstm_feats[:,:,1:-1] = lstm_feats[:,:,1:-1]*0.001 

	    # print(lstm_feats)
	    return lstm_feats 

	def neg_log_likelihood(self, input_ids, attention_mask, tags):

		# feats : [batchsize, seq_len, n_tags]
		# tags : [batchsize, n_tags]
		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
		enc, _ = self.lstm(encoded_layer, self.hidden)
		lstm_feats = self.fc(enc)
		# lstm_feats[:,:,-1] = lstm_feats[:,:,-1]*0.001

		loss = -self.CRF(lstm_feats, tags, attention_mask.bool(), reduction= 'mean')

		return loss 

	def forward(self, input_ids, attention_mask):

		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
		enc, _ = self.lstm(encoded_layer,self.hidden)
		lstm_feats = self.fc(enc)
		# lstm_feats[:,:,-1] = lstm_feats[:,:,-1]*0.001

		return self.CRF.decode(emissions= lstm_feats, mask= attention_mask.bool())

class model_crf(nn.Module):
	def __init__(self, n_tags, hidden_dim=768, batchsize= 64):
		super(model_crf, self).__init__()
		self.n_tags = n_tags
		self.lstm =  nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=hidden_dim//2, dropout= 0.1, batch_first=True)		
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained('bert-base-chinese')
		# self.bert.eval()  # 知用来取bert embedding
		self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
		self.CRF = CRF(n_tags, batch_first= True)
		self.hidden = self.init_hidden(batchsize)

	def init_hidden(self, batchsize):
		return (torch.randn(2*2, batchsize, self.hidden_dim // 2).to(self.device),
				torch.randn(2*2, batchsize, self.hidden_dim // 2).to(self.device))

	def neg_log_likelihood(self, input_ids, attention_mask, tags):

		# feats : [batchsize, seq_len, n_tags]
		# tags : [batchsize, n_tags]
		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
		enc, _ = self.lstm(encoded_layer, self.hidden)
		lstm_feats = self.fc(enc)
		# lstm_feats[:,:,-1] = lstm_feats[:,:,-1]*0.001

		loss = -self.CRF(lstm_feats, tags, attention_mask.bool(), reduction= 'mean')

		return loss 

	def forward(self, input_ids, attention_mask, tags):

		encoded_layer, _  = self.bert(input_ids.long(), attention_mask)
		enc, _ = self.lstm(encoded_layer,self.hidden)
		lstm_feats = self.fc(enc)
		# lstm_feats[:,:,-1] = lstm_feats[:,:,-1]*0.001
		loss = -self.CRF(lstm_feats, tags, attention_mask.bool(), reduction= 'token_mean')
		pred_seqs = self.CRF.decode(emissions= lstm_feats, mask= attention_mask.bool())
		return loss, pred_seqs