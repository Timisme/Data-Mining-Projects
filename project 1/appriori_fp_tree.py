import numpy as np
from collections import OrderedDict  
import pandas as pd
import time
import itertools
import csv


IBM_columns = ['customer_id', 'transaction_id', 'item_id']
df = pd.read_table("IBM.data", sep="\s+",names=IBM_columns,index_col='transaction_id')

start_time = time.time()
transactions = []
for transaction_id in list(df.index.unique()):
    if type(df.loc[transaction_id]['item_id']) == np.int64:
        transactions.append([df.loc[transaction_id]['item_id']])
    else:
        transactions.append(df.loc[transaction_id]['item_id'].tolist())
end_time = time.time()
print('Data Reading takes {:3f} seconds'.format(end_time - start_time))

#transactions = [['3','4','2'],['2','5','4'],['4','1','6'],['5','6','7']]

#transactions = [['HotDogs', 'Buns', 'Ketchup'],['HotDogs', 'Buns'],['HotDogs', 'Coke', 'Chips'],['Chips', 'Coke'],['Chips', 'Ketchup'],['HotDogs', 'Coke', 'Chips']]

def get_transaction_dict(transactions):
	transactions_dict = OrderedDict()
	for transaction in transactions:
		transactions_dict[frozenset(transaction)] = transactions_dict.get(frozenset(transaction),0) + 1 
	return transactions_dict

transactions_dict = get_transaction_dict(transactions)

#print('transaction_dict:',transactions_dict)

def get_fp_tree(_transactions_dict, min_support):
	
	_headerTable = {}
	
	for transaction in _transactions_dict.keys():
		'''針對指定transaction的某item'''
		for item in transaction: 
			'''_headertable[item] 儲存item的support'''
			_headerTable[item] = _headerTable.get(item,0) + _transactions_dict[transaction]

	root_node = treenode('Root',1,None)

	for key in list(_headerTable): # keys returns an iterator instead of a list. 
			if _headerTable[key] < min_support:
				'''刪除不符合min_support的item'''
				del _headerTable[key]

	#freq_items_dict_ 儲存freq item的support
	freq_items_dict_ = _headerTable.copy() 
	
	freq_items = set(_headerTable.keys()) #frequent L1

	if len(freq_items) != 0:
		for key in _headerTable.keys():
			_headerTable[key] = [_headerTable[key],None] #每個key對應的值(support)中增加一个“None”，利後續存相似元素準 #
		
	for transaction, count in _transactions_dict.items(): #每筆trans 及 其出現的次數(之後trans會是條件基 #
		freq_item_dict = {}
		for item in transaction:
			if item in freq_items:
				freq_item_dict[item] = _headerTable[item][0] #針對每筆trans做排序，建立為該trans的dict以儲存該item的suppor #
		sorted_transaction = [x[0] for x in sorted(freq_item_dict.items(),key = lambda x : x[1],reverse=True)]
		# 將 sorted_transaction 加入 fp_tree 中
		insert_to_tree(sorted_transaction, root_node, _headerTable, count)
	return root_node, _headerTable, freq_items_dict_

def insert_to_tree(_sorted_transaction, _root_node, Header_table, count):
	if len(_sorted_transaction) == 0:
		return 

	if _sorted_transaction[0] in _root_node.children: # the chidren is a dict that stores the item_name as the key 
		_root_node.children[_sorted_transaction[0]].add_support(count)
	else: 
		_root_node.children[_sorted_transaction[0]] = treenode(nodeName= _sorted_transaction[0], support= count, parentNode= _root_node)
		if Header_table[_sorted_transaction[0]][1] == None:
			Header_table[_sorted_transaction[0]][1] = _root_node.children[_sorted_transaction[0]]
		else: # 該item 目前有指向的node
			update_header(pointed_node= Header_table[_sorted_transaction[0]][1], linked_node= _root_node.children[_sorted_transaction[0]])
	if len(_sorted_transaction) > 1 :
		insert_to_tree(_sorted_transaction[1::], _root_node.children[_sorted_transaction[0]], Header_table, count)

def update_header(pointed_node, linked_node):
	while(pointed_node.nodelink != None):
		pointed_node = pointed_node.nodelink # 指向node之連結node#
	pointed_node.nodelink = linked_node #指向node之連結node和目標node連結形成連結鍊#


class treenode:
	def __init__(self, nodeName, support, parentNode):
		self.name = nodeName # = item name
		self.count = support
		self.nodelink = None
		self.parent = parentNode
		self.children = {} # key stores the item name, value is the next node object
	
	def add_support(self, support):
		self.count += support 

	def showtree(self, index = 1):
		print('  '*index, self.name, ' ', self.count)
		for child in self.children.values():
			child.showtree(index + 1)


def get_single_prefix_path(single_node, prefix_path): #從leaf node向上找出單條條件基, 將其 prefix_path(list) 更新為條件基#
	if single_node.parent != None:
		prefix_path.append(single_node.name)
		get_single_prefix_path(single_node.parent, prefix_path)

def find_all_prefixPath(item_node): #針對所有該 K1 item 鏈結之 nodes 各向上找 single prefix path，output為dict(key為條件基、value為條件基support)#
	conditional_patterns_dict = {}
	while item_node != None:
		prefixPath = []
		get_single_prefix_path(item_node, prefixPath)
		if len(prefixPath) > 1: #有條件基(不包含自己)
			conditional_patterns_dict[frozenset(prefixPath[1:])] = item_node.count
		item_node = item_node.nodelink # 更新為下一個鏈結點
	return conditional_patterns_dict

