'''
如果两个用户相似，则与这两个用户相关联的物品也类似；
如果两个物品类似，则与这两个物品相关联的用户也类似
如果我们的二部图是 G(V, E) ，其中V是节点集合，E是边集合
'''
import numpy as np 

filename = 'graph_1.txt'


class SimRank():
	def __init__(self, filename, epoch= 5):

		with open(file=filename) as f:

			self.data = [ tuple(line.split(',')) for line in f.readlines()]

		self.V = list(set([nodes[0] for nodes in self.data]))
		self.E = list(set([nodes[1] for nodes in self.data]))

		self.G = np.zeros(shape= (len(self.V), len(self.E)))

		for node_tuple in self.data:

			v = node_tuple[0]
			e = node_tuple[1]

			v_idx = self.V.index(v)
			e_idx = self.E.index(e)

			# print(v,e)
			# print(v_idx, e_idx)
			# print('-'*50)

			self.G[v_idx, e_idx] += 1

		print(f'graph : \n{self.G}')
		print('-'*50)

		self.I_v = np.identity(len(self.V)) # 自己和自己SimRank = 1
		self.I_e = np.identity(len(self.E))

	def V_SimRank(self, v1, v2):

		if v1 == v2:
			return 1 

		else :

			Rank_sum = 0
			v1_idx = self.V.index(v1)
			v2_idx = self.V.index(v2)

			penalty = 1/ (self.G[v1_idx].sum(axis= 0) * self.G[v2_idx].sum(axis= 0))
			print(f'penalty: {penalty}')
			print('-'*50)

			for e_i in [ i for i, e in enumerate(self.G[v1_idx]) if e != 0]:
				for e_j in [ j for j, e in enumerate(self.G[v2_idx]) if e != 0]:
					if  e_i == e_j:
						Rank_sum += 1
		return penalty * Rank_sum


	# def E_SimRank(self, e1, e2):

def main():

	Ranker = SimRank(filename= filename)

	print(Ranker.V_SimRank(v1= '1', v2= '2'))


if __name__ == '__main__':
	main()





