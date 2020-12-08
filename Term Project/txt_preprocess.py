from sklearn.model_selection import train_test_split

# file_path = 'data/train_input.data'

class preprocess:

	def __init__(self, data):

		# with open(file_path, 'r', encoding='utf-8') as f:
		# 	data=f.readlines()#.encode('utf-8').decode('utf-8-sig')

		data_list, data_list_tmp = list(), list()
		article_id_list=list()
		# article_id_list = list()
		idx=0

		for row in data:
			data_tuple = tuple()
			if row == '\n':
				article_id_list.append(idx)
				idx+=1
				# data_list_tmp.append(('[SEP]','[SEP]'))
				data_list.append(data_list_tmp)
				# data_list_tmp = [('[CLS]','[CLS]')]
				data_list_tmp = []
			else:
				row = row.strip('\n').split(' ')
				data_tuple = (row[0], row[1])
				data_list_tmp.append(data_tuple)
				#data_list_tmp 儲存暫時的data_tuple(token,label)
		if len(data_list_tmp) != 0:
			data_list.append(data_list_tmp)
		#data_list 是 list of tuple 的list
	    
	    # here we random split data into training dataset and testing dataset
	    # but you should take `development data` or `test data` as testing data
	    # At that time, you could just delete this line, 
	    # and generate data_list of `train data` and data_list of `development/test data` by this function
		self.traindata_list, self.testdata_list, self.traindata_article_id_list, self.testdata_article_id_list=train_test_split(data_list,
	                                                                                                    article_id_list,
	                                                                                                    test_size=0.33,
	                                                                                                    random_state=42)
		self.data_list = data_list
		self.article_id_list = article_id_list

	def get_scts_labels(self, max_stc_len):
    
		all_stcs = list()
		all_labels = list()

		for article_txt_tuple, article_id in zip(self.data_list, self.article_id_list):

			txt_len = len(article_txt_tuple) #(文章數，每個文章對應的總字數) (word, label)
			stc = str() #存字數= max_stc_len的字串
			labels = list() # 存該字串對應的label
			stcs = list() # 存該article的所有sentence
			art_labels = list() # 存該article所有 labels

			n_stc = int(txt_len / max_stc_len) + 1 

			for idx, (word, label) in enumerate(article_txt_tuple):

				stc += word
				labels.append(label)
				if ((idx+1) % max_stc_len) == 0 : #整除
					stcs.append(stc)
					art_labels.append(labels)
					stc = str()
					labels = list()

				elif len(stcs) == (n_stc - 1): #倒數最後一句 長度可能不夠
					stcs.append(stc)
					art_labels.append(labels)

			all_stcs.append(stcs)
			all_labels.append(art_labels)

		stcs = [txt for art_txt in all_stcs for txt in art_txt]
		labels = [label for art_label in all_labels for label in art_label]

		print('sentences總數: {}'.format(len(stcs)))
		print('labels總數: {}'.format(len(labels)))

		return stcs, labels

	def tag2id(self, stcs_label):

		all_label = list()
		for stc_label in stcs_label:
			for label in stc_label:
				all_label.append(label)

		labels_set = set(all_label)
		tag2id_dict = dict()

		for idx, label in enumerate(labels_set):
			tag2id_dict[label] = idx


		return tag2id_dict

	def label_to_ids(self, tag_to_id, raw_labels):

		label2id = []
		for stc_labels in raw_labels:
			stc_label_ids = [tag_to_id[label] for label in stc_labels]
			label2id.append(stc_label_ids)
		return label2id


if __name__ == '__main__':

	file_path = 'data/train_input.data'

	with open(file_path, 'r', encoding='utf-8') as f:
		data=f.readlines()#.encode('utf-8').decode('utf-8-sig')

	preprocessor = preprocess(data)
	stcs, labels = preprocessor.get_scts_labels(max_stc_len=50)
	print(stcs[:2])
	# print(data[:10])

