import torch 
import torch.nn as nn 
from sklearn.metrics import f1_score

def test(model, test_dataloader, device):

  preds_epoch = []
  gts_epoch = []
  epoch_loss = 0
  iteration = 0

  model.eval()

  for idx, batch_dict in enumerate(test_dataloader):

    # print('idx: ',idx+1)
    input_ids = batch_dict['input_ids'].to(device)
    attention_mask = batch_dict['attention_mask'].to(device)
    labels = batch_dict['labels'].to(device)

    with torch.no_grad():
      loss, pred_labels = model(input_ids, attention_mask.bool(), labels)

    # mask gt labels 
    labels = batch_dict['labels'].numpy()
    masks = batch_dict['attention_mask'].numpy()

    labels_nopad = []
    for label , seq_mask in zip(labels, masks):

      seq = [tag for tag, mask in zip(label, seq_mask) if mask == 1]
      labels_nopad.append(seq)

    # one dim array 
    preds= [tag for seq in pred_labels for tag in seq]
    gts= [tag for seq in labels_nopad for tag in seq]

    preds_epoch += preds
    gts_epoch += gts

    epoch_loss += loss.item()
    iteration += 1

  f1_macro = f1_score(y_true= gts_epoch, y_pred= preds_epoch, average= 'macro')
  f1_micro = f1_score(y_true= gts_epoch, y_pred= preds_epoch, average= 'micro')
  avg_loss = epoch_loss / iteration
  
  print('test_f1(macro, micro) ({:.2f},{:.2f}) | test_avg_loss {:.2f}'.format(f1_macro, f1_micro, avg_loss))

  return f1_macro, f1_micro, avg_loss

if __name__ == '__main__':

  test_hist = {}

  test_hist[1] =1.23

  print(test_hist)


  