import numpy as np

# Stochastic adjacency matrix M
# page i has di out-links

def get_n_M(filename):

	V = set()
	out_degree = dict()

	with open(filename) as f:
		for line in f:
			[node, node_pnt2] = line.split(',')

			i = int(node)
			j = int(node_pnt2)

			V.add(i)
			V.add(j)

			out_degree[i] = out_degree.get(i, 0) + 1

	V = sorted(V)
	n = len(V)
	M = np.zeros([n,n])

	with open(filename) as f:
		for line in f:
			[node, node_pnt2] = line.split(',')
			i = int(node)
			j = int(node_pnt2)

			M[j-1, i-1] = 1/out_degree[i]
	
	return n, M

def PowerMethod(iteration, n, M, damping= 0.15):
	damping_matrix = [[ damping*(1/n) for i in range(n)] for j in range(n)]
	A = (1-damping)*M + damping_matrix
	r = [[1/n] for i in range(n)]
	for i in range(iteration):
		print('iter', i)
		r = np.dot(A, r) 
	return r 

if __name__ == '__main__':
	
	file = 'graph_3.txt'

	n, M = get_n_M(filename= file)

	print(n, M)

	r = PowerMethod(iteration= 100, n= n, M= M)
	print(r)