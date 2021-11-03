#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May  2 02:43:56 2021

@author: juanmalagon
"""


import datetime
import pandas as pd
import time

import functions as fl

# 1. Define connected_comp function

def connected_comp(input_table):
    def relation (a,b):
        '''Defines a boolean relation from the set of tuples'''
        if (a,b) in tuples:
            return True
        else:                       
            return False
    def symmetric_closure(tuples):
        '''Creates the symmetric closure for the boolean relation defned by a set of tuples'''
        closure = set(tuples)
        new_relations = set((y,x) for x,y in closure)
        return list(closure.union(new_relations))
    subset = input_table[['LEFT_SIDE', 'RIGHT_SIDE']]
    tuples = [tuple(x) for x in subset.to_numpy()]
    iterable = list(set(subset.LEFT_SIDE).union(set(subset.RIGHT_SIDE)))
    tuples = symmetric_closure(tuples)
    equivalence_classes = fl.make_equivalence_classes(iterable, tuples)
    return equivalence_classes

# 2. Find connected components and time it

input_table = pd.read_csv('sample.csv')

start_time = time.time()
output = connected_comp(input_table)
end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time finding connected components (seconds): ', elapsed_time)

# 3. Prepare output table

output_table = pd.DataFrame(columns = ['LEFT_SIDE', 'ID_UNIQUE'])
left_side = [item for sublist in output for item in sublist]
id_unique = list()
for index in range(len(output)):
    appendix = [index]*len(output[index])
    id_unique.extend(appendix)
output_table['LEFT_SIDE'] = left_side
output_table['ID_UNIQUE'] = id_unique
new = output_table['LEFT_SIDE'].str.split("|", n = 1, expand = True)
output_table['SOURCE'] = new[0]
output_table['IDI'] = new[1]
output_table = output_table[['ID_UNIQUE', 'SOURCE', 'IDI']].applymap(str)
TIME_PROCESSED = datetime.datetime.now()
output_table['TIM_PROCESSED'] = TIME_PROCESSED

print('Connected components finished succesfully')