def mineTree(TreeClass, headerTable_dict, min_support, prefixPath, freq_item_list, freq_pattern_dict):
	item_sorted = [x[0] for x in sorted(headerTable_dict.items(),key= lambda x:x[1][0],reverse = False)] #將item依照其support降冪排序#
	#print('item sorted',item_sorted)
	for item in item_sorted : 
		condPatternBases_dict = find_all_prefixPath(headerTable_dict[item][1]) #針對該item找出其所有條件基#
		#print('item',item,'has condpatternbases',condPatternBases_dict)
		new_freq_set = prefixPath.copy()
		new_freq_set.add(item)
		#print('prefix path:',frozenset(new_freq_set))
		#print('item counts:',headerTable_dict[item][0])
		freq_pattern_dict[frozenset(new_freq_set)] = freq_pattern_dict.get(frozenset(new_freq_set),0)+headerTable_dict[item][0]
		freq_item_list.append(new_freq_set)
		condTree, condHeader, _ = get_fp_tree(condPatternBases_dict,min_support) #利用該item的所有條件基建立fp tree#
		if condHeader != None:
			#print('condHeader:',condHeader,'\n')
			mineTree(condTree, condHeader, min_support, new_freq_set,freq_item_list,freq_pattern_dict)
	return freq_item_list


start_time = time.time()
min_sup = 10
Fp_tree, HeaderTable, freq_item_dict = get_fp_tree(transactions_dict,min_support = min_sup)

freq_patterns = []
freq_pattern_dict = {}
mineTree(Fp_tree, HeaderTable,min_sup, set([]),freq_patterns,freq_pattern_dict)
end_time = time.time()

occurence_dict = {}

for pattern in freq_patterns:
	occurence_dict[len(pattern)] = occurence_dict.get(len(pattern),0) + 1

print('Lk occurence:\n',occurence_dict)
#print('HeaderTable:\n',HeaderTable)
print('mining process takes {:.3f} seconds'.format(end_time-start_time))
#print('frequent patterns', freq_patterns)
#print('frequent pattern dict\n',freq_pattern_dict)

def rule_generator(freq_itemset, _candidate_sets, init_num, min_confidence, rules_list): #['4','3','2','1'] 
	
	if len(freq_itemset) == 1 :
		return 
	elif init_num > len(freq_itemset):
		return 
	elif len(freq_itemset) > 1:
		if init_num == 1 : #第一層
			_candidate_sets = [set(subset) for subset in list(itertools.combinations(freq_itemset,len(freq_itemset)-1))] #[{'4', '2', '3'}, {'4', '3', '1'}, {'4', '2', '1'}, {'1', '2', '3'}]
			#print('candidate_sets for init = 1\n',_candidate_sets)
			init_num += 1 
			rule_generator(freq_itemset, _candidate_sets, init_num, min_confidence, rules_list)
		else : 
			pruned_subsets = [(set(subset),set(freq_itemset)-set(subset),round(freq_pattern_dict[frozenset(freq_itemset)] / freq_pattern_dict[frozenset(subset)],3)) for subset in _candidate_sets if (freq_pattern_dict[frozenset(freq_itemset)] / freq_pattern_dict[frozenset(subset)]) >= min_confidence]
			# [('4', '3', '1'), ('4', '2', '1'), ('3', '2', '1')]
			if pruned_subsets != []:
				rules_list.append(pruned_subsets)
				#print('pruned_subsets:\n',pruned_subsets)
				candidate_sets = []
				for i in range(len(pruned_subsets)-1):
					for j in range(i+1, len(pruned_subsets)):
						if pruned_subsets[i][0].intersection(pruned_subsets[j][0]) != set():
							##print('k-1 subset:',(pruned_subsets[i][0].intersection(pruned_subsets[j][0]), pruned_subsets[i][1].union(pruned_subsets[j][1])))
						 candidate_sets.append(pruned_subsets[i][0].intersection(pruned_subsets[j][0]))
				if candidate_sets == []:
					return
				else: 
					#print('k{} candidate sets:\n'.format(init_num), candidate_sets)
					init_num += 1 
					rule_generator(freq_itemset, candidate_sets,init_num, min_confidence, rules_list)
			else:
				return

start_time = time.time()
rules_list = []
for freq_pattern in freq_patterns:
	rules = []
	rule_generator(list(freq_pattern),set(),1,0.6,rules)
	if rules != []:
		rules_list.append(rules)
		# print('rules:\n',rules)
end_time = time.time()
print('rule generating takes {:.3f} seconds'.format(end_time-start_time))
flattened_rules = [val for rule1 in rules_list for rule2 in rule1 for val in rule2]
ordered_rules = sorted(flattened_rules,key = lambda x : x[2],reverse = True)
# print('Rule Generated:\n',rules_list)
# print('Flattened Rule Generated:\n',flattened_rules)
print('# of Rules:',len(flattened_rules))
with open('rules.csv','w') as csv_file:
	# fieldnames = ['item','associated itemset','confidence']
	csv_writer = csv.writer(csv_file, delimiter='\t')
	# csv_writer.writeheader()
	for rule in ordered_rules:
		csv_writer.writerow(rule)



# length = 0 
# for rule in rules_list:
# 	for rule1 in rule:
# 		print(rule1)
# 		length += len(rule1)
#print('# of Rules:',length)
