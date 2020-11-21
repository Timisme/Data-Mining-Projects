# Ensemble 

![](https://i.imgur.com/QIQ6nql.png =50%x)

## Bagging - 用於strong classifier

:::info
Bagging概念很簡單，從訓練資料中隨機抽取(取出後放回，n<N)樣本訓練多個分類器(要多少個分類器自己設定)，每個分類器的權重一致最後用投票方式(Majority vote)得到最終結果，而這種抽樣的方法在統計上稱為bootstrap。
:::

    Bagging的精神在於從樣本中抽樣這件事情，如果模型不是分類問題而是預測的問題，分類器部份也可以改成regression，最後投票方式改成算平均數即可。如果是用Bagging會希望單一分類器能夠是一個效能比較好的分類器
    
#### Bagging的優點在於原始訓練樣本中有噪聲資料(不好的資料)，透過Bagging抽樣就有機會不讓有噪聲資料被訓練到，所以可以降低模型的不穩定性(較robust，較不容易overfitting)

## Random Forest

:::info
DT 容易overfit，RF利用Bagging的方式降低Overfit程度，但是光用resampling 的效果並不大。RF的精隨在每次要產生DT的branch時都隨機決定那些feature當作input。
:::

### Out of Bagging 

不用特別把training set再切成validation set，利用OOB就可以達到cross validation的效果

:::info
某些classfier只給到一些sample，再用該classifier去cross validate它沒有看到過的sample
:::

![](https://i.imgur.com/d7A9UDr.png =50%x)

---

# Boosting - 用於 Weak classifier

:::info
Boosting算法是將很多個弱的分類器(weak classifier)進行合成變成一個強分類器(Strong classifier)，和Bagging不同的是分類器之間是有關聯性的，是透過將舊分類器的錯誤資料權重提高，然後再訓練新的分類器，這樣新的分類器就會學習到錯誤分類資料(misclassified data)的特性，進而提升分類結果。
:::

    如果一個weak clasifier的error rate 低於 50%，則透過boosting可以達到0%的error rate

#### 如何得到不同的弱分類器?

1. Resampling training data to form a new set 
2. ==Re-weighting==

![](https://i.imgur.com/7ILmgpK.png =50%x)


## Adaboost 

:::info
針對一個弱分類器f1，可以找出一筆sample data，透過更改sample data的權重，使得f1分類的error=0.5(random classification)，則可以利用f2特別訓練這筆sample data得到更好的效果。
:::

![](https://i.imgur.com/MqKbHkg.png =50%x)


## Random Forest 

:::info
精隨在於，利用bagging方式，從N筆training data中以取出不放回的方式隨機抽取N筆data(代表可以data重複)，給予每個DT，然後每個DT在生成branch的時候都會隨機挑取固定個數個features，當作split條件
:::

![](https://i.imgur.com/5HDkPR9.png =50%x)

    Question: 要如何決定每棵樹挑幾個subset of features?

:::info
RF判斷一筆資料的class的方式為，每棵樹都會針對該筆data做出判斷，然後用多數決的方式決定這筆data的label
:::

#### out of bag dataset 
![](https://i.imgur.com/zxVQuoW.png =50%x)

如何判斷RF的分類效果?

    利用out of bag dataset 丟進該tree 去看看該tree有沒有正確label

![](https://i.imgur.com/cn9sLrw.png =50%x)


