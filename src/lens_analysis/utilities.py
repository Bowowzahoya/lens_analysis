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

# Family and applicant merging mixins
def get_conversion_function_dict(custom_conversion_function_dict, type_="families"):
    if type_ == "families":
        conversion_function_dict = FAMILIES_DEFAULT_CONVERSION_FUNCTION_DICT.copy()
    elif type_ == "applicants":
        conversion_function_dict = APPLICANTS_DEFAULT_CONVERSION_FUNCTION_DICT.copy()
    else:
        raise Exception()

    for key in custom_conversion_function_dict:
        conversion_function_dict[key] = custom_conversion_function_dict[key]
    return conversion_function_dict

def join_columns(df, conversion_function_dict):
    """ 
    Compresses a dataframe to a series by specified functions

    conversion_function_dict: dictionary of length 2 tuples, 
    key: 
    - string, name of column in df
    value: 
    - first tuple element, string,
        name of target index in output series
    - second tuple element, function,
        function to map column to a single value
    
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

FAMILIES_DEFAULT_CONVERSION_FUNCTION_DICT = {\
    JURISDICTION_COL:(JURISDICTIONS_COL, join_set),
    KIND_COL:(KINDS_COL, join_set),
    PUBLICATION_NUMBER_COL:(PUBLICATION_NUMBERS_COL, join_set),
    LENS_ID_COL:(LENS_IDS_COL, join_set),
    PUBLICATION_DATE_COL:(EARLIEST_PUBLICATION_DATE_COL, join_earliest),
    PUBLICATION_YEAR_COL:(EARLIEST_PUBLICATION_YEAR_COL, join_earliest),
    APPLICATION_NUMBER_COL:(APPLICATION_NUMBERS_COL, join_set),
    APPLICATION_DATE_COL:(EARLIEST_APPLICATION_DATE_COL, join_earliest),
    EARLIEST_PRIORITY_DATE_COL:(EARLIEST_PRIORITY_DATE_COL, join_earliest),
    TITLE_COL:(TITLE_COL, join_set),
    ABSTRACT_COL:(FIRST_ABSTRACT_COL, join_first),
    APPLICANTS_COL:(APPLICANTS_COL, join_set),
    INVENTORS_COL:(INVENTORS_COL, join_set),
    OWNERS_COL:(OWNERS_COL, join_set),
    URL_COL:(URLS_COL, join_set),
    DOCUMENT_TYPE_COL:(DOCUMENT_TYPES_COL, join_set),
    CITES_PATENT_COUNT_COL:(FAMILY_CITES_PATENT_COUNT_COL, join_sum),
    CITED_PATENT_COUNT_COL:(FAMILY_CITED_PATENT_COUNT_COL, join_sum),
    SIMPLE_FAMILY_SIZE_COL:(SIMPLE_FAMILY_SIZE_COL, join_max),
    EXTENDED_FAMILY_SIZE_COL:(EXTENDED_FAMILY_SIZE_COL, join_max),
    CPC_CLASSIFICATIONS_COL:(CPC_CLASSIFICATIONS_COL, join_sum),
    IPCR_CLASSIFICATIONS_COL:(IPCR_CLASSIFICATIONS_COL, join_set),
    US_CLASSIFICATIONS_COL:(US_CLASSIFICATIONS_COL, join_set),
    HAS_FULL_TEXT_COL:(INCLUDED_SIMPLE_FAMILY_SIZE_COL, join_size)}

APPLICANTS_DEFAULT_CONVERSION_FUNCTION_DICT = {\
    CITATION_SCORE_COL:(MEAN_CITATION_SCORE_COL, join_mean),
    APPLICANTS_COL:(JOINT_PATENTS_WITH_COL, join_set),
    LENS_IDS_COL:(FAMILIES_COUNT_COL, join_size),
    JURISDICTIONS_COL:(JURISDICTIONS_COL, join_set),
    PRIORITY_JURISDICTIONS_COL:(PRIORITY_JURISDICTIONS_COL, join_set),
    CITATION_SCORE_COL:(MEAN_CITATION_SCORE_COL, join_mean),
    MARKET_COVERAGE_COL:(MEAN_MARKET_COVERAGE, join_mean),
    PATENT_POWER_COL:(MEAN_PATENT_POWER, join_mean)}

# Applicant utilities
def unfold_cell_overloaded_column(dataframe, in_column_name, out_column_name, separator=SEPARATOR):
    """
    Cell overloaded columns are string columns where single cells contain multiple values,
    separated by a separator (e.g. ';;')

    This function splits the cells into new cells, that are appended at the end of the dataframe,
    with the rest of the row identical to the original row.

    This is for example useful in applicant splitting and grouping.
    """
    split_column = dataframe[in_column_name].str.split(separator, expand=True)
    dataframe[out_column_name] = split_column[0]

    for column in split_column.columns[1:]:
        new_cells = split_column[column].dropna()

        new_rows = dataframe.loc[new_cells.index].copy()
        new_rows[out_column_name] = new_cells

        dataframe = dataframe.append(new_rows)
    return dataframe


# Recognizing string content in Series format
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

    