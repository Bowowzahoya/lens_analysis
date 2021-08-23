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
def join_columns(df, conversion_function_list):
    """ 
    Compresses a dataframe (typically a groupby subset) to a series by specified conversion functions
    """
    return conversion_function_list.convert(df)

class ConversionFunctionList():
    def __init__(self, conversion_functions: list):
        self.conversion_functions = []
        for conversion_function in conversion_functions:
            self.update(conversion_function)
    
    def convert(self, dataframe):
        series = pd.Series(dtype="object")
        for conversion_function in self.conversion_functions:
            series = series.append(conversion_function.convert(dataframe))
        return series

    def update(self, conversion_function):
        if isinstance(conversion_function, ConversionFunction):
            self.update_from_conversion_function(conversion_function)
        elif isinstance(conversion_function, tuple):
            self.update_from_tuple(conversion_function)

    def update_from_conversion_function(self, conversion_function):
        self.conversion_functions.append(conversion_function)

    def update_from_tuple(self, tuple_):
        if len(tuple_) == 4:
            kwargs = tuple_[3]
        else:
            kwargs = {}
        conversion_function = ConversionFunction(*tuple_[:3], **kwargs)
        self.conversion_functions.append(conversion_function)

class ConversionFunction():
    def __init__(self, function, in_column_name, out_index_name, 
                weight_column_name=None):
        self.function = function
        self.in_column_name = in_column_name # can be string or regex-pattern
        self.out_index_name = out_index_name # can be string or function with input 'in_column_name' (must be if in_column_name is regex-pattern)
        self.weight_column_name = weight_column_name

    @property
    def is_weighted(self):
        return not isinstance(self.weight_column_name, type(None))

    @property
    def in_column_is_re_pattern(self):
        return isinstance(self.in_column_name, re.Pattern)

    @property
    def out_index_is_function(self):
        return callable(self.out_index_name)

    def get_in_out_pairs(self, dataframe):
        if self.in_column_is_re_pattern:
            in_names = [col for col in dataframe.columns if bool(self.in_column_name.match(col))]
        else:
            in_names = [self.in_column_name]

        if self.out_index_is_function:
            out_names = [self.out_index_name(col) for col in in_names]
        else:
            out_names = [self.out_index_name]
        
        return zip(in_names, out_names)
        
    def convert(self, dataframe):
        series = pd.Series()
        for in_column_name, out_index_name in self.get_in_out_pairs(dataframe):
            series[out_index_name] = self.convert_one(dataframe, in_column_name)

        return series

    def convert_one(self, dataframe, in_column_name):
        if self.is_weighted:
            if self.function == join_mean:
                column = dataframe[in_column_name]*dataframe[self.weight_column_name]
                total_weight = dataframe[self.weight_column_name].sum()
                return join_sum(column)/total_weight
            elif self.function == join_sum:
                column = dataframe[in_column_name]*dataframe[self.weight_column_name]
                return self.function(column)
            elif self.function == join_size_not_nan:
                mask = dataframe[in_column_name].notna()
                column = mask*dataframe[self.weight_column_name]
                return join_sum(column)
            else:
                raise Exception(f"Can not do a weighted join with function {self.function}.")
        else:
            return self.function(dataframe[in_column_name])

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

def join_size_not_nan(col):
    isna = col.isna().value_counts()
    if False in isna.index:
        return col.isna().value_counts()[False]
    else:
        return 0

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

