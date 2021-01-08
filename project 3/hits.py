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
	def __init__(self, filename):

		I_dict = dict()

		with open(filename) as f:
			data = [tuple(line.strip().split(',')) for line in f.readlines()]
			for node_tuple in data:
				if node_tuple[0] not in I_dict.keys():
					I_dict[node_tuple[0]] = [node_tuple[1]]
				else:
					I_dict[node_tuple[0]].append(node_tuple[1])

		V = list(sorted(set(list(I_dict.keys()) + [ j for js in I_dict.values() for j in js])))

		self.L = np.zeros(shape= (len(V), len(V)))

		for node in I_dict.keys():
			i = V.index(node)

			for out_neighbor in I_dict[node]: 
				j = V.index(out_neighbor)
				
				self.L[i, j] += 1

		self.n = self.L.shape[0]
		self.a = np.ones(self.n)
		self.h = np.ones(self.n)

	def get_scores(self, epsilon= 1e-15):

		epsilon_vector = epsilon*np.ones(self.n)

		while True:

			h_old = self.h 
			a_old = self.a

			self.a = np.dot(self.L.transpose(), h_old)
			vector_size = np.linalg.norm(self.a) # 2norm

			if vector_size != 0:
				self.a = self.a * (1/vector_size) # mu
			# print(self.a)
			self.h = np.dot(self.L, a_old)
			vector_size = np.linalg.norm(self.h)

			if vector_size != 0:
				self.h = self.h * (1/vector_size)

			# 當h, a更新差值對於每個Page都小於epsilon時stop 
			if (((abs(self.h - h_old) < epsilon_vector).all()) &
			((abs(self.a - a_old) < epsilon_vector).all())):
				break

		return self.h, self.a

def main():


	filename = 'graph_5.txt'

	# L = np.random.randint(2, size= (n, n))

	hit_algo = HITS(filename= filename)

	# print(f"L : {L}")
	print('-'*50)
	print('a: ', np.argmax(hit_algo.get_scores()[1]))
	print('h: ', np.argmax(hit_algo.get_scores()[0]))
	print('a: ', hit_algo.get_scores()[1][427])
	print('h: ', hit_algo.get_scores()[0][194])

if __name__ == '__main__':
	main()

