import torch 
import torch.nn as nn 
from torchcrf import CRF
from transformers import BertModel
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class model_crf(nn.Module):
	def __init__(self, n_tags, hidden_dim=256, train= True):
		super(model_crf, self).__init__()
		self.n_tags = n_tags
		self.lstm =  nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=hidden_dim//2, batch_first=True)		
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained('bert-base-chinese')
		self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
		self.CRF = CRF(n_tags, batch_first= True)

	def init_hidden(self, batch_size):
		return (torch.randn(2*2, batch_size, self.hidden_dim // 2).to(self.device),
				torch.randn(2*2, batch_size, self.hidden_dim // 2).to(self.device))

	def forward(self, input_ids, attention_mask, tags= False):

		# bert out : [batch, seq, 768]
		batch_size = input_ids.size(0)
		bert_output, _  = self.bert(input_ids.long(), attention_mask)
		
		seq_len = torch.sum(attention_mask, dim= 1)
		print(seq_len)
		pack_input = pack_padded_sequence(input= bert_output, lengths= seq_len, batch_first= True, enforce_sorted= False)
		packed_lstm_out, _ = self.lstm(pack_input,self.init_hidden(batch_size= batch_size))
		lstm_enc, _=  pad_packed_sequence(packed_lstm_out, batch_first=True, padding_value=0)
		print(lstm_enc.size())
		lstm_feats = self.fc(lstm_enc)
		# lstm_feats[:,:,-1] = lstm_feats[:,:,-1]*0.001
		# loss = -self.CRF(lstm_feats, tags, attention_mask.bool(), reduction= 'token_mean')
		# pred_seqs = self.CRF.decode(emissions= lstm_feats, mask= attention_mask.bool())

		# return loss, pred_seqs


if __name__ == '__main__':

	from torchsummary import summary
	device= 'cuda'

	mask = torch.tensor([[1,1,1],[1,1,0]], dtype= torch.bool)

	for seq_mask in mask :
		print(seq_mask)

	# seq_len =map(lambda x :x.count(True))
	print(torch.sum(mask, dim= 1))

	# print(seq_len)

	# model = model_crf(n_tags= 25).to(device)

	# model(torch.tensor([[24,24,23],[24,24,15]], dtype=torch.long).to(device),
	# 	torch.tensor([[1,1,1],[1,1,0]], dtype= torch.bool).to(device))

	print([' '.join(list('好朋友hisdsdsdsqoji'))])

	print(int(5/3))

	# print(pred)

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

