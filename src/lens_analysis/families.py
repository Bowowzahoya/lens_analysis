# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021
Functionality for grouping families from Lens .csv exports
Using 'aggregate_to_family()' to create a dataframe of families with 
all covered jurisdictions, earliest publication data, 
all applicant names, etc.

Additional parameters such as citation scores
can be calculated using 'add_extra_family_information()'

@author: David
"""
import pandas as pd
import numpy as np
import datetime as dt

from lens_analysis.market_coverage import get_market_coverage
from .constants import *
from .citations import get_citation_score
from .market_coverage import get_market_coverage
from .utilities import join_columns, FAMILIES_DEFAULT_DATAFRAME_COMPRESSOR

def aggregate_to_family(lens_export: pd.DataFrame, dataframe_compressor=FAMILIES_DEFAULT_DATAFRAME_COMPRESSOR):
    """
    Merges a Lens patent export at the publication level into families.
    
    Parameters:
        lens_export: DataFrame
        - Lens export with publications per row
        dataframe_compressor: DataFrameCompressor
        - Provides how to compress the different columns to a single value per family
    Returns:
        families: DataFrame of patent families with as index the sorted priority numbers
    """
    lens_export[PRIORITY_NUMBERS_COL] = lens_export[PRIORITY_NUMBERS_COL].fillna("")
    lens_export[PRIORITY_NUMBERS_COL] = lens_export[PRIORITY_NUMBERS_COL].astype(str)

    lens_export = _add_family_relevant_priorities(lens_export)
    
    groupby = lens_export.groupby(FAMILY_RELEVANT_PRIORITIES_COL)
    
    families = groupby.apply(join_columns, dataframe_compressor)
    families = _order_families_columns(families)

    return families

def _add_family_relevant_priorities(lens_export: pd.DataFrame):
    lens_export[FAMILY_RELEVANT_PRIORITIES_COL] = lens_export[PRIORITY_NUMBERS_COL].copy()
    
    lens_export[FAMILY_RELEVANT_PRIORITIES_COL] = lens_export[FAMILY_RELEVANT_PRIORITIES_COL].apply(_remove_w_priority_numbers)
    lens_export[FAMILY_RELEVANT_PRIORITIES_COL] = lens_export[FAMILY_RELEVANT_PRIORITIES_COL].apply(_remove_non_p_priority_numbers)
    lens_export[FAMILY_RELEVANT_PRIORITIES_COL] = lens_export.apply(_remove_second_jurisdiction_priorities, axis=1)
    lens_export[FAMILY_RELEVANT_PRIORITIES_COL] = lens_export[FAMILY_RELEVANT_PRIORITIES_COL].apply(_sort_priority_numbers)
    return lens_export

def _remove_w_priority_numbers(priority_numbers):
    new_priority_numbers = [p for p in priority_numbers.split(SEPARATOR) if len(p) > 1] # only if faulty data
    new_priority_numbers = [p for p in new_priority_numbers if p[-1] != PRIORITY_NUMBER_WIPO_EXTENSION]
    if new_priority_numbers == []: return priority_numbers
    else: return SEPARATOR.join(new_priority_numbers)
    
def _remove_non_p_priority_numbers(priority_numbers):
    new_priority_numbers = [p for p in priority_numbers.split(SEPARATOR) if len(p) > 1] # only if faulty data
    new_priority_numbers = [p for p in new_priority_numbers if p[-1] == PRIORITY_NUMBER_PRIORITY_EXTENSION]
    if new_priority_numbers == []: return priority_numbers
    else: return SEPARATOR.join(new_priority_numbers)
    
def _remove_second_jurisdiction_priorities(row):
    priority_numbers = row[FAMILY_RELEVANT_PRIORITIES_COL]
    jurisdiction = row[JURISDICTION_COL]

    new_priority_numbers = [p for p in priority_numbers.split(SEPARATOR) if len(p) > 2] # only if faulty data
    priority_number_jurisdictions = set([p[:2] for p in new_priority_numbers])
    if len(priority_number_jurisdictions) >= 2:
        return SEPARATOR.join([p for p in new_priority_numbers if p[:2] != jurisdiction])
    else:
        return priority_numbers

def _sort_priority_numbers(priority_numbers: str):
    return SEPARATOR.join(sorted(priority_numbers.split(SEPARATOR)))

def add_extra_family_information(families: pd.DataFrame, citation_score_per_jurisdiction=True,
        year_for_citations=dt.date.today().year):
    families[EARLIEST_PRIORITY_YEAR_COL] = _get_years(families[EARLIEST_PRIORITY_DATE_COL])

    families[PRIORITY_JURISDICTIONS_COL] = families.index.map(_get_jurisdictions_from_numbers)

    families[CITATION_SCORE_COL] = get_citation_score(families, 
        citation_score_per_jurisdiction=citation_score_per_jurisdiction, 
        skip_years=[year_for_citations-2, year_for_citations-1, year_for_citations])

    families[MARKET_COVERAGE_COL] = get_market_coverage(families)

    families[PATENT_POWER_COL] = families[CITATION_SCORE_COL]*families[MARKET_COVERAGE_COL]

    families[IS_TOP_PATENT_COL] = _get_is_top_patents(families[PATENT_POWER_COL])

    families[WEIGHT_PER_APPLICANT_COL] = _get_weight_per_applicant(families[APPLICANTS_COL])

    families = _order_families_columns(families)

    return families

def _get_jurisdictions_from_numbers(numbers: str):
    jurisdictions_list = [prio[:2] for prio in numbers.split(SEPARATOR)]
    return SEPARATOR.join(set(jurisdictions_list))

def _get_is_top_patents(patent_powers: pd.Series, top_percentage=0.1):
    non_na_patent_powers = patent_powers.dropna()
    sorted_patent_powers = non_na_patent_powers.sort_values(ascending=False)

    top_threshold = int(top_percentage*len(patent_powers.dropna()))
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

def _order_families_columns(families):
    ordered_columns = [column for column in FAMILIES_ORDERED_COLUMNS if column in families.columns]
    families = families[ordered_columns]
    return families
