from model import Bert_BiLstm_Crf
from dataset import bert_stc_dataset
from txt_preprocess2 import preprocess2
from train import train
from transformers import BertModel, BertTokenizer
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

file_path = 'data/train_input.data'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('{} is being used'.format(device))

# ---------------前處理---------------
with open(file_path, 'r', encoding='utf-8') as f:
	data=f.readlines()#.encode('utf-8').decode('utf-8-sig')

preprocessor = preprocess2(data)

stcs, labels = preprocessor.get_stcs_label2ids()
tag2id_dict = preprocessor.tag2id(labels)
n_tags = len(tag2id_dict)
print('tags數: {}'.format(n_tags))

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

# ---------------模型---------------
model = Bert_BiLstm_Crf(n_tags= n_tags).to(device)

train_dataset = bert_stc_dataset(stcs= stcs, labels= labels, tokenizer= tokenizer, max_length= 300)
train_dataloader = DataLoader(train_dataset, batch_size= 10, shuffle= True)

optimizer = torch.optim.Adam(model.parameters(), lr = 1e-4)

# ---------------訓練---------------
# train_model = train(model= model, optimizer= optimizer, train_loader= train_dataloader, test_loader= 0, num_epochs= 5, device= device)



