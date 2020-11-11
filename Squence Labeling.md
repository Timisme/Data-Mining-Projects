# Squence Labeling 

[參考台大李弘毅教授的課程](https://www.youtube.com/watch?v=o9FPSqobMys)

input x as a sequence to predict y also as a sequence 

## Pos tagging 

### HMM

Step 1 

先建立 Pos tagging (label) 順序
且知道這些 Pos tagging 順序之間的Probability 
可知道一個pos tag sequence的機率

![](https://i.imgur.com/SLRfJRT.png)

Step 2 

如果知道sensor model (tagging 有多少機率是哪個state)

![](https://i.imgur.com/T0Rd1zo.png)

所以可以算出一組state sequence出現的機率

## 計算機率
![](https://i.imgur.com/UrRNU52.png)

![](https://i.imgur.com/nBFv1MD.png)

:::info
如何計算 每個transition之間與sensor之間的機率?
:::

    透過training dataset 
    
所以給定一組evidence， 透過training可以知道該組evidence sequence對應的每個state sequence的機率，但是

:::info
如何找到最佳state sequence???
:::

![](https://i.imgur.com/6WE18Bo.png)

# Viterbi Algorithm 找出機率最高的那組sequence

input : 給定P(Y|X)
output : 在給定X情況下，出現機率最高的那組Y

complexity = len(seq)*(num_tag**2)


## HMM 缺點

![](https://i.imgur.com/pm0ljV7.png)

原因 HMM 將transition & sensor視為獨立

:::info
HMM 可能太注重於transition之間的機率，而忽略training資料中實際發生的情況(腦補沒看過的pattern)，所以當training data 很少的時候用HMM就不錯
:::

# 超強CRF

也假設transi & sensor為獨立的情況下，解決HMM遇到的問題

![](https://i.imgur.com/PMmlDLa.png)

:::info
CRF 假設 P(X,Y) ~ 正比於 exp(w*fi(x,y))
且 p(y|x) = exp(w*fi(x,y))/Z(x)
:::

## 機率計算 

![](https://i.imgur.com/a9IbE8s.png)
![](https://i.imgur.com/vragMVF.png)
![](https://i.imgur.com/iDLy2ss.png)


    CRF的目的，也是找出P(X,Y)這個機率，但更靠譜
    
# Feature Dimension for crf 

:::info
假設有S個tags，L個words(states), 則feature vector part 1 有 S*L維(所有pairs) --- 且值為各pairs出現的次數
:::

part 2 

![](https://i.imgur.com/C87oc8a.png)


:::info
tags之間的所有組合 value為出現次數，dimension = s*s + 2*s (start and end也有)
:::


# 如何訓練CRF?
![](https://i.imgur.com/dOuezpu.png)

:::info
目標函數O(w)為最大化每個不同長度sequence下看到最有可能的label seq的機率
:::

    注意：此時要最佳化O(w)
    
:::info
該念：s,t這個pair在training出現次數越多則weight增加越多，而且weight代表的就是機率
:::

    訓練好後，再用viterbi找出最佳解(inference)

# Viterbi 可以設定限制 讓state sequence只包含合理的順序


![](https://i.imgur.com/j1Fbgmi.png)


:::info
最好的方式就是將RNN和CRF/structured perceptiron/ svm 結合 
:::

# 神之概念 串起來!!!

![](https://i.imgur.com/uhuuOw7.png)

:::info
用bilstm 的output 可以知道再給定的一組x sequence下，被固定label的機率，即p(y|x)再利用換算成p(x|y)
:::

