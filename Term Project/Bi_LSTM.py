import torch.nn as nn
import torch

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