import torch 
import torch.nn as nn 
from torchcrf import CRF
from transformers import BertModel

class model_crf(nn.Module):
	def __init__(self, n_tags, hidden_dim=768, bert_train= True):
		super(model_crf, self).__init__()
		self.n_tags = n_tags
		self.lstm =  nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=hidden_dim//2, batch_first=True)
		# self.transitions = nn.Parameter(torch.randn(
		#     self.n_tags, self.n_tags))
		
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained('bert-base-chinese')
		self.bert_train = bert_train
		# self.bert.eval()  # 知用来取bert embedding

		# self.start_label_id = 25
		# self.end_label_id = 26

		# self.transitions.data[self.start_label_id, :] = -10000
		# self.transitions.data[:, self.end_label_id] = -10000
		self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
		# self.transitions.to(self.device)
		self.CRF = CRF(n_tags, batch_first= True)

	def init_hidden(self):
		return (torch.randn(2, 1, self.hidden_dim // 2),
				torch.randn(2, 1, self.hidden_dim // 2))

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
	    return lstm_feats 

	def neg_log_likelihood(self, input_ids, attention_mask, tags):

		# feats : [batchsize, seq_len, n_tags]
		# tags : [batchsize, n_tags]
		lstm_feats = self._get_lstm_features(input_ids= input_ids, attention_mask= attention_mask)
		
		loss = -self.CRF(lstm_feats, tags, attention_mask.bool())

		return loss 

	def forward(self, input_ids, attention_mask):

		lstm_feats= self._get_lstm_features(input_ids= input_ids, attention_mask= attention_mask)

		return self.CRF.decode(emissions= lstm_feats, mask= attention_mask.bool())

if __name__ == '__main__':

	from torchsummary import summary
	device= 'cuda'

	model = model_crf(n_tags= 25).to(device)

	pred = model(torch.tensor([[24,24,23],[24,24,15]], dtype=torch.long).to(device),
		torch.tensor([[1,1,1],[1,1,0]], dtype= torch.bool).to(device))

	print(pred)

	# print(summary(model, [(128,200),(128,200)]))
	# labels = torch.tensor([[24,24,23],[24,24,15]], dtype=torch.long).numpy()
	# masks = torch.tensor([[1,1,1],[1,1,0]], dtype= torch.long).numpy()
	# # masked_list = (labels*mask).numpy()

	# labels_nopad = []
	# for label , seq_mask in zip(labels, masks):

	# 	seq = [tag for tag, mask in zip(label, seq_mask) if mask == 1]
	# 	labels_nopad.append(seq)

	# print(labels_nopad)

