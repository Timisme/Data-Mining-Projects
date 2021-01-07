import numpy as np  

class SimRank():
	def __init__(self, filename, epoch= 5):

		self.I_dict = dict()
		self.O_dict = dict()

		with open(file=filename) as f:

			data = [ tuple(line.strip().split(',')) for line in f.readlines()]

		for node_tuple in data:

			in_neighbor = node_tuple[0]
			out_neighbor = node_tuple[1]
			# print(in_neighbor, out_neighbor)
			if out_neighbor in self.I_dict.keys():
				self.I_dict[out_neighbor].append(in_neighbor)
			else:
				self.I_dict[out_neighbor] = [in_neighbor]

			if in_neighbor in self.O_dict.keys():
				self.O_dict[in_neighbor].append(out_neighbor)
			else:
				self.O_dict[in_neighbor] = [out_neighbor]

		print(f'I dict: {self.I_dict}')
		print('-'*50)
		in_neighbors = [i for Is in list(self.I_dict.values()) for i in Is]
		
		nodes_list = list(sorted(set(list(self.I_dict.keys()) + in_neighbors)))
		N = len(nodes_list)
		print(f'N: {N}')
		print(f'nodes_list: {nodes_list}')
		print('-'*50)

		self.I = np.zeros(shape= (N, N)) # In-Neighbor-Matrix
		self.Q = np.zeros((N,N))
		# print(f'I: {I}')
		# print('-'*50)

		for out_neighbor in self.I_dict.keys():

			i_idx = nodes_list.index(out_neighbor)

			for in_neighbor in self.I_dict[out_neighbor]:

				j_idx = nodes_list.index(in_neighbor)

				self.I[i_idx, j_idx] += 1

		for in_neighbor in self.O_dict.keys():
			i_idx = nodes_list.index(in_neighbor)
			n = len(self.O_dict[in_neighbor])

			for out_neighbor in self.O_dict[in_neighbor]:
				j_idx = nodes_list.index(out_neighbor)
				self.Q[i_idx, j_idx] = 1/n

		print(f'I: {self.I}\n')
		print(f'Q: {self.Q}')

	def get_SimRank(self, C= 0.8, epsilon= 1e-4, epochs= 100):

		I = np.identity(self.Q.shape[0])

		S = (1-C) * I # init

		for _ in range(epochs):

			old_S = S 
			S = C*np.dot(np.dot(self.Q.transpose(), old_S), self.Q) + (1-C) * I 

		return S


	

	# def E_SimRank(self, e1, e2):

def main():

	filename = 'graph_3.txt'
	Ranker = SimRank(filename= filename)
	print('-'*50)
	print(f'Rank:\n\n{Ranker.get_SimRank()}')

	# print(Ranker.V_SimRank(v1= '1', v2= '2'))


if __name__ == '__main__':
	main()