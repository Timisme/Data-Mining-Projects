from torch.utils.data import Dataset, DataLoader
import torch

class bert_stc_dataset(Dataset):
    
    def __init__(self, stcs, labels, tokenizer, max_length):
        
        self.stcs = stcs
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.pad_labels = []

        for i in range(len(labels)):
            temp_label = [0]*max_length
            temp_label[:len(labels[i])] = labels[i]
            self.pad_labels.append(temp_label)
            
        
    def __len__(self):
        return len(self.stcs)
    
    def __getitem__(self, idx):
        
        txt = str(self.stcs[idx])
        # print(txt)
        
        encoding = self.tokenizer.encode_plus(
            txt,
#             truncation= True,
            max_length= self.max_length,
            padding = 'max_length',
            add_special_tokens=True,
#             pad_to_multiple_of=True,
            return_attention_mask= True,
            return_token_type_ids= False,
            return_tensors='pt')
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label' : torch.tensor(self.pad_labels[idx], dtype= torch.long)
        }
        