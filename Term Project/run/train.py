import torch 
import torch.nn
from sklearn.metrics import f1_score

def train(model, optimizer, train_loader, test_loader, num_epochs, device):

	train_loss = {}
	test_loss = {}
	train_f1 = {}
	test_f1 = {}

	for epoch in range(num_epochs):

		preds = []
		gts = []
		epoch_loss = 0
		iteration = 0

		model.train()

		for idx, batch_dict in enumerate(train_loader):

			input_ids = batch_dict['input_ids'].to(device)
			attention_mask = batch_dict['attention_mask'].to(device)
			labels = batch_dict['labels'].to(device)

			model.zero_grad()

			score, pred_labels = model(input_ids, attention_mask)

			loss = model.neg_log_likelihood(input_ids, attention_mask, labels)
			loss.backward()
			optimizer.step()

			preds.append(torch.flatten(pred_labels))
			gts.append(torch.flatten(labels))
			epoch_loss += loss.item()
			iteration += idx

		f1_score = f1_score(y_true= gts, y_pred= preds)
		avg_loss = epoch_loss / iteration

		print('epoch {}/{} | train_f1 {:.2f} | train_loss {:.2f}'.format(epoch, num_epochs, f1_score, iteration))

	return model
	
if __name__ == '__main__':

	data = torch.tensor([[1,3,2],[4,3,1]])
	print(data.size())
	print(torch.flatten(data))