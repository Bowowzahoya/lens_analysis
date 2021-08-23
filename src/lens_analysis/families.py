# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021
Functionality for grouping families from Lens .csv exports
Using merge_to_family() to create a dataframe of families with 
all covered jurisdictions, earliest publication data, 
all applicant names, etc.

The function makes use of dictionary 
FUNC_D that maps certain columns from the family DataFrame (key)
to new columns (value1) in the applicant DataFrame 
through a function (value2)
    
You can add or change these mappings by providing a custom_func_d

@author: David
"""
import pandas as pd
import numpy as np

from lens_analysis.market_coverage import get_market_coverage
from .constants import *
from .citations import get_citation_score
from .market_coverage import get_market_coverage
from .utilities import join_columns, FAMILIES_DEFAULT_CONVERSION_FUNCTION_LIST

def merge_to_family(lens_export: pd.DataFrame, conversion_function_list=None):
    """
    Merges a Lens patent export at the publication level into families.
    
    Parameters:
        lens_export: DataFrame
        Lens export with publications per row
        
        custom_conversion_function_dict: dict with tuples of length 2 as values, optional
        A dictionary of which columns in the lens_export to map to which columns
        in the family DataFrame, using which function. Where no values, will use default conversion dict.
        The default is {}.
    
    Returns:
        families: DataFrame of patent families with as index the sorted priority numbers
    """
    # Needed because NL00918;;NL988 should be same family as NL988;;NL00918
    lens_export[SORTED_PRIORITY_NUMBERS_COL] = lens_export[PRIORITY_NUMBERS_COL].apply(_sort_priority_numbers)
    
    groupby = lens_export.groupby(SORTED_PRIORITY_NUMBERS_COL)
    
    if isinstance(conversion_function_list, type(None)):
        conversion_function_list = FAMILIES_DEFAULT_CONVERSION_FUNCTION_LIST
    families = groupby.apply(join_columns, conversion_function_list)

    return families

def _sort_priority_numbers(priority_numbers: str):
    return SEPARATOR.join(sorted(priority_numbers.split(SEPARATOR)))

def add_extra_family_information(families: pd.DataFrame):
    families[EARLIEST_PRIORITY_YEAR_COL] = _get_years(families[EARLIEST_PRIORITY_DATE_COL])

    families[PRIORITY_JURISDICTIONS_COL] = families.index.map(_get_jurisdictions_from_numbers)

    families[CITATION_SCORE_COL] = get_citation_score(families)

    families[MARKET_COVERAGE_COL] = get_market_coverage(families)

    families[PATENT_POWER_COL] = families[CITATION_SCORE_COL]*families[MARKET_COVERAGE_COL]

    families[IS_TOP_PATENT_COL] = _get_is_top_patents(families[PATENT_POWER_COL])

    families[WEIGHT_PER_APPLICANT_COL] = _get_weight_per_applicant(families[APPLICANTS_COL])

    return families

def _get_jurisdictions_from_numbers(numbers: str):
    jurisdictions_list = [prio[:2] for prio in numbers.split(SEPARATOR)]
    return SEPARATOR.join(set(jurisdictions_list))

def _get_is_top_patents(patent_powers: pd.Series, top_percentage=0.1):
    non_na_patent_powers = patent_powers.dropna()
    sorted_patent_powers = non_na_patent_powers.sort_values(ascending=False)

    top_threshold = int(top_percentage*len(patent_powers))
    top_indices = sorted_patent_powers.iloc[:top_threshold].index

    is_top_patents = pd.Series(index=patent_powers.index, data=np.nan)
    is_top_patents.loc[non_na_patent_powers.index] = False
    is_top_patents.loc[top_indices] = True
    return is_top_patents

def _get_years(dates: pd.Series):
    dates = pd.to_datetime(dates)
    return dates.dt.year

def _get_weight_per_applicant(applicants_series: pd.Series):
    return 1./applicants_series.str.split(SEPARATOR).str.len()



    