#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Apr 2 12:38:49 2020

@author: juanmalagon
"""


import itertools

from collections import defaultdict
from scipy.sparse import lil_matrix


class Graph:
    
    def __init__(self,vertices):
        self.V= vertices
        self.graph= defaultdict(list)
        self.tc = lil_matrix((self.V, self.V))
    
    def addEdge(self,u,v):
        self.graph[u].append(v)
    
    def DFSUtil(self,s,v):
        self.tc[s,v] = 1
        for i in self.graph[v]:
            if self.tc[s,i]==0:
                self.DFSUtil(s,i)
        
    def transitiveClosure(self):
        for i in range(self.V):
            print('Transitive closure of ', i, ' out of ', self.V, ' completed')
            self.DFSUtil(i, i)


def dfs_transitive_closure(iterable, tuples):
    enumeration = list(enumerate(iterable))
    enumeration_reversed = [(a,b) for (b,a) in enumeration]
    num_to_idi = dict(enumeration)
    idi_to_num = dict(enumeration_reversed)
    tuples_num = [(idi_to_num[a], idi_to_num[b]) for (a,b) in tuples]
    my_graph = Graph(len(iterable))
    for item in tuples_num:
        my_graph.addEdge(item[0],item[1])
    my_graph.transitiveClosure()
    tuples_final = [(m,n) for m in range(len(iterable)) for n in range(len(iterable)) if my_graph.tc[m,n] == 1]
    tuples_final_idi = [(num_to_idi[a], num_to_idi[b]) for (a,b) in tuples_final]
    return tuples_final_idi


def make_equivalence_classes(iterable, tuples):
    enumeration = list(enumerate(iterable))
    enumeration_reversed = [(a,b) for (b,a) in enumeration]
    num_to_idi = dict(enumeration)
    idi_to_num = dict(enumeration_reversed)
    tuples_num = [(idi_to_num[a], idi_to_num[b]) for (a,b) in tuples]
    my_graph = Graph(len(iterable))
    for item in tuples_num:
        my_graph.addEdge(item[0],item[1])
    my_graph.transitiveClosure()
    a_list = list(zip(my_graph.tc.nonzero()[0], my_graph.tc.nonzero()[1]))
    an_iterator = itertools.groupby(a_list, lambda x : x[0])
    classes = list()
    for key, group in an_iterator:
        equivalence_class = [x[1] for x in list(group)]
        equivalence_class_idi = sorted([num_to_idi[item] for item in equivalence_class])
        classes.append(equivalence_class_idi)
        print('Equivalence class of ', key, ' out of ', len(iterable), ' detected')
    unique_data = [list(x) for x in set(tuple(x) for x in classes)]
    return unique_data