FAMILIES_DEFAULT_CONVERSION_FUNCTION_LIST = ConversionFunctionList([\
    (join_set, JURISDICTION_COL, JURISDICTIONS_COL),
    (join_set, KIND_COL, KINDS_COL),
    (join_set, PUBLICATION_NUMBER_COL, PUBLICATION_NUMBERS_COL),
    (join_set, LENS_ID_COL, LENS_IDS_COL),
    (join_earliest, PUBLICATION_DATE_COL, EARLIEST_PUBLICATION_DATE_COL),
    (join_earliest, PUBLICATION_YEAR_COL, EARLIEST_PUBLICATION_YEAR_COL),
    (join_set, APPLICATION_NUMBER_COL, APPLICATION_NUMBERS_COL),
    (join_earliest, APPLICATION_DATE_COL, EARLIEST_APPLICATION_DATE_COL),
    (join_earliest, EARLIEST_PRIORITY_DATE_COL, EARLIEST_PRIORITY_DATE_COL),
    (join_set, TITLE_COL, TITLE_COL),
    (join_first, ABSTRACT_COL, FIRST_ABSTRACT_COL),
    (join_set, APPLICANTS_COL, APPLICANTS_COL),
    (join_set, INVENTORS_COL, INVENTORS_COL),
    (join_set, OWNERS_COL, OWNERS_COL),
    (join_set, URL_COL, URLS_COL),
    (join_set, DOCUMENT_TYPE_COL, DOCUMENT_TYPES_COL),
    (join_sum, CITES_PATENT_COUNT_COL, FAMILY_CITES_PATENT_COUNT_COL),
    (join_sum, CITED_PATENT_COUNT_COL, FAMILY_CITED_PATENT_COUNT_COL),
    (join_max, SIMPLE_FAMILY_SIZE_COL, SIMPLE_FAMILY_SIZE_COL),
    (join_max, EXTENDED_FAMILY_SIZE_COL, EXTENDED_FAMILY_SIZE_COL),
    (join_sum, CPC_CLASSIFICATIONS_COL, CPC_CLASSIFICATIONS_COL),
    (join_set, IPCR_CLASSIFICATIONS_COL, IPCR_CLASSIFICATIONS_COL),
    (join_set, US_CLASSIFICATIONS_COL, US_CLASSIFICATIONS_COL),
    (join_size, HAS_FULL_TEXT_COL, INCLUDED_SIMPLE_FAMILY_SIZE_COL)])

APPLICANTS_DEFAULT_CONVERSION_FUNCTION_LIST = ConversionFunctionList([\
    (join_set, APPLICANTS_COL, JOINT_PATENTS_WITH_COL),
    (join_size, LENS_IDS_COL, FAMILIES_COUNT_COL),
    (join_set, JURISDICTIONS_COL, JURISDICTIONS_COL),
    (join_most, JURISDICTIONS_COL, MAIN_JURISDICTION_COL),
    (join_set, PRIORITY_JURISDICTIONS_COL, PRIORITY_JURISDICTIONS_COL),
    (join_most, PRIORITY_JURISDICTIONS_COL, MAIN_PRIORITY_JURISDICTION_COL),
    (join_mean, CITATION_SCORE_COL, MEAN_CITATION_SCORE_COL, {"weight_column_name": WEIGHT_PER_APPLICANT_COL}),
    (join_mean, MARKET_COVERAGE_COL, MEAN_MARKET_COVERAGE, {"weight_column_name": WEIGHT_PER_APPLICANT_COL}),
    (join_mean, PATENT_POWER_COL, MEAN_PATENT_POWER, {"weight_column_name": WEIGHT_PER_APPLICANT_COL}),
    (join_sum, WEIGHT_PER_APPLICANT_COL, FRACTIONAL_FAMILIES_COUNT_COL),
    (join_sum, IS_TOP_PATENT_COL, TOP_PATENTS_COL),
    (join_size_not_nan, IS_TOP_PATENT_COL, HAS_CITATION_SCORE_NUMBER_COL),
    (join_sum, IS_TOP_PATENT_COL, FRACTIONAL_TOP_PATENTS_COL, {"weight_column_name": WEIGHT_PER_APPLICANT_COL}),
    (join_size_not_nan, IS_TOP_PATENT_COL, FRACTIONAL_HAS_CITATION_SCORE_NUMBER_COL, {"weight_column_name": WEIGHT_PER_APPLICANT_COL}),
    (join_sum, re.compile("[0-9]{4}"), lambda x: x),
    (join_sum, re.compile("[0-9]{4}"), lambda x: x+FRACTIONAL_COL_EXTENSION, {"weight_column_name": WEIGHT_PER_APPLICANT_COL})])
    

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

        new_rows = dataframe.loc[new_cells.index].copy()
        new_rows[out_column_name] = new_cells

        new_dataframe = new_dataframe.append(new_rows)
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

    