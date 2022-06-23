# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021

Function calc_mncs():
Calculates the mean normalized citation score
per patent family per year. Will rely on the sum of citations
of all family documents, and earliest publication year of all
family documents for assigned year of the family.

The mean normalized citation score is the field-normalized year-normalized
amounts of citations (normalized by world average). This means a score of 1.0
is exactly the amount of citations expected for this sector for
this year.

Function requires that provided families are already in a single sector, 
and includes the whole world.
Function does not split up per sector.

@author: David
"""
import pandas as pd
from itertools import chain
from .constants import *
import datetime as dt
from collections import Counter
import numpy as np


def get_citation_score(dataframe, 
        year_column=EARLIEST_PUBLICATION_YEAR_COL,
        citation_score_per_jurisdiction=True,
        skip_years=[dt.date.today().year-2, dt.date.today().year-1, dt.date.today().year]):

    if citation_score_per_jurisdiction:
        return _get_citation_score_per_jurisdiction(dataframe,
            year_column=year_column,
            skip_years=skip_years)
    else:
        return _get_citation_score_not_per_jurisdiction(dataframe,
            year_column=year_column,
            skip_years=skip_years)
    

def _get_citation_score_not_per_jurisdiction(dataframe,
        year_column=EARLIEST_PUBLICATION_YEAR_COL,
        skip_years=[dt.date.today().year-2, dt.date.today().year-1, dt.date.today().year]):

    citation_scores = pd.Series(index=dataframe.index, dtype="object")

    mean_citations_per_year = dataframe.groupby(year_column)[FAMILY_CITED_PATENT_COUNT_COL].mean()
    
    for year in mean_citations_per_year.index:
        if year in skip_years: continue

        mask = dataframe[year_column] == year

        citation_scores_sub = (dataframe.loc[mask, FAMILY_CITED_PATENT_COUNT_COL]+1)/\
            (mean_citations_per_year[year]+1)

        citation_scores[dataframe.loc[mask].index] = citation_scores_sub

    return citation_scores   
    
def _get_citation_score_per_jurisdiction(dataframe,
        year_column=EARLIEST_PUBLICATION_YEAR_COL,
        skip_years=[dt.date.today().year-2, dt.date.today().year-1, dt.date.today().year]):

    citation_scores = pd.Series(index=dataframe.index, dtype="object")

    mean_citations_per_year_per_jurisdiction = _get_mean_citations_per_year_per_jurisdiction(dataframe,  
        year_column=year_column)

    years = dataframe[year_column].unique()
    for year in years:
        if year in skip_years: continue
        if np.isnan(year): continue
        dataframe_in_year = dataframe[dataframe[year_column] == year]
        citation_scores[dataframe_in_year.index] =  dataframe_in_year[CITED_PER_JURISDICTION_COL].apply(_get_citation_score, 
            citations_per_jurisdiction=mean_citations_per_year_per_jurisdiction[year])
    return citation_scores

def _get_mean_citations_per_year_per_jurisdiction(dataframe,  
        year_column=EARLIEST_PUBLICATION_YEAR_COL):
    years = dataframe[year_column].unique()
    citations_dict = {}
    for year in years:
        dataframe_in_year = dataframe[dataframe[year_column] == year]
        citation_counters = dataframe_in_year[CITED_PER_JURISDICTION_COL].apply(_get_citations_per_jurisdiction)
        document_counters = dataframe_in_year[JURISDICTIONS_COL].apply(_get_documents_per_jurisdiction)
        citations_dict[year] = (pd.Series(citation_counters.sum())/pd.Series(document_counters.sum())).fillna(0)
    return citations_dict

def _get_citations_per_jurisdiction(dict_string):
    return Counter({s[:2]:int(s[3:]) for s in dict_string.split(SEPARATOR)})

def _get_documents_per_jurisdiction(jurisdictions):
    return Counter({s:1 for s in jurisdictions.split(SEPARATOR)})

def _get_citation_score(dict_string, citations_per_jurisdiction={}):
    return np.mean([(int(s[3:])+1)/(citations_per_jurisdiction[s[:2]]+1) for s in dict_string.split(SEPARATOR)])
    
def _get_all_jurisdictions(jurisdictions):
    jurisdictions_df = jurisdictions.str.split(SEPARATOR, expand=True)
    all_jurisdictions = set()
    for column in jurisdictions_df.columns:
        all_jurisdictions |= set(list(jurisdictions_df[column].unique()))
    return all_jurisdictions


