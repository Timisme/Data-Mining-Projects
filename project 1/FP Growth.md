# FP Growth 
```python=
def get_transaction_dict(transactions):
	transactions_dict = {}
	for transaction in transactions:
		transactions_dict[frozenset(transaction)] = transactions_dict.get(frozenset(transaction),0) + 1 
	return transactions_dict

transactions_dict = get_transaction_dict(transactions)
```
建立字典，將每筆itemset的frosenset作為key, value為該itemset在資料集出現的次數

```python=
class treenode:
	def __init__(self, nodeName, support, parentNode):
		self.name = nodeName # = item name
		self.count = support
		self.nodelink = None
		self.parent = parentNode
		self.children = {} # key stores the item name, value is the next node object
	
	def add_support(self, support):
		self.count += support 

```
定義fp tree中結點的treenode物件（class），每個node都有自己的名稱、support、鏈結點、父結點、子結點，其中add support function可對該物件support作更新。

```python=
def get_fp_tree(_transactions_dict, min_support): #_transactions_dict : {'frozenset()':int}
	
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
				del(_headerTable[key])

	#freq_items_dict_ 儲存freq item的support
	freq_items_dict_ = _headerTable.copy() 
	freq_items = set(_headerTable.keys()) #frequent L1
```
這個步驟為建立FP Tree，適用於第一次資料庫掃描後的fp tree與後續條件基(Conditional pattern base)的建立。函數給入儲存itemsets的dictionary以及minimum support。而函數中會建立該itemsets的header table，並移除不符合Min support的item
```python=
	if len(freq_items) != 0:
		for key in _headerTable.keys():
			_headerTable[key] = [_headerTable[key],None] #每個key對應的值(support)中增加一个“None”，利後續存相似元素 #
		
	for transaction, count in _transactions_dict.items(): #每筆trans 及 其出現的次數(之後trans會是條件基 #
		freq_item_dict = {}
		for item in transaction:
			if item in freq_items:
				freq_item_dict[item] = _headerTable[item][0] #針對每筆trans做排序，建立為該trans的dict以儲存該item的suppor #
		if len(freq_item_dict) > 0:
			sorted_transaction = [x[0] for x in sorted(freq_item_dict.items(),key = lambda x : (x[1],x[0]),reverse=True)]
			# 將 sorted_transaction 加入 fp_tree 中
			insert_to_tree(sorted_transaction, root_node, _headerTable, count)
	return root_node, _headerTable, freq_items_dict_
```
這個步驟延續get_fp_tree函數內容。首先將headertable額外儲存每個item在FP tree的相同item鍵結。後續將itemsets中每筆itemset利用疊代的方式插入至該fp tree中，過程中將會更新每個item的support以及其鏈結點，整體建立該itemsets的FP tree。
```python=
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
```
此步驟僅是建立fp tree過程中會利用的function，其中Insert_to_tree將給入itemset依照該itemset中的item依順序及規定的插入tree中，而update_header為更新header table中每個item儲存在tree中的鍊結點。

```python=
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
```

這段函數是針對transaction中的各個item在fp tree中的所有節點(包含連結點)找出該item的所有條件基（conditional pattern path)。

```python=
def mineTree(TreeClass, headerTable_dict, min_support, prefixPath, freq_item_list, freq_pattern_dict):
	item_sorted = [x[0] for x in sorted(headerTable_dict.items(),key= lambda x:x[1][0],reverse = False)] #將item依照其support降冪排序#
	for item in item_sorted : 
		condPatternBases_dict = find_all_prefixPath(headerTable_dict[item][1]) #針對該item找出其所有條件基#
		new_freq_set = prefixPath.copy()
		new_freq_set.add(item)
		freq_pattern_dict[frozenset(new_freq_set)] = freq_pattern_dict.get(frozenset(new_freq_set),0)+headerTable_dict[item][0]
		freq_item_list.append(new_freq_set)
		condTree, condHeader, _ = get_fp_tree(condPatternBases_dict,min_support) #利用該item的所有條件基建立fp tree
		if condHeader != None:
			mineTree(condTree, condHeader, min_support, new_freq_set,freq_item_list,freq_pattern_dict)
	return freq_item_list
```

此段程式碼主要功能是利用 header table 針對各個找出 fp tree 中的所有條件基，而對於每個item，利用疊代的方式利用條件基中的 conditional header table 建立條件基樹(conditional fp tree)，以此方式找出所有符合minimum support 的 frequent patterns 與 其 support值

```python=
def rule_generator(freq_itemset, _candidate_sets, init_num, min_confidence, rules_list): #['4','3','2','1'] 
	if len(freq_itemset) == 1 :
		return 
	elif init_num > len(freq_itemset):
		return 
	elif len(freq_itemset) > 1:
		if init_num == 1 : #第一層
			_candidate_sets = [frozenset(subset) for subset in list(itertools.combinations(freq_itemset,len(freq_itemset)-1))]
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
```
這段為rule generation的階段，和先前hash tree的方法相同，不再贅述

找出rules後，關於後續的程式碼也和Hash tree的部分大致相同，主要只是寫入檔案和整理list而已。