import sys

sys.path.insert(1, 'D:\\python git projects\\Data-Mining-Projects\\project 3')
# print(sys.path)

from pagerank import get_n_M, PowerMethod
from hits import HITS

for i in range(1, 4):

	filename= f'graph_{i}_new.txt'
	filename2 = f'../graph_{i}.txt'

	# print('-'*50)
	n, M, V= get_n_M(filename= filename)
	n1, M1, V1 = get_n_M(filename2)

	PR= PowerMethod(n=n, M= M)
	PR1 = PowerMethod(n1, M1)

	# print('-'*50)
	hit_algo = HITS(filename= filename)
	hit_algo2 = HITS(filename2)

	h = hit_algo.get_scores()[0]
	a = hit_algo.get_scores()[1]

	h1 = hit_algo2.get_scores()[0]
	a1 = hit_algo2.get_scores()[1]

	
	print(f'new PR: {PR}\nnew h: {h}\nnew a: {a}')
	print('-'*50)
	print(f'old PR: {PR1}\nold h: {h1}\nold a: {a1}')
	print('-'*50)