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
import re

from itertools import chain
from collections import Counter
from .constants import *

# Family and applicant merging mixins
def join_columns(df, dataframe_compressor):
    return dataframe_compressor.convert(df)

class DataFrameCompressor():
    """
    Compresses a DataFrame to a series using 'CompressionFunction' instances
    """
    def __init__(self, compression_functions: list):
        self.compression_functions = []
        for compression_function in compression_functions:
            self.update(compression_function)
    
    def convert(self, dataframe):
        compression_outputs = []
        for compression_function in self.compression_functions:
            compression_outputs.append(compression_function.convert(dataframe))

        compression_outputs_dict = {k:v for item in compression_outputs for (k,v) in item.items()}
        return pd.Series(compression_outputs_dict)

    def update(self, compression_function):
        if isinstance(compression_function, CompressionFunction):
            self.update_from_compression_function(compression_function)
        elif isinstance(compression_function, tuple):
            self.update_from_tuple(compression_function)

    def update_from_compression_function(self, compression_function):
        self.compression_functions.append(compression_function)

    def update_from_tuple(self, tuple_):
        if len(tuple_) == 4:
            kwargs = tuple_[3]
        else:
            kwargs = {}
        compression_function = CompressionFunction(*tuple_[:3], **kwargs)
        self.compression_functions.append(compression_function)

class CompressionFunction():
    """
    Compresses a number of columns in a DataFrame to a series using a specified function

    If regex-pattern provided, it will work on multiple columns. Only the first column can have a regex.
    """
    def __init__(self, in_column_names, function, out_index_names, 
                remove_duplicate_index=True):
        self.function = function
        self.in_column_names = in_column_names # can be strings or regex-pattern + strings
        self.out_index_names = out_index_names # can be strings or functions with input 'in_column_names' (must be if in_column_names has regex-patterns)
        self.remove_duplicate_index = remove_duplicate_index

    @property
    def in_columns_have_re_pattern(self):
        return any([isinstance(col, re.Pattern) for col in self.in_column_names])

    @property
    def out_indexes_have_function(self):
        return any([callable(ix) for ix in self.out_index_names])

    def get_in_out_pairs(self, dataframe):
        if self.in_columns_have_re_pattern:
            in_names = [[col]+self.in_column_names[1:] for col in dataframe.columns if bool(self.in_column_names[0].match(col))]
        else:
            in_names = [[col for col in self.in_column_names]]

        if self.out_indexes_have_function:
            out_names = [[func(in_name) for func in self.out_index_names] for in_name in in_names]
        else:
            out_names = [[ix for ix in self.out_index_names]]

        return zip(in_names, out_names)
        
    def convert(self, dataframe) -> dict:
        result_dicts = []

        for in_column_names, out_index_names in self.get_in_out_pairs(dataframe):
            result_list = self.convert_one(dataframe, in_column_names)
            result_dicts.append({k:v for k,v in zip(out_index_names, result_list)})

        return {k:v for item in result_dicts for (k,v) in item.items()}

    def convert_one(self, dataframe, in_column_names):
        if self.remove_duplicate_index:
            dataframe = dataframe[~dataframe.index.copy().duplicated(keep='first')].copy()

        return self.function(dataframe[in_column_names])

# wrapper for functions that take a single Series and return a single value
def single_argument_single_output(function):
    def wrapper(dataframe):
        series = dataframe[dataframe.columns[0]]
        output = function(series)
        return [output]
    return wrapper

def single_output(function):
    def wrapper(dataframe):
        output = function(dataframe)
        return [output]
    return wrapper

@single_argument_single_output
def join(col):
    col = col.dropna()
    return BIG_SEPARATOR.join(col.astype(str))

@single_argument_single_output
def join_first(col):
    col = col.dropna()
    if len(col) == 0:
        return np.nan
    return col.iloc[0]

@single_argument_single_output
def join_first_english(col):
    col = col.dropna()
    if len(col) == 0:
        return np.nan
    
    col_mask = col.apply(lambda el: contains_string(el, ENGLISH_IDENTIFIER_STRINGS))
    col = col[col_mask]
    if len(col) == 0:
        return np.nan

    return col.iloc[0]

@single_argument_single_output
def join_set(col):
    col = col.dropna()
    all_vals = col.astype(str).str.split(SEPARATOR)
    return SEPARATOR.join(set(chain(*all_vals)))

@single_argument_single_output
def join_set_len(col):
    col = col.dropna()
    all_vals = col.astype(str).str.split(SEPARATOR)
    return len(set(chain(*all_vals)))

@single_argument_single_output
def join_max(col):
    return col.max()

@single_argument_single_output
def join_sum(col):
    return col.sum()

