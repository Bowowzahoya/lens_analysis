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
from .constants import CIT_COL, TOT_CIT_COL, PY_COL, ERL_PY_COL, MNCS_COL
import datetime as dt


def calc_mncs(fam, cit_col=TOT_CIT_COL, pb_yr_col=ERL_PY_COL,
              skip_years=[dt.date.today().year-2, dt.date.today().year-1, dt.date.today().year]):
    """
    Calculates the normalized citation score of a df of families
    
    Parameters:
        - fam: DataFrame of families with index unique priority number
        - cit_col (optional): name of the column with citation values
        default TOT_CIT_COL as defined in constants
        - pb_yr_col (optional): name of the column with publication year
        default ERL_PY_COL as defined in constants
        - skip_years (optional): years not to take along, default last
        three years (as citation not mature enough)
        
    Returns:
        fam: DataFrame with mean normalized citation score column added
    """
    cit_py = fam.groupby(pb_yr_col)[cit_col].mean() # averages
    
    for yr in cit_py.index:
        if yr in skip_years: continue
        mncs = (fam.loc[fam[pb_yr_col] == yr, cit_col]+1)/(cit_py[yr]+1)
        fam.loc[fam[pb_yr_col] == yr, MNCS_COL] = mncs
    return fam

    
    
    
    