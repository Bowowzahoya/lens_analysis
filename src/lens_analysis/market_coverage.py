# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021
Calculate market coverage for a patent family using
calc_mark_cov()

Market coverage is defined as GDP of covered jurisdicion
divided by GDP of the USA (score of 1.0 for US patents).

Patents that are not granted yet are discounted by a standard
average granting rate of 0.7.

@author: David
"""
import pandas as pd
from itertools import chain
from .constants import *
import datetime as dt
import os

DAT_DIR = os.path.join(os.path.dirname(__file__),"res/")
GLOBAL_GDPS = pd.read_csv(DAT_DIR+"market-cov.csv", index_col=0)

def get_market_coverage(families, application_stage_penalty=0.7, wo_equivalent=1.39):
    market_coverage = families.apply(_get_family_market_coverage, axis=1, 
        application_stage_penalty=application_stage_penalty, wo_equivalent=wo_equivalent)

    return market_coverage

def _get_family_market_coverage(row, application_stage_penalty=0.7, wo_equivalent=1.39):
    # WO equivalent is expected market coverage for an average WO patent that
    # makes it into a granted patent, as roughly calculated from Lens

    jurisdictions = row[JURISDICTIONS_COL].split(SEPARATOR)
    year = row[EARLIEST_PUBLICATION_YEAR_COL]
    types = row[DOCUMENT_TYPES_COL]
    
    gdps = [_get_jurisdiction_gdps(jur, year) for jur in jurisdictions]
    market_coverage = sum(gdps)/_get_jurisdiction_gdps(US_JURISDICTION, year)

    if jurisdictions == [WO_JURISDICTION]:
        market_coverage = wo_equivalent
    elif WO_JURISDICTION in jurisdictions:
        market_coverage = max((wo_equivalent+market_coverage)/2, market_coverage)

    if GRANTED_PATENT_ENTRY not in types:
        market_coverage *= application_stage_penalty
    return market_coverage

def _get_jurisdiction_gdps(jurisdiction, year):
    if str(year) not in GLOBAL_GDPS.columns and int(year) > 2000:
        year = 2018
    elif str(year) not in GLOBAL_GDPS.columns and int(year) < 2000:
        year = 1960
        
    try:
        gdp_coverage= GLOBAL_GDPS.loc[jurisdiction, str(year)]
        # if not found, pick first available at a later year
        while not(gdp_coverage >= 0):
            year += 1
            gdp_coverage = GLOBAL_GDPS.loc[jurisdiction, str(year)]
    except:
        # error in jurisdiction format
        print(f"Jurisdiction not recognized: {jurisdiction}.")
        gdp_coverage = 0
    return gdp_coverage
