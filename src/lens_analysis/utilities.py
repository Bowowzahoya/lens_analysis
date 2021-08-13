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
import numpy as np

from itertools import chain
from collections import Counter
from .constants import *

def join(col):
    col = col.dropna()
    return BIG_SEPARATOR.join(col.astype(str))

def join_first(col):
    col = col.dropna()
    if len(col) == 0:
        return np.nan
    return col.iloc[0]

def join_set(col):
    col = col.dropna()
    all_vals = col.astype(str).str.split(SEPARATOR)
    return SEPARATOR.join(set(chain(*all_vals)))

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

def join_most(column):
    """ 
    Will return value that occurs most often    
    """
    column = column.dropna()
    all_values = column.astype(str).str.split(SEPARATOR)
    all_values = [val for val in chain(*all_values)]
    if len(all_values) == 0:
        return np.nan
    modes = get_mode_or_modes(all_values)
    return SEPARATOR.join(modes)

def get_mode_or_modes(list_):
    counter = Counter(list_)
    return [key for key, count in counter.items() if count == counter.most_common(1)[0][1]]

def join_columns(df, conversion_function_dict):
    """ 
    Compresses a df of a family to a series of the family
    conversion_function_dict: dictionary of length 2 tuples, first string, second function
        to map column to a single value
    
    """
    sr = pd.Series()
    for column_in in df.columns:
        if column_in in conversion_function_dict:
            index_out = conversion_function_dict[column_in][0]
            function = conversion_function_dict[column_in][1]
        else: 
            continue
        sr[index_out] = function(df[column_in])
    return sr

def contains_word(string, series_of_words):
    """
    Fast method to check if any of a series of words is contained
    exactly in a string
    That is: series_of_words=[ai], string=air pressure will return False, 
    but series_of_words=[ai], str_sr=responsible ai, will return True
    """
    string = " "+string+" "
    series_of_words = " "+series_of_words+" "
    return series_of_words.apply(lambda x: x in string).any()

def contains_string(string, series_of_strings):
    """
    is any of the strings in series_of_strings contained in string
    """
    return series_of_strings.apply(lambda x: x in string).any()

def ends_on_word(string, series_of_words):
    """
    Fast method to check if a string ends with any in a series of words
    """
    string = " "+string
    series_of_words = " "+series_of_words
    return series_of_words.apply(lambda x: \
                                x == string[-min(len(string), len(x)):]).any()

    