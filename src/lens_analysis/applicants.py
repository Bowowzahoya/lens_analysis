# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021

This module provides functionality for finding the biggest applicant
from patent family data

Main functions:
    - merge_to_applicants(), takes a patent family DataFrame and
    groups them into families per applicant, also distilling other
    information like covered jurisdiction, market coverage, citation scores
    
    The function makes use of dictionary 
    FUNC_D that maps certain columns from the family DataFrame (key)
    to new columns (value1) in the applicant DataFrame 
    through a function (value2)
    
    You can add or change these mappings by providing a custom_func_d
    
    - alias_apps(), maps applicant names in a family DataFrame to
    other names. Can be used to add different variants of a name together.
    For example IBM Licensing, IBM China and I.B.M. all map to IBM.
    This can be done using either a dict or a function.
    After this, merge_to_applicants() can be used on the new applicant column
    to get a fairer picture.

@author: David
"""
import pandas as pd
from itertools import chain
from collections import defaultdict
from .constants import *
from .utilities import join_columns, APPLICANTS_DEFAULT_CONVERSION_FUNCTION_LIST
from .utilities import unfold_cell_overloaded_column

def merge_to_applicants(families: pd.DataFrame, 
                        conversion_function_list=None,
                        aliases=pd.Series()):
    """
    Merges a families dataframe into applicants
    
    Returns:
        applicants: DataFrame of applicants with as index the applicant name (or aliased name if supplied)
    """
    families = families.join(_one_hot_encode_years(families))
    families = unfold_cell_overloaded_column(families, APPLICANTS_COL, APPLICANT_COL, separator=SEPARATOR)
    families[ALIASED_APPLICANT_COL] = _get_aliases(families[APPLICANT_COL], aliases)

    groupby = families.groupby(ALIASED_APPLICANT_COL)
    
    if isinstance(conversion_function_list, type(None)):
        conversion_function_list = APPLICANTS_DEFAULT_CONVERSION_FUNCTION_LIST
    applicants = groupby.apply(join_columns, conversion_function_list)
    return applicants

def _one_hot_encode_years(families, year_column_name=EARLIEST_PRIORITY_YEAR_COL):
    years = families[year_column_name].unique()

    dataframe = pd.DataFrame(index=families.index, columns=[str(yr) for yr in years], data=0)
    for year in years:
        mask = families[year_column_name] == year
        dataframe.loc[mask, str(year)] = 1
    return dataframe

def _get_aliases(applicant_series:pd.Series, aliases):
    aliased_list = [aliases[applicant] if applicant in aliases.index else applicant for applicant in applicant_series]
    return pd.Series(index=applicant_series.index, data=aliased_list)