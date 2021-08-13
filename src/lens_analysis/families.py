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

from lens_analysis.market_coverage import get_market_coverage
from .constants import *
from .citations import get_citation_score
from .market_coverage import get_market_coverage
from .utilities import join, join_set, join_max, join_sum, join_earliest 
from .utilities import join_size, join_columns, join_most, join_first
from .utilities import get_mode_or_modes

DEFAULT_CONVERSION_FUNCTION_DICT = {\
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
APPLICANTS_COL:(FAMILY_APPLICANTS_COL, join_set),
INVENTORS_COL:(FAMILY_INVENTORS_COL, join_set),
OWNERS_COL:(FAMILY_OWNERS_COL, join_set),
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


def merge_to_family(lens_export, custom_conversion_function_dict={}):
    """
    Merges a Lens patent export at the publication level into families.
    
    Parameters:
        lens_export: DataFrame
        Lens export with publications per row
        
        custom_conversion_function_dict: dict with tuples of length 2 as values, optional
        A dictionary of which columns in the lens_export to map to which columns
        in the family DataFrame, using which function. Uses same structure as DEFAULT_CONVERSION_FUNCTION_DICT
        and will override if there is overlap. The default is {}.
    
    Returns:
        families: DataFrame of patent families with as index the sorted priority numbers
    """
    # Needed because NL00918;;NL988 should be same family as NL988;;NL00918
    lens_export[SORTED_PRIORITY_NUMBERS_COL] = lens_export[PRIORITY_NUMBERS_COL].apply(_sort_priority_numbers)
    
    groupby = lens_export.groupby(SORTED_PRIORITY_NUMBERS_COL)
    
    conversion_function_dict = DEFAULT_CONVERSION_FUNCTION_DICT.copy()
    for key in custom_conversion_function_dict:
        conversion_function_dict[key] = custom_conversion_function_dict[key]
    
    families = groupby.apply(join_columns, conversion_function_dict)

    return families

def _sort_priority_numbers(priority_numbers):
    return SEPARATOR.join(sorted(priority_numbers.split(SEPARATOR)))

def add_extra_family_information(families):
    families[PRIORITY_JURISDICTIONS_COL] = families.index.map(get_jurisdictions_from_number)
    families[CITATION_SCORE_COL] = get_citation_score(families)
    families[MARKET_COVERAGE_COL] = get_market_coverage(families)

    return families

def get_jurisdictions_from_number(numbers):
    jurisdictions_list = [prio[:2] for prio in numbers.split(SEPARATOR)]
    return SEPARATOR.join(set(jurisdictions_list))
    