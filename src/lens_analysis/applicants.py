# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021

This module provides functionality for finding the biggest applicant
from patent family data

Main functions:
    - merge_to_applicants(), takes a patent family DataFrame and
    groups them into families per applicant, also distilling other
    information like covered jurisdiction, market coverage, citation scores

@author: David
"""
import pandas as pd
from itertools import chain
from collections import defaultdict
from .constants import *
from .utilities import join_columns, APPLICANTS_DEFAULT_DATAFRAME_COMPRESSOR
from .utilities import unfold_cell_overloaded_column

def merge_to_applicants(families: pd.DataFrame, 
                        dataframe_compressor=APPLICANTS_DEFAULT_DATAFRAME_COMPRESSOR,
                        aliases=pd.Series(dtype="object")):
    """
    Merges a families dataframe into applicants
    
    Parameters:
        families: DataFrame
        dataframe_compressor: DataFrameCompressor
        - Provides how to compress the different columns to a single value per applicant
        aliases: Series
        - Aliases to use per applicant (e.g. IBM UK: IBM, IBM CO LTD: IBM)
    Returns:
        applicants: DataFrame of applicants with as index the applicant name (or aliased name if supplied)
    """
    families = families.join(_one_hot_encode_years(families))
    families = unfold_cell_overloaded_column(families, APPLICANTS_COL, APPLICANT_COL, separator=SEPARATOR)

    families[APPLICANT_IN_INVENTORS_COL] = families.apply(_get_applicant_in_inventors, axis=1)
    families[ALIASED_APPLICANT_COL] = _get_aliases(families[APPLICANT_COL], aliases)

    groupby = families.groupby(ALIASED_APPLICANT_COL)

    applicants = groupby.apply(join_columns, dataframe_compressor)
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

def _get_applicant_in_inventors(row):
    return row[APPLICANT_COL] in row[INVENTORS_COL].split(SEPARATOR)