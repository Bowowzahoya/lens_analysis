# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021
Utility functions for other modules

There are a few join functions that
are options for collapsing columns into a single value

join_cols is the basic function for collapsing a dataframe into
a series that is used to collapse Lens exports to family dataframes
or family dataframes to applicant dataframes.

@author: David
"""
import pandas as pd
from itertools import chain
from collections import Counter
from .constants import *

def _mode(sample):
     c = Counter(sample)
     return [k for k, v in c.items() if v == c.most_common(1)[0][1]]
 
def join(col):
    return BIG_SEP.join(col.astype(str))

def join_set(col):
    all_vals = col.astype(str).str.split(SEP)
    return SEP.join(set(chain(*all_vals)))

def join_max(col):
    return col.max()

def join_sum(col):
    return col.sum()

def join_mean(col):
    return col.mean()

def join_earliest(col):
    return col.sort_values().iloc[0]

def join_size(col):
    return len(col)

def join_most(col):
    """ 
    Will return value that occurs most often    
    """
    all_vals = col.astype(str).str.split(SEP)
    all_vals = [val for val in chain(*all_vals)]
    mode = _mode(all_vals)
    return SEP.join(mode)

def join_cols(df, func_d):
    """ 
    Compresses a df of a family to a series of the family
    func_d: dictionary of length 2 tuples, first string, second function
        mapping of columns through function to other column
    std_func: function to use when column not in func_d
        will automatically map to same column name
    
    """
    sr = pd.Series()
    for col in df.columns:
        if col in func_d:
            col_out = func_d[col][0]
            func = func_d[col][1]
        else: 
            continue
        sr[col_out] = func(df[col])
    return sr



    