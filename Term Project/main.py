from model import Bert_BiLstm_Crf
from dataset import bert_stc_dataset
from txt_preprocess import preprocess
from txt_preprocess2 import preprocess2
from transformers import BertModel, BertTokenizer
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

file_path = 'data/train_input.data'

with open(file_path, 'r', encoding='utf-8') as f:
	data=f.readlines()#.encode('utf-8').decode('utf-8-sig')

preprocessor = preprocess2(data)

stcs, labels = preprocessor.get_stcs_label2ids()
tag2id_dict = preprocessor.tag2id(labels)
n_tags = len(tag2id_dict)
print('tags數: {}'.format(n_tags))
# stc_labels_ids = preprocessor.label_to_ids(tag2id_dict, labels)

pretrained_model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(pretrained_model_name)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# model = Bert_BiLstm_Crf(n_tags= n_tags, 
# 	pretrained_model_name= pretrained_model_name, 
# 	tokenizer= tokenizer).to(device)

train_dataset = bert_stc_dataset(stcs= stcs, labels= labels, tokenizer= tokenizer, max_length= 100)

train_Dataloader = DataLoader(train_dataset, batch_size= 10, shuffle= True)

# optimizer = torch.optim.Adam(model.parameters(), lr = config.lr)
# model = BertModel.from_pretrained(pretrained_model_name).to(device)

def train(train_Dataloader, num_epochs):

	model = Bert_BiLstm_Crf(n_tags= n_tags, 
	pretrained_model_name= pretrained_model_name, 
	tokenizer= tokenizer).to(device) 

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)

	train_loss = {}
	test_loss = {}

	for epoch in range(num_epochs):

		total_loss= 0
		total_iter = 0 

		model.train()

		for idx, batch in enumerate(train_Dataloader):

			input_ids = batch['input_ids'].to(device)
			attention_masks = batch['attention_mask'].to(device)
			labels = batch['label'].to(device)

			print('input size for bert: {}'.format(input_ids.size()))

			optimizer.zero_grad()

			_, out = model(input_ids, attention_masks)
			# print('model output seq:\n{}'.format(out))
			# print('truth label:\n{}'.format(labels))

			loss = model.neg_log_likelihood(input_ids, attention_masks, labels)
			loss.backward()
			optimizer.step()

			total_loss += loss
			total_iter += 1

			break

		print('epoch {}/{} | loss {}'.format(epoch, num_epochs, (total_loss/total_iter)))
		break

train(train_Dataloader=train_Dataloader, num_epochs= 1)

