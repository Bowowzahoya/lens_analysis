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
GLOBAL_COV = pd.read_csv(DAT_DIR+"market-cov.csv", index_col=0)

def _get_mark_cov(jur, yr):
    """"
    Get the coverage of the jurisdiction jur GDP for year yr
    Where 1.0 is the GDP of the USA.
    """
    if str(yr) not in GLOBAL_COV.columns and int(yr) > 2000:
        yr = 2018
    elif str(yr) not in GLOBAL_COV.columns and int(yr) < 2000:
        yr = 1960
        
    try:
        cov = GLOBAL_COV.loc[jur, str(yr)]
        # if not found, pick first available at a later year
        while not(cov >= 0):
            yr += 1
            cov = GLOBAL_COV.loc[jur, str(yr)]
    except:
        # error in jurisdiction format
        print(f"Jurisdiction not recognized: {jur}.")
        cov = 0
    return cov


def _sum_mark_cov(row, jur_col=JURS_COL, pb_yr_col=ERL_PY_COL, 
                 typ_col=TYPS_COL, app_pen=0.7):
    """Sum market coverages of all jurisdictions"""
    jurs = row[jur_col].split(SEP)
    yr = row[pb_yr_col]
    typs = row[typ_col]
    
    weights = [_get_mark_cov(jur, yr) for jur in jurs]
    mcov = sum(weights)/_get_mark_cov("US", yr)
    if "Granted Patent" not in typs:
        mcov *= app_pen
        
    return mcov
   

def calc_mark_cov(fam, jur_col=JURS_COL, pb_yr_col=ERL_PY_COL, 
                  typ_col=TYPS_COL, app_pen=0.7):
    """
    Calculates the market coverage of patent families
    
    Parameters:
        - fam, DataFrame of patent families with index sorted priority number
        - jur_col (optional): str, name of the Jurisdictions column
        default JURS_COL from constants module
        - pb_yr_col (optional): str, name of the Publication Year column
        default ERL_PY_COL from constants module
        - typ_col (optional): str, name of the Type column
        default TYP_COL from constants module
        - app_pen (optional): float, penalty for patents
        that are still wholly in application phase.
        Note: this will mean the whole patent family will not be penalized
        anymore as soon as only one of the jurisdiction has granted
        the patent.
        
    Returns:
        - fam, DataFrame of patent families with updated
        market coverage column.
    """
    fam[MCOV_COL] = fam.apply(_sum_mark_cov, axis=1)

    return fam    