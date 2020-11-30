# 資料探勘 Mid term 

###### tags: `資料探勘`

## Association Rule 

### FP Growth

:::info
Frequent Pattern Growth 規則

Let a be a frequent itemset in DB, B be a's conditional
pattern base, and b be an itemset in B. Then a 聯集 b is a
frequent itemset in DB iff b is frequent in B.
:::

#### why FP growth the winner?

1. Divide and Conquer (根據目前已知freq itemsets細分後找出所有子集freq ) 
2. 不用找candidate?
3. Compressed database?
4. 不用重複掃描整個database
5. 找出local freq items，建立sub fp tree，沒有pattern search and matching(第二次掃DB時已經將完整tree建立完成)

#### 以下重點(why?)

:::info
1. 為甚麼要sort 1-itemset (by support)?
2. descent order方式建立fp growth?
    * 當items的count相同，如何排序?   
:::

## Multi-level Association Rule 

:::info
high level 的問題
相同的support值會產生很多的frequent itemsets(產生很多沒有很重要的關聯)
愈高level的item愈容易滿足min support?

uniform support 會遇到兩個問題
1. 設太高 -> 只有high level會留下
2. 設太低 -> 太多freq itemsets

Reduced Support : 4 strategies 
:::

    A set A is a superset of another set B if all elements of the set B are elements of the set A.

![](https://i.imgur.com/ZqQ5nyC.png =50%x)


:::info

Max-patterns
freq patterns without frequent super pattern。
如BCDE is max-pattern，but BCD not(even frequent as well)

Closed frequent itemsets
An itemset is closed in a data set if there exists no superset that has the same support count as this original itemset.(較寬鬆，即便superset有超過min support但不及original set，就是closed)
:::

==max patterns 和 closed frequent itemset差在哪?==
    
    Frequent item set 𝑋∈𝐹 is maximal if it does not have any frequent supersets.
    Frequent item set X ∈ F is closed if it has no superset with the same frequency

![](https://i.imgur.com/BxXRA1F.png =50%x)

==用closed freq itemset找出的rule更有代表性。==
![](https://i.imgur.com/bAhDPsR.png =50%x)

---

## Quantitative 關聯法則

![](https://i.imgur.com/eAeIoG6.png =50%x)

:::info
問題:

當attribute被切的很多，資料本身各item的 support value很低，confidence很容易就很高(attribute的 support value低) 
:::

----

# Text Analysis 

:::info
Inverted index:
給定文字，輸出output為文章id及在文章內位置
:::

### Lexical processing 

1. tokenization
2. stemming (複數 字根 去除等。)
3. removing stop words 降低size reduction 

:::info
TF-IDF 
IDFj = log(total documents in the set / docus which contain the term W)
:::

![](https://i.imgur.com/rYKVK1t.png)

### BM25

    TF-IDF 的複雜版。算兩個向量的SCORE

#### LSA & LSI example 

    svd -> 無法運算大量文本

#### word embedding 

:::info
問題:
遇到沒看過的字詞(out of bag)，沒有分辨及預測力
:::
    
#### information extraction 

:::info
workflow 
1. 斷字和辭意分系(lexical analysis)
2. paper name idenfication 
3. shallow parsing? (syntactic analysis)
4. building relations 
5. inferencing? 
:::

![](https://i.imgur.com/suDMHRW.png)


---

# Sequence Pattern

![](https://i.imgur.com/KWIqB9m.png =50%x)

    element是時間t的大單位，一個element細分為多個items

## Subsequence 

![](https://i.imgur.com/fQtvM5M.png =50%x)

## Sequential pattern mining 目標為?
    
    給定一組序列，找出所有其frequent subsequences

![](https://i.imgur.com/G4MJ3ZC.png =50%x)

## Challenge 

    1. 計算量大 2. many scan of databases 3. 長序列準度問題

![](https://i.imgur.com/UAuDGeX.png =50%x)

## algorithm 

    特殊情況 將items 做mapping時將同個element中大於兩個freq item
    皆做組合
    
![](https://i.imgur.com/KuHFv1t.png)
 
:::info
注意:

(3)(5)是兩個不同時間的pattern，不是(3 5)的子集
:::
![](https://i.imgur.com/OB8bbof.png)

### FreeSpan 

運用概念 ==pattern projected== 

:::info
1. 將各序列依照item分別映射(project)到更小的projected database
2. 根據projected database繼續往下長subsequence
3. divide and conquer作法
4. 可以將完整的序列資料分成各種subset。
:::

![](https://i.imgur.com/ThL7Qoy.png =50%x)

![](https://i.imgur.com/2QWkJue.png =50%x)

![](https://i.imgur.com/INaUSfE.png =50%x)

### ==Prefix Span== 

:::info
優勢:
1. no candidate subsets to be generated 
2. projected DBs keep shrinking 
:::

![](https://i.imgur.com/ARQCuXn.png =50%x)

    每次針對item建立projected DB 時可以找到subset

![](https://i.imgur.com/JoQFynH.png =50%x)
![](https://i.imgur.com/B2lHdpq.png =50%x)

    prefix span 精神:
    先用prefix分別找projection db -> divide and conquer
    從db找Sequential pattern -> 和prefix 組合也是sp
    
    先把答案整理好，一個個往下做，和其他條獨立，很快收斂，速度快。

-----

# Machine Learning 

## 決策樹

:::info

1. hunt's algo : 隨機選擇feature去分類 ---> overfitting
2. Greedy Strategy 
    split the records based on an attribute test that optimizes certain criterion
    就是找到一個最佳的attribute可以使得目標被最大滿足(min | max)
    (在這時間點最好的解)
==nodes with homogeneous class distribution are preferred==
利用node impurity計算不純度
:::

![](https://i.imgur.com/YtKDALG.png =50%x)

### 常用計算node impurity算法
![](https://i.imgur.com/0MuNpRR.png =50%x)
![](https://i.imgur.com/P7ADzWW.png =50%x)

    決策樹訓練的目標函數為
    information gain = parent node entropy - weighted sum entropy(選擇能將info gain最大化的feature去split)

:::info
gini 和 entropy計算方式皆prefer splits that result in large num of partitions, each being small but pure。
:::

:::info
leaf node (stop) criterion 
1. 當劃分後每筆資料都是同個類別
2. 當劃分後每筆資料都有相同的features
3. early stopping -> reduce overfitting
::: 

    優點：
    1. 計算快速
    2. 可以很簡單的解釋data
    3. 表現和其他分類模型不會差很多
    4. 對於symbolic feature表現特好。

    問題:
    1. 有缺值對tree的訓練影響很大。
    2. nodes次數越多，愈容易overfitting。
    3. 如果feature交互作用才對結果有影響，決策樹沒辦法分類。
    4. 代表DT僅能找出單一feature對結果的影響。
    5. 對noise 很sensitive
    
    解決overfitting
    1. pre-pruning
        用更嚴謹的方式設定停損點
    2. ...
    
## KNN

![](https://i.imgur.com/5Iz9Fkb.png =50%x)

:::info
K值選取tricks

1. 如果k 太小，則很有可能會因為鄰近為noise data產生錯誤分類
2. k太大也可能因為選到距離太遠的feature(與自己太不像了還要選)
:::

## 貝氏

:::info
直接假設各feature之間條件獨立。
:::
![](https://i.imgur.com/BgyPrfr.png =50%x)

![](https://i.imgur.com/ONNwOVA.png =50%x)

:::info
優點:
1. robust to noise
2. 能處理missing value(計算時後當作1e-6等？)
:::
    