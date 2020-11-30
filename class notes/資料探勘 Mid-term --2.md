# 資料探勘 Mid-term --2 

###### tags: `資料探勘`

![](https://i.imgur.com/Vqlnpdd.png =50%x)
![](https://i.imgur.com/veHXGP6.png =50%x)

## Precision - recall trade-off plot 

:::info
precision & recall 會因為不同情況對threshold設定大小的關係有不同的變動，例如僅有在非常高機率的預測下才會predict 1，則precision 會很高，但是recall 反而會下降(因為很多真實為1的都沒有predict為1，門檻太高。)
:::

![](https://i.imgur.com/F1xkrlO.png =50%x)

[precision & recall curve 資訊檢索](https://ithelp.ithome.com.tw/articles/10192869)

:::info
Average Precision 

在取出relevant的情況下，平均的precision。(每次的檢索結果會依照各個docu累進計算當下的precion & recall)

MAP 

不同QUERY下，AP的平均 -> 考量每一個狀況的全盤指標
:::

    Average Precion 問題
    1. 不能偵測單一不正常分類的部分
    2. 預知道特定query的表現
    

:::info

Precision at k 
針對搜尋引擎的問題，更在乎在總檢所文章總數為k時，precision為多少。
(特定的前幾筆文章，用precision at k衡量較能符合使用者感受)

但是一旦relevant文章總數高，自然precision at k也會高。

R-Precision

==the precision at the R-th position in the ranking==
==將K設為relevant文章總數，則precision = recall(break even pnt)==

:::

:::info
marcoaveraging: 重視種類
所有類別的每一個統計指標值的算數平均值


microaveraging: 重視量
針對data所有instance不分類別得做confusion matrix
:::

:::info

sensitivity : 所有ground truth為Positive的data中，總共有多少比例被正確分類為positive。

Specificity : 所有ground truth為negative總共正確抓出多少比例的true negative。
:::

==smaple class不balance時用accu不能完整表達模型的預測能力==

## ROC curve 

:::info
一個sensitivity vs (1-specificity) 曲線，曲線變動來自於對於分類threshold的設定大小變動。

(true positive vs false positive rate)

y軸為答案是1，也正確猜1的比例，x是答案是0，但錯誤地猜成1的比例。

如果threshold設很低(很容易就猜1)，則sensitivity很高，但(1-specifitivity)也很高。

把threshold設更高，兩者可能皆會降低，要找一個threshold，使地有最大true posi/false posi比例。
:::

![](https://i.imgur.com/hg7ULxW.png =50%x)

    對於imbalanced data，利用Precision or recall有更好地解釋能力。
    
    auc 幫助判斷哪個分類器表現更好。(與閥值設定無關)
    
==在非常不balanced的data用roc做比較都有較stable的解釋力==

:::info

Q1 : f1 score 和 break even pnt關係？

break even point -> precision = recall = f1 score
:::

![](https://i.imgur.com/rhKcwyG.png =50%x)

![](https://i.imgur.com/P5ipshs.png =50%x)

![](https://i.imgur.com/gAB2zPb.png =50%x)

# Ranked list 

1. NDCG

## 度量一個query中各個docu的gain，根據docu在預測中排序的位置
![](https://i.imgur.com/AZWSblA.png =50%x)

2. Kendall-tau 

## 度量兩組具順序的list之間的關聯性。

![](https://i.imgur.com/ub8zw69.png =50%x)

共有C n取2種組合。(兩組中一致的組合順序相同，視為一組concordant)
    
    問題: 如果有一些bad ranked data，則kendall數值下降很快。
    (sensitive)
    
## Cohen's Kappa 

== 度量兩個raters之間的同意一致性。其中一個rater為分類器，另一個為ground truth。

    假設兩個raters的決定互相獨立，可以算期望的agreement。

![](https://i.imgur.com/tIJOuXE.png =50%x)

-----

# 關聯法則

## 定義 

::: info
support : fraction of transactions that contain an itemset 
:::

![](https://i.imgur.com/l8VzJAC.png =50%x)

## Appriori algo 

### appriori property(anti monotone)

==核心概念: 一個frequent itemset的所有subset必定也是freq==
==一組itemset的support不會大於其任一subset的support==

    若subset非freq，則其superset必定也非freq。
    
:::info
steps
1. 找出freq one itemset
2. 有交集用聯集產生candidate itemset (Lk self join)
3. subset check，如果subset非freq，則prun candidate itemset
:::

## 如何加速計算candidates support的方法？

1. Hash Tree
2. FP growth 

## Rules Generation 

:::info
對於一個freq itemset m，找出其subset p，做出inference p->(m-p)
:::

## reduction on database size

![](https://i.imgur.com/rYyLpvE.png =50%x)

---

## frequent pattern mining bottleneck 

1. 多次掃描資料庫 costly
2. 產生太多的candidates list

# FP-Growth 

1. mining in main memery
2. 不做candidate generation 
3. 頻率較多的items有更大的機率share item

:::info
steps 

1. 建立fp tree(header also)
    * 掃描第一次db，建立freq one itemset 
    * 依照support大小排序，transactions扣除非freq後也照support排序
    * 依序依照transaction插入tree建立fp tree
3. frequent pattern growth
    * divide into 條件fp tree，跟一個header指向之freq item相連
:::

![](https://i.imgur.com/ZT99HCA.png =50%x)

