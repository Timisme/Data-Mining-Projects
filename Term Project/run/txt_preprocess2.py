import re

class preprocess2():
	def __init__(self, data):
		self.data = data
		self.article_id_list = list()
		self.data_list= list()
		data_list_tmp = list()
		idx = 0

		for row in data:
			data_tuple = tuple()
			if row == '\n':
				self.article_id_list.append(idx)
				idx+=1
				# data_list_tmp.append(('[SEP]','[SEP]'))
				self.data_list.append(data_list_tmp)
				# data_list_tmp = [('[CLS]','[CLS]')]
				data_list_tmp = []

			else:
				row = row.strip('\n').split(' ')

				if row[0] in ['。', '？','！']:
					self.article_id_list.append(idx)
					self.data_list.append(data_list_tmp)
					data_list_tmp= []

				elif row[0] not in ['摁','嗯','啦','喔','欸','啊','齁']:
					data_tuple = (row[0], row[1])
					data_list_tmp.append(data_tuple)
				#data_list_tmp 儲存暫時的data_tuple(token,label)
		if len(data_list_tmp) != 0:
			self.data_list.append(data_list_tmp)

		# print(len(self.data_list), len(self.article_id_list))
		# print(self.data_list[0])
		# traindata_list, testdata_list, traindata_article_id_list, testdata_article_id_list=train_test_split(self.data_list,self.article_id_list,test_size= 0.33)
		# print('ex1 ',self.data_list[2])

	def get_stc_label(self):
		all_stcs = list()
		all_labels = list()

		for article_txt_tuple, article_id in zip(self.data_list, self.article_id_list):

			txt_len = len(article_txt_tuple) #(文章數，每個文章對應的總字數) (word, label)
			stc = str() #存字數= max_stc_len的字串
			labels = ['[CLS]'] # 存該字串對應的label

			for idx, (word, label) in enumerate(article_txt_tuple):

				stc += word
				labels.append(label)

			labels.append('[SEP]')
			
			all_stcs.append(stc)
			all_labels.append(labels)

		all_stcs_clean = []
		all_labels_clean = []

		for stc, label in zip(all_stcs,all_labels):
			
			stc_clean = re.sub(r'(醫師：)|(個管師：)|(民眾：)|(家屬：)|(護理師：)', '', stc)
			all_stcs_clean.append(stc_clean)

			len_diff = len(stc) - len(stc_clean)
			
			if len_diff >= 3:

				del label[1:1+len_diff]

			all_labels_clean.append(label)


		print('sentences總數: {}'.format(len(all_stcs)))
		print('labels總數: {}'.format(len(all_labels)))
		# print(all_stcs[0])
		# print(all_labels[0])
		return all_stcs_clean, all_labels_clean

	def tag2id(self, stcs_label):

		all_label = list()
		for stc_label in stcs_label:
			for label in stc_label:
				all_label.append(label)

		labels_set = sorted(set(all_label))
		tag2id_dict = dict()

		for idx, label in enumerate(labels_set):
			tag2id_dict[label] = idx

		# tag2id_dict['[CLS]'] = len(tag2id_dict) 
		# tag2id_dict['[SEP]'] = len(tag2id_dict)

		return tag2id_dict

	def label_to_ids(self, tag_to_id, raw_labels):

		label2id = []
		for stc_labels in raw_labels:
			stc_label_ids = [tag_to_id[label] for label in stc_labels]
			label2id.append(stc_label_ids)
		return label2id

	def get_stcs_label2ids(self):

		stcs, labels = self.get_stc_label()
		tag2id = self.tag2id(stcs_label= labels)
		labels_ids= self.label_to_ids(tag_to_id= tag2id, raw_labels= labels)

		return stcs, labels_ids


if __name__ == '__main__':

	file_path = 'data/train_input.data'

	with open(file_path, 'r', encoding='utf-8') as f:
		data=f.readlines()
	stcs, labels = preprocess2(data= data).get_stcs_label2ids()
	print('output stc idx = 0:\n',stcs[:10])
	print('output label idx = 0\n',labels[:10])

	print(max(stcs, key=len))
	print(len(max(stcs, key=len)))

	# txt = '醫師：回去還好嗎'
	# label = labels[0]
	# txt_clean = re.sub(r'(醫師：)|(個管師：)|(民眾：)|(家屬：)|(護理師：)', '', txt)
	# print(txt_clean)

	# len_diff = len(txt) - len(txt_clean)
	# print(len_diff)

	# del label[1:1+len_diff]

	# print(label)

