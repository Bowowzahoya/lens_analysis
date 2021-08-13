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


def get_citation_score(dataframe, 
        citation_column=FAMILY_CITED_PATENT_COUNT_COL, 
        year_column=EARLIEST_PUBLICATION_YEAR_COL,
        skip_years=[dt.date.today().year-2, dt.date.today().year-1, dt.date.today().year]):
    # returns dataframe with column added (in place)

    mean_citations_per_year = dataframe.groupby(year_column)[citation_column].mean()

    citation_scores = pd.Series(index=dataframe.index)
    for year in mean_citations_per_year.index:
        if year in skip_years: continue

        mask = dataframe[year_column] == year

        citation_scores_sub = (dataframe.loc[mask, citation_column]+1)/\
            (mean_citations_per_year[year]+1)

        citation_scores[dataframe.loc[mask].index] = citation_scores_sub

    return citation_scores

    
    
    
    