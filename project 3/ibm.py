import numpy as np 
import itertools

filename = 'data/ibm.data'

with open(filename, 'r') as f:
	data = f.readlines()
	trans_dict = dict()

	for line in data:
		line = line.split()
		tran = line[0]
		item = line[-1]

		if tran not in trans_dict.keys():
			trans_dict[tran] = [item]
		else:
			trans_dict[tran].append(item)

# print(trans_dict)
log = list()
log2 = list()
modes = ['direct', 'bidirect']

for mode in modes:
	print(f'mode: {mode}')
	with open(f'data/ibm_graph_{mode}.txt', 'w') as f:
		if mode == 'direct':
			for items in trans_dict.values():
				combinations = itertools.combinations(items, 2)
				for combination in combinations:
					if combination not in log:
						node_in = combination[0]
						node_out = combination[1]
						row = node_in+','+node_out
						f.write(row+ '\n')
						log.append(combination)
		else:
			for items in trans_dict.values():
				combinations = itertools.combinations(items, 2)
				for combination in combinations:
					node_in = combination[0]
					node_out = combination[1]
					row1 = node_in+','+node_out
					row2 = node_out+','+node_in
					for row in [row1, row2]:
						if row not in log2:
							f.write(row+ '\n')
							log2.append(row)



