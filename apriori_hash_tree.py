import numpy as np
import csv
import pandas as pd
import itertools
import time
from hash_tree import HNode, HTree

file = 'data\\BreadBasket_list.csv'
file_freq = 'data\\Bread_freq_HashTree.csv'
file_rule = 'data\\Bread_rule_HashTree.csv'

start_time = time.time()
with open(file,newline='') as file:
	contents = csv.reader(file)
	transactions  = [row for row in contents if row]
end_time = time.time()

print('Data Loading takes {:.3f} seconds'.format(end_time-start_time))

transactions = [set(transaction) for transaction in transactions]

def get_L1(_transactions, min_support):
	candidate_items = {} #stores support for each item
	for transaction in _transactions:
		for item in transaction:
			candidate_items[item] = candidate_items.get(item,0) + 1 
	L1_support = [] 
	L1_list = []
	for item in candidate_items:
		if candidate_items[item] >= min_support:
			L1_support.append(([item],candidate_items[item]))
			L1_list.append([item])
	return L1_support, L1_list

def get_k_subsets(datasets, length):
	subsets = []
	for itemset in datasets:
		subsets.extend([sorted(itemset) for itemset in list(itertools.combinations(itemset,length))])
		# print('C from datasets',list(itertools.combinations(itemset,length)))
		# print('sorted c', [sorted(itemset) for itemset in list(itertools.combinations(itemset,length))])
	subsets = [val for val in subsets]
	return subsets

def subset_generation(ck_data,l):
	return list(map(list,set(itertools.combinations(ck_data,l))))

#apriori generate function to generate ck 
# lK = [[2,3,4],[2,4,4]] e.q
# L2,3
def ck_generator(Lk,k):
	ck_set = []
	#join Ck=(Lk-1 self join Lk-1)
	lenlk = len(Lk) 
	for i in range(lenlk):
		for j in range(i+1,lenlk):
			L1 = list(Lk[i])[:k - 2] #該Lk倒數第一前的元素
			L2 = list(Lk[j])[:k - 2]
			if L1 == L2:
				ck_set.append(sorted(list(set(Lk[i]).union(set(Lk[j]))))) # set a | set b -> 聯集
	return ck_set 

def generate_hash_tree(candidate_itemsets, max_leaf_cnt, max_child_cnt):

	# This function generates hash tree of itemsets with each node having no more than child_max_length
	# childs and each leaf node having no more than max_leaf_length.
	# htree = HTree(max_child_cnt, max_leaf_cnt)
	htree = HTree(max_leaf_cnt, max_child_cnt)
	for itemset in candidate_itemsets:
		# add this itemset to hashtree
		htree.insert(itemset)
	return htree

def apriori(_transactions,min_support,max_leaf_cnt,max_child_cnt, freq_patterns, freq_patterns_support): 
	k=2 
	L1_dict, L1_list = get_L1(_transactions, min_support)
	freq_patterns.append(L1_list)
	freq_patterns_support.append(L1_dict)
	C2_candidates = ck_generator(L1_list, 2)
	print('C2 oK')
	# print('C2:\n', C2_candidates)
	h_tree = generate_hash_tree(C2_candidates,max_leaf_cnt,max_child_cnt)
	k_subsets = get_k_subsets(_transactions,k)
	# print('c2 from trans:\n',k_subsets)
	for subset in k_subsets:
		h_tree.add_support(subset)
	L2 = [items[0] for items in h_tree.get_frequent_itemsets(min_support)]
	if L2 == []:
		print('L2 is empty')
		return 
	print('L2 oK')
	# print([items for items in h_tree.get_frequent_itemsets(min_support)])
	freq_patterns.append(L2)
	freq_patterns_support.append([items for items in h_tree.get_frequent_itemsets(min_support)])
	k += 1 # k= 3
	
	while(len(freq_patterns[k-2])>0):
		Ck_candidates = ck_generator(freq_patterns[k-2], k)
		if Ck_candidates == []:
			break
		print('C%d ok'%k)
		# print(Ck_candidates)
		h_tree = generate_hash_tree(Ck_candidates,max_child_cnt,max_child_cnt)
		k_subsets = get_k_subsets(_transactions,k)
		
		for subset in k_subsets:
			h_tree.add_support(subset)
		Lk = [items[0] for items in h_tree.get_frequent_itemsets(min_support)]
		if Lk == []:
			break 
		print('L%d ok'%k)
		# print([items for items in h_tree.get_frequent_itemsets(min_support)])
		freq_patterns.append(Lk)
		freq_patterns_support.append([items for items in h_tree.get_frequent_itemsets(min_support)])
		k += 1
	return 



