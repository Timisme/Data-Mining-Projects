import torch.nn as nn
import torch
from transformers import BertModel, BertTokenizer
from torch.nn.utils.rnn import pack_padded_sequence
# input for LSTM if batch_first set True = (Batchsize, seq_len, features)

class BiLstm(nn.Module):
	def __init__(self, input_size, hidden_size, num_layers, num_classes):
		super(BiLstm, self).__init__()
		self.hidden_size = hidden_size
		self.num_layers = num_layers
		self.lstm = nn.lstm(input_size, hidden_size, num_layers, batch_first= True, bidirectional= True)
		self.fc = nn.Linear(hidden_size*2, num_classes)

	def forward(self, x):
		h0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size)
		c0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size)

		out, _ = self.lstm(x, (h0, c0))
		out = self.fc(out[:,-1,:]) # (batchsize, no seq_len, hidden_size)

		return out

if __name__ == '__main__':

# 	stc = '我是吳淫昆'
# 	tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
# 	# print(tokenizer(stc))
# 	token_dict = tokenizer.encode_plus(
#             stc,
# #             truncation= True,
#             max_length= 10,
#             padding = 'max_length',
#             add_special_tokens=True,
# #             pad_to_multiple_of=True,
#             return_attention_mask= True,
#             return_token_type_ids= False,
#             return_tensors='pt')
# 	print(token_dict['input_ids'])

# 	# model = BertModel.from_pretrained('bert-base-chinese')
# 	# input_ids, attention_mask = token_dict['input_ids'], token_dict['attention_mask']
# 	# features, out = model(input_ids, attention_mask)
# 	# print(features.size())
# 	# print(features[0, -1, :])

# 	labels = torch.tensor([[24],[24],[0]], dtype= torch.long)
# 	gts = torch.tensor([[24],[19],[10]], dtype= torch.long)

# 	loss = nn.CrossEntropyLoss(labels, gts)

# 	print(loss)

	if __name__ == '__main__':

		# X = torch.randint(0, 2, size= (10, 5, 256))
		# print(X)
		# mask = X.tolist().map(lambda x: len(x))
		# print(mask)

		# packed_X = pack_padded_sequence(input= X, lengths= seq_len, batch_first= True, enforce_sorted= False)
		# lstm = nn.LSTM(input_size= 256, hidden_size= 128)

		# out, _ = lstm(input=X, batch_first= True)

		# print(out)

		x = torch.randint(1, 5, size= (10,20,25), dtype=torch.float)
		y = torch.zeros(size= (10, 30, 25), dtype= torch.float)

		print(torch.cat((x,y), dim= 1))
		print('ABC'.split())
		# print('A' in ['ABC'.split('')])




