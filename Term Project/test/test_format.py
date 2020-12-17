import csv
import re
from transformers import BertTokenizer

class test_output():
    def __init__(self, data):
        
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

                if row[0] in ['。', '？','！','，','～','：',',']:
                    
                    self.word_id.append(word_id_tmp)
                    self.word_article_id.append(article_id_tmp)
                    self.data_list.append(data_list_tmp)
                    data_list_tmp = []
                    article_id_tmp = []
                    word_id_tmp = []
                    
                elif row[0] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
                      
                    data_tuple = (row[0].lower(), row[1], article_id, word_id)
                    data_list_tmp.append(data_tuple)
                    article_id_tmp.append(article_id)
                    word_id_tmp.append(word_id)

                elif row[0] not in ['摁','嗯','啦','喔','欸','啊','齁','嘿','…','...']:
                    
                    data_tuple = (row[0], row[1], article_id, word_id)
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
    
    def get_stc_label(self):
        
        all_stcs = list()
        all_labels = list()
        all_article_ids = list()
        all_word_ids = list()

        for stc_list in self.data_list:

            txt_len = len(stc_list) #(文章數，每個文章對應的總字數) (word, label)
            stc = str() #存字數= max_stc_len的字串
            labels = []
            article_ids = []
            word_ids = []
            

            for idx, (word, label, article_id, word_id) in enumerate(stc_list):

                stc += word
                labels.append(label)
                article_ids.append(article_id)
                word_ids.append(word_id)

            all_stcs.append(stc)
            all_labels.append(labels)
            all_article_ids.append(article_ids)
            all_word_ids.append(word_ids)
        
        assert len(all_stcs) > 0, 'all stcs len = 0' 
        
        all_stcs_clean = []
        all_labels_clean = []
        all_article_ids_clean = []
        all_word_ids_clean = []
        idx = 0
        
        for stc, label, article_id, word_id in zip(all_stcs, all_labels, all_article_ids, all_word_ids):
            stc_clean = re.sub(r'(醫師)|(個管師)|(民眾)|(家屬)|(護理師)', '', stc)
            # print(stc, stc_clean, label)
            if (len(stc_clean)>=2) & (len(set(label)) >= 2):  
            # print(stc_clean, stc)
                all_stcs_clean.append(stc)
                all_labels_clean.append(label)
                all_article_ids_clean.append(article_id)
                all_word_ids_clean.append(word_id)

            elif (len(stc_clean)>=2) & (((idx+1) % 5) == 0):
                all_stcs_clean.append(stc)
                all_labels_clean.append(label)
                all_article_ids_clean.append(article_id)
                all_word_ids_clean.append(word_id)
            idx += 1

            # 這一步就先把label 做 0 padding
            
        max_length = len(max(all_stcs_clean, key=len))
        assert max_length > 0, 'max length less than 1'
        
        pad_labels = []

        for i in range(len(all_labels_clean)):
            temp_label = ['[PAD]']*max_length
            temp_label[:len(all_labels_clean[i])] = all_labels_clean[i]
            pad_labels.append(temp_label)

        print('sentences總數: {}'.format(len(all_stcs_clean)))
        print('labels總數: {}'.format(len(all_labels_clean)))
            
        return all_stcs_clean, pad_labels, all_article_ids_clean, all_word_ids_clean
    
    def tag2id(self, stcs_label):

        all_label = list()
        for stc_label in stcs_label:
            for label in stc_label:
                all_label.append(label)

        labels_set = sorted(set(all_label))
        tag2id_dict = {'[PAD]':0} #固定將PAD id設為0

        labels_set.remove('[PAD]')

        for idx, label in enumerate(labels_set):
            tag2id_dict[label] = idx+1

        return tag2id_dict

    def label_to_ids(self, tag_to_id, raw_labels):

        label2id = []
        for stc_labels in raw_labels:
            stc_label_ids = [tag_to_id[label] for label in stc_labels]
            label2id.append(stc_label_ids)
        return label2id

    def get_stcs_label2ids(self):

        stcs, labels, article_ids, word_ids = self.get_stc_label()
        tag2id = self.tag2id(stcs_label= labels)
        labels_ids= self.label_to_ids(tag_to_id= tag2id, raw_labels= labels)

        return stcs, labels_ids, article_ids, word_ids

if __name__ == '__main__':

	with open('data/train_input.data', 'r', encoding= 'utf-8') as f:
		data = f.readlines()

	stcs, pad_labels, article_ids, word_ids = test_output(data= data).get_stcs_label2ids()

	tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

	encoding = tokenizer.batch_encode_plus(stcs, 
                                 # max_length= max_len,
                                 padding=True,
                                 add_special_tokens=False,
                                 return_attention_mask= True,
                                 return_token_type_ids= False,
                                 is_split_into_words=True,
                                 return_tensors='pt')
		self.hidden_dim = hidden_dim
		self.fc = nn.Linear(hidden_dim, self.n_tags)
		self.bert = BertModel.from_pretrained('bert-base-chinese')

		for param in self.bert.parameters():
			param.requires_grad = False