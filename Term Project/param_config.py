import numpy as np
import torch 
import torch.nn as nn 

class config(nn.Module):
	def __init__(self, num_epochs, lr, batch_size, device):
		super(config, self).__init__()
		self.num_epochs = 20
		self.lr = 1e-3
		self.batch_size = 20
		self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

