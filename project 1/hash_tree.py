import numpy as np
import csv
import pandas as pd
import itertools
import time

class HNode:

    def __init__(self):
        self.children = {}
        self.isLeaf = True
        self.bucket = {}


class HTree:

    def __init__(self, max_leaf_cnt, max_child_cnt):
        self.root = HNode()
        self.max_leaf_cnt = max_leaf_cnt
        self.max_child_cnt = max_child_cnt
        self.frequent_itemsets = []

    def recur_insert(self, node, itemset, index, cnt):
        """
        Recursively adds nodes inside the tree and if required splits leaf node and
        redistributes itemsets among child converting itself into intermediate node.
        """
        if index == len(itemset):
            # last bucket so just insert
            if itemset in node.bucket:
                node.bucket[itemset] += cnt
            else:
                node.bucket[itemset] = cnt
            return

        if node.isLeaf:

            if itemset in node.bucket:
                node.bucket[itemset] += cnt
            else:
                node.bucket[itemset] = cnt
            if len(node.bucket) == self.max_leaf_cnt:
                # bucket has reached its maximum capacity and its intermediate node so
                # split and redistribute entries.
                for old_itemset, old_cnt in node.bucket.items():

                    hash_key = self.hash(old_itemset[index])
                    if hash_key not in node.children:
                        node.children[hash_key] = HNode()
                    self.recur_insert(node.children[hash_key], old_itemset, index + 1, old_cnt)
                # there is no point in having this node's bucket
                # so just delete it
                del node.bucket
                node.isLeaf = False
        else:
            hash_key = self.hash(itemset[index])
            if hash_key not in node.children:
                node.children[hash_key] = HNode()
            self.recur_insert(node.children[hash_key], itemset, index + 1, cnt)

    def insert(self, itemset):
        # as list can't be hashed we need to convert this into tuple
        # which can be easily hashed in leaf node buckets
        itemset = tuple(itemset)
        self.recur_insert(self.root, itemset, 0, 0)

    def add_support(self, itemset):
        runner = self.root
        itemset = tuple(itemset)
        index = 0
        while True:
            if runner.isLeaf:
                if itemset in runner.bucket:
                    runner.bucket[itemset] += 1
                break
            hash_key = self.hash(itemset[index])
            if hash_key in runner.children:
                runner = runner.children[hash_key]
            else:
                break
            index += 1

    def dfs(self, node, support_cnt):
        if node.isLeaf:
            for key, value in node.bucket.items():
                if value >= support_cnt:
                    self.frequent_itemsets.append((list(key), value))
                    # print key, value, support_cnt
            return

        for child in node.children.values():
            self.dfs(child, support_cnt)

    def get_frequent_itemsets(self, support_cnt):
        """
        Returns all frequent itemsets which can be considered for next level
        """
        self.frequent_itemsets = []
        self.dfs(self.root, support_cnt)
        return self.frequent_itemsets

    def hash(self, val):
        return hash(val)

