from torch.utils.data import Dataset
import torch

class bert_stc_dataset(Dataset):
    
    def __init__(self, stcs, labels, tokenizer, max_length):
        
        self.stcs = stcs
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        # self.pad_labels = []

        #已經在preprocess2 做完label 0 padding
        # for i in range(len(labels)):
        #     temp_label = [0]*max_length
        #     temp_label[:len(labels[i])] = labels[i]
        #     self.pad_labels.append(temp_label)
            
        
    def __len__(self):
        return len(self.stcs)
    
    def __getitem__(self, idx):
        
        txt = str(self.stcs[idx])

        txt = ' '.join(list(txt))
        # print(txt)
        
        encoding = self.tokenizer.encode_plus(
            txt,
#             truncation= True,
            max_length= self.max_length,
            padding = 'max_length',
            add_special_tokens=False,
#             pad_to_multiple_of=True,
            return_attention_mask= True,
            return_token_type_ids= False,
            return_tensors='pt')
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels' : torch.tensor(self.labels[idx], dtype= torch.long)
        }

if __name__ == '__main__':

    from txt_preprocess2 import preprocess2
    from transformers import BertModel, BertTokenizer
    from torch.utils.data import DataLoader
    from model2 import model_crf
    from sklearn.model_selection import train_test_split

    # file_path = 'data/train_input.data'
    # with open(file_path, 'r', encoding='utf-8') as f:
    #     data=f.readlines()

    # stcs, labels = preprocess2(data= data).get_stcs_label2ids()
    # print('stcs: ',stcs[15])
    # stcs, raw_labels = preprocess2(data= data).get_stc_label()
    # tag2id_dict = preprocess2(data= data).tag2id(raw_labels)
    # n_tags = len(tag2id_dict)
    # print('n_tags', n_tags)
    # print(tag2id_dict)
    stcs = ['我是大AAI陰莖','哈哈哈alspdsds規']
    labels = [[1,1],[2,3]]
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    max_length = max([len(txt) for txt in stcs])
    # print(max_length)

    dataset = bert_stc_dataset(stcs= stcs, labels=labels, tokenizer= tokenizer, max_length= max_length)
    print(dataset[0]['input_ids'])
    # print(stcs[15])
    # print('input_ids', dataset[15]['input_ids'])
    # print('attention_mask:', dataset[15]['attention_mask'])
    # print('label:', dataset[15]['labels'])

    # for i in range(len(dataset)):
    #     if len(dataset[i]['input_ids']) != max_length:
    #         print(i)

    # train_x, test_x, train_y, test_y = train_test_split(stcs, labels, test_size= 0.33, shuffle= False, random_state= 42)
    # train_dataset = bert_stc_dataset(stcs= train_x, labels= train_y, tokenizer= tokenizer, max_length= max_length)
    # print('training stcs 總數: {}'.format(len(train_dataset)))
    # train_dataloader = DataLoader(train_dataset, batch_size= 32, shuffle= True)

    # print(train_x[15])
    # print('input_ids', train_dataset[15]['input_ids'])
    # print('attention_mask:', train_dataset[15]['attention_mask'])
    # print('label:', train_dataset[15]['labels'])


    # dataloader = DataLoader(dataset, batch_size= 10, shuffle= True)

    # batch= next(iter(dataloader))
    # print('batch mask size: ',batch['attention_mask'].size())

    # # print(batch['attention_mask'].permute(1,0).size())
    # # print('label: ', batch['labels'])

    # labels = batch['labels'].numpy()
    # masks = batch['attention_mask'].numpy()
    # # masked_list = (labels*mask).numpy()

    # labels_nopad = []
    # for label , seq_mask in zip(labels, masks):

    #     seq = [tag for tag, mask in zip(label, seq_mask) if mask == 1]
    #     labels_nopad.append(seq)

    # print('batch_ids\n',batch['input_ids'])
    # print('未Padding的gt labels:\n',labels_nopad)
    # model = model_crf(n_tags= n_tags)

    # # print(batch['attention_mask'].bool())
    # pred_seq = model(batch['input_ids'], batch['attention_mask'].bool())

    # print('pred seq:\n',pred_seq)