@single_output
def join_sum_weighted(df):
    df = df.dropna()
    value_column = df.iloc[:, 0]
    weight_column = df.iloc[:, 1]
    return (value_column*weight_column).sum()

@single_argument_single_output
def join_mean(col):
    return col.mean()

@single_output
def join_mean_weighted(df):
    df = df.dropna()
    value_column = df.iloc[:, 0]
    weight_column = df.iloc[:, 1]
    return (value_column*weight_column).sum()/weight_column.sum()

@single_argument_single_output
def join_earliest(col):
    return col.sort_values().iloc[0]

@single_argument_single_output
def join_size(col):
    return len(col)

@single_argument_single_output
def join_any(col):
    return any(col)

@single_argument_single_output
def join_size_not_nan(col):
    is_na = col.isna().value_counts()
    if False in is_na.index:
        return col.isna().value_counts()[False]
    else:
        return 0

@single_output
def join_size_not_nan_weighted(df):
    value_column = df.iloc[:, 0]
    weight_column = df.iloc[:, 1]
    not_na_mask = value_column.notna()
    if not not_na_mask.any():
        return 0
    else:
        return weight_column[not_na_mask].sum()

@single_argument_single_output
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

@single_output
def join_dict_sum(df):
    df = df.dropna()
    sr = df.groupby(df.columns[0])[df.columns[1]].sum()
    return SEPARATOR.join([f"{ix}:{sr.loc[ix]}" for ix in sr.index])


def get_mode_or_modes(list_):
    counter = Counter(list_)
    return [key for key, count in counter.items() if count == counter.most_common(1)[0][1]]

FAMILIES_DEFAULT_DATAFRAME_COMPRESSOR = DataFrameCompressor([\
	([JURISDICTION_COL], join_set, [JURISDICTIONS_COL]),
	([KIND_COL], join_set, [KINDS_COL]),
	([PUBLICATION_NUMBER_COL], join_set, [PUBLICATION_NUMBERS_COL]),
	([LENS_ID_COL], join_set, [LENS_IDS_COL]),
	([PUBLICATION_DATE_COL], join_earliest, [EARLIEST_PUBLICATION_DATE_COL]),
	([PUBLICATION_YEAR_COL], join_earliest, [EARLIEST_PUBLICATION_YEAR_COL]),
	([APPLICATION_NUMBER_COL], join_set, [APPLICATION_NUMBERS_COL]),
	([APPLICATION_DATE_COL], join_earliest, [EARLIEST_APPLICATION_DATE_COL]),
	([EARLIEST_PRIORITY_DATE_COL], join_earliest, [EARLIEST_PRIORITY_DATE_COL]),
	([TITLE_COL], join_set, [TITLES_COL]),
	([ABSTRACT_COL], join_first_english, [FIRST_ENGLISH_ABSTRACT_COL]),
	([APPLICANTS_COL], join_set, [APPLICANTS_COL]),
	([INVENTORS_COL], join_set, [INVENTORS_COL]),
	([OWNERS_COL], join_set, [OWNERS_COL]),
	([URL_COL], join_first, [FIRST_URL_COL]),
	([DOCUMENT_TYPE_COL], join_set, [DOCUMENT_TYPES_COL]),
	([CITES_PATENT_COUNT_COL], join_sum, [FAMILY_CITES_PATENT_COUNT_COL]),
	([CITED_PATENT_COUNT_COL], join_sum, [FAMILY_CITED_PATENT_COUNT_COL]),
    ([JURISDICTION_COL, CITED_PATENT_COUNT_COL], join_dict_sum, [CITED_PER_JURISDICTION_COL]),
	([SIMPLE_FAMILY_SIZE_COL], join_max, [SIMPLE_FAMILY_SIZE_COL]),
	([EXTENDED_FAMILY_SIZE_COL], join_max, [EXTENDED_FAMILY_SIZE_COL]),
	([CPC_CLASSIFICATIONS_COL], join_set, [CPC_CLASSIFICATIONS_COL]),
	([IPCR_CLASSIFICATIONS_COL], join_set, [IPCR_CLASSIFICATIONS_COL]),
	([US_CLASSIFICATIONS_COL], join_set, [US_CLASSIFICATIONS_COL]),
	([HAS_FULL_TEXT_COL], join_size, [INCLUDED_SIMPLE_FAMILY_SIZE_COL]),
    ([LEGAL_STATUS_COL], join_set, [LEGAL_STATUSES_COL])])

