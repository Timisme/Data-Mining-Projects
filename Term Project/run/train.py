import torch 
import torch.nn
from sklearn.metrics import f1_score

def train(model, optimizer, train_loader, test_loader, num_epochs, device):

	train_loss = {}
	test_loss = {}
	train_f1 = {}
	test_f1 = {}

	for epoch in range(num_epochs):

		epoch_loss = 0
		iteration = 0

		model.train()

		for idx, batch_dict in enumerate(train_loader):

			print('idx: ',idx+1)

			input_ids = batch_dict['input_ids'].to(device)
			attention_mask = batch_dict['attention_mask'].to(device)
			labels = batch_dict['labels'].to(device)

			model.zero_grad()

			pred_labels = model(input_ids, attention_mask.bool())

			loss = model.neg_log_likelihood(input_ids, attention_mask, labels)
			loss.backward()
			optimizer.step()

			# mask gt labels 
			labels = batch_dict['labels'].numpy()
			masks = batch_dict['attention_mask'].numpy()
			# masked_list = (labels*mask).numpy()

			labels_nopad = []
			for label , seq_mask in zip(labels, masks):

				seq = [tag for tag, mask in zip(label, seq_mask) if mask == 1]
				labels_nopad.append(seq)

			# one dim array 
			preds= [tag for seq in pred_labels for tag in seq]
			gts= [tag for seq in labels_nopad for tag in seq]

			epoch_loss += loss.item()
			iteration += 1

			print('pred_labels', pred_labels)
			print('preds:', preds)
			print('gts:',gts)
			print(f1_score(y_true= gts, y_pred= preds, average= 'macro'))
			print(f1_score(y_true= gts, y_pred= preds, average= 'micro'))
			print(loss.item())

		f1 = f1_score(y_true= gts, y_pred= preds, average= 'macro')
		avg_loss = epoch_loss / iteration

		print('epoch {}/{} | train_f1 {:.2f} | train_loss {:.2f}'.format(epoch, num_epochs, f1, avg_loss))

	return model
	
if __name__ == '__main__':

	data = torch.tensor([[1,3,2],[4,3,1]])
	print(data.size())
	print(torch.flatten(data))