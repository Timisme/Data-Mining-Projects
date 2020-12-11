# from model import Bert_BiLstm_Crf
from model2 import model_crf
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

stcs, labels = preprocess2(data= data).get_stcs_label2ids()
stcs, raw_labels = preprocess2(data= data).get_stc_label()
tag2id_dict = preprocess2(data= data).tag2id(raw_labels)
n_tags = len(tag2id_dict)
print('n_tags', n_tags)
print(tag2id_dict)

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
max_length = max([len(txt) for txt in stcs])

# ---------------模型---------------
model = model_crf(n_tags= n_tags).to(device)

train_dataset = bert_stc_dataset(stcs= stcs, labels= labels, tokenizer= tokenizer, max_length= 300)
train_dataloader = DataLoader(train_dataset, batch_size= 10, shuffle= True)

optimizer = torch.optim.Adam(model.parameters(), lr = 1e-4)

# ---------------訓練---------------
train_model = train(model= model, optimizer= optimizer, train_loader= train_dataloader, test_loader= 0, num_epochs= 5, device= device)



