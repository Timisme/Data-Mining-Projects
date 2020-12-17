import csv
import re
from transformers import BertTokenizer, BertModel
import torch
import torch.nn as nn
from torchcrf import CRF
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class test_output():
	def __init__(self, data, model, tokenizer, batch_size):

		self.model = model
		self.tokenizer = tokenizer
		self.batch_size = batch_size
		self.data_list = []
		self.word_id = []
		self.word_article_id = [] 
		article_id = 0
		word_id = 0
		data_list_tmp = []
		article_id_tmp = []
		word_id_tmp = []
		
		for row in data:
			
			data_tuple = tuple()
			if row == '\n':
				
				article_id += 1 
				word_id = 0
				self.word_id.append(word_id)
				self.word_article_id.append(article_id_tmp)
				self.data_list.append(data_list_tmp)
				data_list_tmp = []
				article_id_tmp = []
				word_id_tmp = []

			else:
				
				row = row.strip('\n').split(' ')

				if row[0] in ['。', '？','！','，','～','：',',','‧']:
					
					self.word_id.append(word_id_tmp)
					self.word_article_id.append(article_id_tmp)
					self.data_list.append(data_list_tmp)
					data_list_tmp = []
					article_id_tmp = []
					word_id_tmp = []
					
				elif row[0] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
					  
					data_tuple = (row[0].lower(), article_id, word_id)
					data_list_tmp.append(data_tuple)
					article_id_tmp.append(article_id)
					word_id_tmp.append(word_id)

				elif row[0] not in ['摁','嗯','啦','喔','欸','啊','齁','嘿','…','...','、']:
					
					data_tuple = (row[0], article_id, word_id)
					data_list_tmp.append(data_tuple)
					article_id_tmp.append(article_id)
					word_id_tmp.append(word_id)
					
				word_id += 1
				
		if len(data_list_tmp) != 0:
			self.data_list.append(data_list_tmp)
			self.word_id.append(word_id_tmp)
			self.word_article_id.append(article_id_tmp)
			
	def raw_output(self):
		return self.data_list, self.word_id, self.word_article_id

	def get_stcs(self):
		
		all_stcs = list()
		all_article_ids = list()
		all_word_ids = list()

		for stc_list in self.data_list:

			txt_len = len(stc_list) #(文章數，每個文章對應的總字數) (word, label)
			stc = str() #存字數= max_stc_len的字串
			article_ids = []
			word_ids = []
			

			for idx, (word,article_id, word_id) in enumerate(stc_list):

				stc += word
				article_ids.append(article_id)
				word_ids.append(word_id)

			all_stcs.append(stc)
			all_article_ids.append(article_ids)
			all_word_ids.append(word_ids)

		assert len(all_stcs) > 0, 'all stcs len = 0' 

		all_stcs_clean = []
		all_article_ids_clean = []
		all_word_ids_clean = []
		idx = 0
		
		for stc, article_id, word_id in zip(all_stcs, all_article_ids, all_word_ids):
			stc_clean = re.sub(r'(醫師)|(個管師)|(民眾)|(家屬)|(護理師)', '', stc)
			# print(stc, stc_clean, label)
			if len(stc_clean) > 1:  
			# print(stc_clean, stc)
				all_stcs_clean.append(stc)
				all_article_ids_clean.append(article_id)
				all_word_ids_clean.append(word_id)

			# 這一步就先把label 做 0 padding
			
		max_length = len(max(all_stcs_clean, key=len))
		assert max_length > 0, 'max length less than 1'

		print('sentences總數: {}'.format(len(all_stcs_clean)))
			
		# return all_stcs_clean, all_article_ids_clean, all_word_ids_clean

		self.clean_stcs, self.clean_article_id, self.clean_word_id = [], [] ,[]

		for stc, article_id, word_id in zip(stcs, article_ids, word_ids):
		#print(stc, article_id, word_id)
			if stc not in ['沒有','也沒有','哪個','那個','算了','不用','有','有有有','有嗎','一點點', '謝謝','不會','不好意思','對不對','好不好','要嗎','還好']:
				self.clean_stcs.append(stc)
				self.clean_article_id.append(article_id)
				self.clean_word_id.append(word_id)
		return self.clean_stcs, self.clean_article_id, self.clean_word_id

	def encoding(self):
		
		max_len = max(len(txt) for txt in self.clean_stcs)

		encoding = self.tokenizer.batch_encode_plus(self.clean_stcs, 
			padding=True,
			add_special_tokens=False,
			return_attention_mask= True,
			return_token_type_ids= False,
			#  is_split_into_words=True,
			return_tensors='pt')

		# batch_size= 32
		pred_labels = []

		for idx in range(int((len(clean_stcs)/self.batch_size))):
			input= encoding['input_ids'][idx*self.batch_size:(idx+1)*self.batch_size].to(device)
			mask = encoding['attention_mask'][idx*self.batch_size:(idx+1)*self.batch_size].to(device)
			tags= torch.zeros((input.size(0),input.size(1)), dtype=torch.long).to(device)
			_, preds = model(input, mask, tags)
			for pred in preds:
				pred_labels.append(pred)

		idx = int((len(clean_stcs)/self.batch_size))
		input= encoding['input_ids'][idx*self.batch_size:].to(device)
		mask = encoding['attention_mask'][idx*self.batch_size:].to(device)
		tags= torch.zeros((input.size(0),input.size(1)), dtype=torch.long).to(device)
		_, preds = model(input, mask, tags)
		for pred in preds:
			pred_labels.append(pred)

		tag2id = {'[PAD]': 0, 'B-ID': 1, 'B-clinical_event': 2, 'B-contact': 3, 'B-education': 4, 'B-family': 5, 'B-location': 6, 'B-med_exam': 7, 'B-money': 8, 'B-name': 9, 'B-organization': 10, 'B-profession': 11, 'B-time': 12, 'I-ID': 13, 'I-clinical_event': 14, 'I-contact': 15, 'I-education': 16, 'I-family': 17, 'I-location': 18, 'I-med_exam': 19, 'I-money': 20, 'I-name': 21, 'I-organization': 22, 'I-profession': 23, 'I-time': 24, 'O': 25}
		id2tag ={v:k for k, v in tag2id.items()}

		self.pred_labels_tag = []
		for label in pred_labels:
			stc_label = [id2tag[id] for id in label]
			self.pred_labels_tag.append(stc_label)

		return self.pred_labels_tag

	def pred_out_tsv(self):

		entity_text = []

		for stc, labels, article_id, word_id in zip(clean_stcs, pred_labels_tag, clean_article_id, clean_word_id):

			entity = str()

			start_pos = 0
			end_pos = 0
			article = 0

			entity_type = str()


			for idx, label in enumerate(labels):
				if bool(re.match(r'B-', label)):
					entity += list(stc)[idx]
					start_pos = word_id[idx]
					article = article_id[idx]
					entity_type = label.split('B-')[1]

				elif bool(re.match(r'I-', label)):
					entity += list(stc)[idx]
					end_pos= word_id[idx]
					try:
						if (labels[idx+1] == 'O') & (entity_type!=''):
							entity_text.append((article, start_pos, end_pos, entity, entity_type))

							entity = str()
							start_pos = 0
							end_pos = 0
							article = 0
							entity_type = str()
					except:
						pass
		with open('test_output.tsv', 'w', encoding='utf-8',newline='\n') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(['article_id','start_position', 'end_position', 'entity_text', 'entity_type'])
			for (article, start_pos, end_pos, entity, entity_type) in entity_text:
				writer.writerow([str(article), str(start_pos), str(end_pos), str(entity), str(entity_type)])

		return entity_text
	

	def pred_out_tsv(self):

		clean_stcs, clean_article_id, clean_word_id = self.get_stcs()
		pred_labels_tag = self.encoding()

		entity_text = []

		for stc, labels, article_id, word_id in zip(clean_stcs, pred_labels_tag, clean_article_id, clean_word_id):

			entity = str()

			start_pos = 0
			end_pos = 0
			article = 0

			entity_type = str()


			for idx, label in enumerate(labels):
				if bool(re.match(r'B-', label)):
					entity += list(stc)[idx]
					start_pos = word_id[idx]
					article = article_id[idx]
					entity_type = label.split('B-')[1]

				elif bool(re.match(r'I-', label)):
					entity += list(stc)[idx]
					end_pos= word_id[idx]
					try:
						if (labels[idx+1] == 'O') & (entity_type!=''):
							entity_text.append((article, start_pos, end_pos, entity, entity_type))

							entity = str()
							start_pos = 0
							end_pos = 0
							article = 0
							entity_type = str()
					except:
						pass
		with open('test_output.tsv', 'w', encoding='utf-8',newline='\n') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(['article_id','start_position', 'end_position', 'entity_text', 'entity_type'])
			for (article, start_pos, end_pos, entity, entity_type) in entity_text:
				writer.writerow([str(article), str(start_pos), str(end_pos), str(entity), str(entity_type)])

		return entity_text

	
print(['a','b','c','d'][2:4])