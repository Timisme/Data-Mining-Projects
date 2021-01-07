import numpy as np 
import time  

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

class HITS():
	def __init__(self, L):
		self.L = L 
		self.n = L.shape[0]
		self.a = np.ones(self.n)
		self.h = np.ones(self.n)
		# self.num_iter = num_iter

	def get_scores(self, epsilon= 1e-4):

		epsilon_vector = epsilon*np.ones(self.n)

		while True:

			h_old = self.h 
			a_old = self.a

			self.a = np.dot(self.L, h_old)
			max_score = self.a.max(axis= 0)

			if max_score != 0:
				self.a = self.a * (1/max_score) # mu
			# print(self.a)
			self.h = np.dot(self.L, a_old)
			max_score = self.h.max(axis= 0)

			if max_score != 0:
				self.h = self.h * (1/max_score)

			# 當h, a更新差值對於每個Page都小於epsilon時stop 
			if (((abs(self.h - h_old) < epsilon_vector).all()) &
			((abs(self.a - a_old) < epsilon_vector).all())):
				break

		return self.h, self.a

def main():
	n = 10
	L = np.random.randint(2, size= (n, n))

	hit_algo = HITS(L= L)

	print(f"L : {L}")
	print('-'*50)
	print(hit_algo.get_scores())

if __name__ == '__main__':
	main()