APPLICANTS_DEFAULT_DATAFRAME_COMPRESSOR = DataFrameCompressor([\
	([APPLICANTS_COL], join_set, [JOINT_PATENTS_WITH_COL]),
	([INVENTORS_COL], join_set, [INVENTORS_COL]),
	([APPLICANT_IN_INVENTORS_COL], join_any, [IS_INVENTOR_COL]),
	([LENS_IDS_COL], join_size, [FAMILIES_COUNT_COL]),
	([JURISDICTIONS_COL], join_set, [JURISDICTIONS_COL]),
	([JURISDICTIONS_COL], join_most, [MAIN_JURISDICTION_COL]),
	([PRIORITY_JURISDICTIONS_COL], join_set, [PRIORITY_JURISDICTIONS_COL]),
	([PRIORITY_JURISDICTIONS_COL], join_most, [MAIN_PRIORITY_JURISDICTION_COL]),
	([CITATION_SCORE_COL, WEIGHT_PER_APPLICANT_COL], join_mean_weighted, [MEAN_CITATION_SCORE_COL], {"remove_duplicate_index":False}),
	([MARKET_COVERAGE_COL, WEIGHT_PER_APPLICANT_COL], join_mean_weighted, [MEAN_MARKET_COVERAGE_COL], {"remove_duplicate_index":False}),
	([PATENT_POWER_COL, WEIGHT_PER_APPLICANT_COL], join_mean_weighted, [MEAN_PATENT_POWER_COL], {"remove_duplicate_index":False}),
	([WEIGHT_PER_APPLICANT_COL], join_sum, [FRACTIONAL_FAMILIES_COUNT_COL], {"remove_duplicate_index":False}),
	([IS_TOP_PATENT_COL], join_sum, [TOP_PATENTS_COL]),
	([IS_TOP_PATENT_COL], join_size_not_nan, [HAS_CITATION_SCORE_NUMBER_COL]),
	([IS_TOP_PATENT_COL, WEIGHT_PER_APPLICANT_COL], join_sum_weighted, [FRACTIONAL_TOP_PATENTS_COL], {"remove_duplicate_index":False}),
	([IS_TOP_PATENT_COL, WEIGHT_PER_APPLICANT_COL], join_size_not_nan_weighted, [FRACTIONAL_HAS_CITATION_SCORE_NUMBER_COL], {"remove_duplicate_index":False}),
	([YEARLY_AMOUNTS_COL_RE_PATTERN], join_sum, [lambda cols: cols[0]]),
	([YEARLY_AMOUNTS_COL_RE_PATTERN, WEIGHT_PER_APPLICANT_COL], join_sum_weighted, [lambda cols: cols[0]+FRACTIONAL_COL_EXTENSION], {"remove_duplicate_index":False})])
	
APPLICANT_TYPES_DEFAULT_DATAFRAME_COMPRESSOR = DataFrameCompressor([\
	([INVENTORS_COL], join_set_len, [UNIQUE_INVENTORS_COL]),
	([MEAN_CITATION_SCORE_COL, FRACTIONAL_FAMILIES_COUNT_COL], join_mean_weighted, [MEAN_CITATION_SCORE_COL]),
	([MEAN_MARKET_COVERAGE_COL, FRACTIONAL_FAMILIES_COUNT_COL], join_mean_weighted, [MEAN_MARKET_COVERAGE_COL]),
	([MEAN_PATENT_POWER_COL, FRACTIONAL_FAMILIES_COUNT_COL], join_mean_weighted, [MEAN_PATENT_POWER_COL]),
	([FRACTIONAL_FAMILIES_COUNT_COL], join_sum, [FRACTIONAL_FAMILIES_COUNT_COL]),
	([FRACTIONAL_TOP_PATENTS_COL], join_sum, [FRACTIONAL_TOP_PATENTS_COL]),
	([FRACTIONAL_HAS_CITATION_SCORE_NUMBER_COL], join_sum, [FRACTIONAL_HAS_CITATION_SCORE_NUMBER_COL]),
	([FRACTIONAL_YEARLY_AMOUNTS_COL_RE_PATTERN], join_sum, [lambda cols: cols[0]])])


# Applicant utilities
def unfold_cell_overloaded_column(dataframe, in_column_name, out_column_name, separator=SEPARATOR):
    """
    Cell overloaded columns are string columns where single cells contain multiple values,
    separated by a separator (e.g. ';;')

    This function splits the cells into new cells, that are appended at the end of the dataframe,
    with the rest of the row identical to the original row.

    This is for example useful in applicant splitting and grouping.
    """
    new_dataframe = dataframe.copy()

    split_column = dataframe[in_column_name].str.split(separator, expand=True)

    new_dataframe[out_column_name] = split_column[0]

    for column in split_column.columns[1:]:
        new_cells = split_column[column].dropna()

        new_rows_dataframe = dataframe.loc[new_cells.index.dropna()].copy()
        new_rows_dataframe[out_column_name] = new_cells

        new_dataframe = pd.concat([new_dataframe, new_rows_dataframe])
    return new_dataframe


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

def has_string(string, series_of_strings):
    return string in series_of_strings.values