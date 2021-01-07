import numpy as np 

'''
Tim's self study note in English :
參考standfort cs 課程講義概念

Link Matrix of the web L, Lij = page i links to page js 
transpose of L = L_trans = page j links to pages is 

a = authorities vector
h = hubs vector 

lambda = scaling factor for calculating h 
mu = scaling factor for calculating a 
'''

'''
formulation: 

start with h a vector of all 1's (假設初始page hubs 皆為1)
scale so the largest component is 1

1. a = mu * L_trans * h
2. h = lambda * L * a
iteration ...
'''

 