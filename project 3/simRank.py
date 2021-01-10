'''
如果两个用户相似，则与这两个用户相关联的物品也类似；
如果两个物品类似，则与这两个物品相关联的用户也类似
如果我们的二部图是 G(V, E) ，其中V是节点集合，E是边集合
C : 阻尼係數 (當sim(a,b) = C*sim(A,A) = C，防止sim(a,b)= 1情況。)
'''
import numpy as np 
import time 

class SimRank():
	def __init__(self, filename, C= 0.8):

		with open(file=filename) as f:

			self.data = [ tuple(line.strip().split(',')) for line in f.readlines()]

		self.V = list(sorted(set([nodes[0] for nodes in self.data]), key= lambda x: int(x)))
		self.E = list(sorted(set([nodes[1] for nodes in self.data]), key= lambda x: int(x)))
		self.G = np.zeros(shape= (len(self.V), len(self.E)))
		self.C = C

		for node_tuple in self.data:

			v = node_tuple[0]
			e = node_tuple[1]

			v_idx = self.V.index(v)
			e_idx = self.E.index(e)

			self.G[v_idx, e_idx] += 1

		print(f'V: {self.V}')
		print('-'*50)
		print(f'E: {self.E}')
		print('-'*50)
		print(f'graph : \n{self.G}')
		print('-'*50)

		self.v_SimRank = np.identity(len(self.V)) # 初始 S = I
		self.e_SimRank = np.identity(len(self.E))

	def V_SimRank(self, v1, v2):

		if v1 == v2:
			return 1 

		else :

			Rank_sum = 0
			v1_idx = self.V.index(v1)
			v2_idx = self.V.index(v2)

			penalty = self.C / (self.G[v1_idx].sum(axis= 0) * self.G[v2_idx].sum(axis= 0))
			# print(f'penalty: {penalty}')
			# print('-'*50)

			for i in [ i for i, e in enumerate(self.G[v1_idx]) if e != 0]:
				for j in [ j for j, e in enumerate(self.G[v2_idx]) if e != 0]:
					Rank_sum += self.e_SimRank[i, j]

		return penalty * Rank_sum

	def E_SimRank(self, e1, e2):

		if e1 == e2:
			return 1 

		else :

			Rank_sum = 0
			e1_idx = self.E.index(e1)
			e2_idx = self.E.index(e2)

			penalty = self.C / (self.G.transpose()[e1_idx].sum(axis= 0) * self.G.transpose()[e2_idx].sum(axis= 0))
			# print(f'penalty: {penalty}')
			# print('-'*50)

			for i in [ i for i, v in enumerate(self.G.transpose()[e1_idx]) if v != 0]:
				for j in [ j for j, v in enumerate(self.G.transpose()[e2_idx]) if v != 0]:
					Rank_sum += self.v_SimRank[i, j]

		return penalty * Rank_sum


	def Compute_SimRank(self, epochs):

		for _ in range(epochs):

			new_v_SimRank = np.identity(len(self.v_SimRank))
			new_e_SimRank = np.identity(len(self.e_SimRank))

			for vi in self.V:  
				for vj in self.V: 
					i = self.V.index(vi)
					j = self.V.index(vj)
					# print(self.V_SimRank(v1= vi, v2= vj))
					new_v_SimRank[i, j] = self.V_SimRank(v1= vi, v2= vj)

			for ei in self.E:  
				for ej in self.E: 
					i = self.E.index(ei)
					j = self.E.index(ej)

					new_e_SimRank[i, j] = self.E_SimRank(e1= ei, e2= ej)

			self.v_SimRank = new_v_SimRank
			self.e_SimRank = new_e_SimRank

		# print(f'SimRank: {self.v_SimRank}')
		return self.v_SimRank

def main():

	filename = 'graph_4.txt'
	Ranker = SimRank(filename= filename, C= 0.8)

	print('-'*50)
	print('Rank:\n\n', Ranker.Compute_SimRank(epochs= 5).round(2))
	print('-'*50)

if __name__ == '__main__':
	main()





