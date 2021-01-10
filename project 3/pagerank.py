import numpy as np

# Stochastic adjacency matrix M
# page i has di out-links

def get_n_M(filename):

	V = set()
	out_degree = dict()

	with open(filename) as f:
		data = [ line.strip().split(',') for line in f.readlines()]
		for node_tuple in data:
			i = node_tuple[0]
			j = node_tuple[1]

			V.add(i)
			V.add(j)

			out_degree[i] = out_degree.get(i, 0) + 1

	V = sorted(V, key= lambda x: int(x))
	n = len(V)
	M = np.zeros([n,n])

	with open(filename) as f:
		data = [ line.strip().split(',') for line in f.readlines()]
		for node_tuple in data:
			i_idx = V.index(node_tuple[0])
			j_idx = V.index(node_tuple[1])

			M[j_idx, i_idx] = 1/out_degree[node_tuple[0]]
	
	return n, M, V

def PowerMethod(n, M, d= 0.85, epsilon= 1e-15):
	# damping_matrix = [[ damping*(1/n) for i in range(n)] for j in range(n)]
	# A = (1-damping)*M + damping_matrix
	# r = [[1/n] for i in range(n)]
	# for i in range(iteration):
	# 	print('iter', i)
	# 	r = np.dot(A, r) 

	iter_ = 0
	e = [1/n for _ in range(n)]
	# print(f'e: {e}')
	# R = [(1-d)*i for i in e]
	R = e

	while True:
		iter_+= 1

		old_R = R
		R = d * np.dot(M, old_R) + [(1-d)*i for i in e]

		if (abs(R - old_R) < epsilon).all():
			print(f'final iter {iter_}')
			break 
	return R.round(5)

if __name__ == '__main__':
	
	modes = ['direct', 'bidirect']

	for mode in modes:
		file = f'data/ibm_graph_{mode}.txt'

		n, M, V = get_n_M(filename= file)
		print(n)
		print(M)
		print('-'*50)
		# print(n, M)

		r = PowerMethod(n= n, M= M, d= 0.85)
		# print(f'r:\n{r}')

		rank_r = [sorted(r).index(x) for x in r]
		# print('V:', V)
		# print(f'rank_r:\n{rank_r}')

		# print(f'max_rank_item: {V[np.argmax(rank_r)]}')
		# print(f'node order by pagerank:\n{[V[rank_r.index(x)] for x in sorted(rank_r, reverse= True)][:10]}')
		np.savetxt(f'data/ibm_{mode}_pagerank.txt', [V[rank_r.index(x)] for x in sorted(rank_r, reverse= True)][:10], fmt="%s")


	file = f'graph_1.txt'

	n, M, V = get_n_M(filename= file)
	print(n)
	print(M)
	print('-'*50)
	# print(n, M)

	r = PowerMethod(n= n, M= M, d= 0.85)
	print(f'r:\n{r}')