def rule_generator(freq_itemset, _candidate_sets, init_num, min_confidence, rules_list): #['4','3','2','1'] 
	if len(freq_itemset) == 1 :
		return 
	elif init_num > len(freq_itemset):
		return 
	elif len(freq_itemset) > 1:
		if init_num == 1 : #第一層
			# print('Each freq pattern Rule Generating...')
			_candidate_sets = [frozenset(subset) for subset in list(itertools.combinations(freq_itemset,len(freq_itemset)-1))] #[{'4', '2', '3'}, {'4', '3', '1'}, {'4', '2', '1'}, {'1', '2', '3'}]
			_candidate_sets = list(dict.fromkeys(_candidate_sets))

			init_num += 1 
			rule_generator(freq_itemset, _candidate_sets, init_num, min_confidence, rules_list)
		else : 
			pruned_subsets = [(set(subset),set(freq_itemset)-set(subset),round(freq_pattern_dict[frozenset(freq_itemset)] / freq_pattern_dict[frozenset(subset)],3)) for subset in _candidate_sets if (freq_pattern_dict[frozenset(freq_itemset)] / freq_pattern_dict[frozenset(subset)]) >= min_confidence]
			if pruned_subsets != []:
				rules_list.append(pruned_subsets)
				candidate_sets = []
				for i in range(len(pruned_subsets)-1):
					for j in range(i+1, len(pruned_subsets)):
						if pruned_subsets[i][0].intersection(pruned_subsets[j][0]) != set():
						 candidate_sets.append(pruned_subsets[i][0].intersection(pruned_subsets[j][0]))
						 candidate_sets = [frozenset(candidate) for candidate in candidate_sets]
						 candidate_sets = list(dict.fromkeys(candidate_sets))
				if candidate_sets == []:
					return
				else: 
					init_num += 1 
					rule_generator(freq_itemset, candidate_sets,init_num, min_confidence, rules_list)
			else:
				return


start_time = time.time()
frequent_items_dict = {}
freq_patterns = []
freq_patterns_support = []
min_sup = 10
max_leaf_cnt = 20
max_child_cnt = 20
apriori(_transactions = transactions,min_support= min_sup,max_leaf_cnt= max_leaf_cnt, max_child_cnt= max_child_cnt, freq_patterns = freq_patterns, freq_patterns_support= freq_patterns_support)
end_time = time.time()

k_occurence = {}

for Lk_list in freq_patterns:
	for lk in Lk_list:
		k_occurence[len(lk)] = k_occurence.get(len(lk),0)+1 

print('k occrence:\n',k_occurence)
print('apriori hash tree mining takes {:.3f} seconds'.format(end_time - start_time))

flattened_patterns = [val for freq in freq_patterns for val in freq ]
flattened_supports = [val for freq in freq_patterns_support for val in freq]
freq_pattern_dict = {}
for freq_pattern in flattened_supports:
		freq_pattern_dict[frozenset(freq_pattern[0])] = freq_pattern_dict.get(frozenset(freq_pattern[0]),0) + freq_pattern[1]

with open(file_freq,'w') as file:
 	file_writer = csv.writer(file, delimiter=',')
 	file_writer.writerow(['min_support:{}'.format(min_sup),'max leaf:{}'.format(max_leaf_cnt)])
 	file_writer.writerow(['Frequent Pattern','Support'])
 	freq_dict_sorted = {key:value for key,value in sorted(freq_pattern_dict.items(), key = lambda item: item[1], reverse= True)}
 	for freq_pattern, support in freq_dict_sorted.items():
 		file_writer.writerow([set(freq_pattern),support])
'''
Rule Generation 
'''
min_conf =0.5
rules_list = []
for _freq_pattern in flattened_patterns:
	rule_generator(freq_itemset= _freq_pattern, _candidate_sets= set([]), init_num= 1, min_confidence= min_conf, rules_list = rules_list)


flattened_rules = [rule for k_rule in rules_list for rule in k_rule] 
final_rules = sorted(flattened_rules, key = lambda x: x[2], reverse = True)

# final_rules = []
# for rule in sorted_rules:
# 	if rule not in final_rules:
# 		final_rules.append(rule)

print('# of rules:',len(final_rules))
print('writing to csv...')
with open(file_rule,'w') as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=',')
	csv_writer.writerow(['Min Support:{}'.format(min_sup),'Min Confidence:{}'.format(min_conf)])
	csv_writer.writerow(['antecedents','consequents','Confidence'])
	for rule in final_rules:
		csv_writer.writerow(rule)
print('writing done!')