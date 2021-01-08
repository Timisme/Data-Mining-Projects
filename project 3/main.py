import numpy as np   
from hits import HITS
from pagerank import get_n_M, PowerMethod
from simRank import SimRank
from SimRank_matrix import SimRank_matrix

for i in range(1, 7):

	filename= f'graph_{i}.txt'

	print('-'*50)
	n, M= get_n_M(filename= filename)
	PR= PowerMethod(n=n, M= M)

	print('-'*50)
	hit_algo = HITS(filename= filename)
	h = hit_algo.get_scores()[0]
	a = hit_algo.get_scores()[1]
	print(h)
	print('-'*50)

	if i < 5:
		Ranker = SimRank(filename= filename, C= 0.8)
		SR = Ranker.Compute_SimRank(epochs= 5).round(5)
		# print('Rank:\n\n', SR)
		# print('-'*50)

	else:

		Ranker_matrix = SimRank_matrix(filename= filename)
		print('-'*50)
		print(f'Rank:\n\n{Ranker_matrix.get_SimRank().round(2)}')
		SR = Ranker_matrix.get_SimRank().round(5)

	# with open(f'outputs/graph_{i}_PageRank.txt', 'w') as f:
	# 		f.write(f'PageRank for graph {i}:\n{PR}')

	# with open(f'outputs/graph_{i}_HITS_hub.txt', 'w') as f:
	# 		f.write(f'hubs for graph {i}:\n{h}')

	# with open(f'outputs/graph_{i}_HITS_authority.txt', 'w') as f:
	# 		f.write(f'authorities for graph {i}:\n{a}')
			
	# with open(f'outputs/graph_{i}_SimRank.txt', 'w') as f:
	# 		for row in SR:
	# 			f.write(f'SimRank_maix for graph {i}:\n{row}')

	np.savetxt(f'outputs/graph_{i}_PageRank.txt', PR, fmt="%s")
	np.savetxt(f'outputs/graph_{i}_HITS_hub.txt', h, fmt="%s")
	np.savetxt(f'outputs/graph_{i}_HITS_authority.txt', a, fmt="%s")
	np.savetxt(f'outputs/graph_{i}_SimRank.txt', SR, fmt="%s")