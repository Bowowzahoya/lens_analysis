# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021

Functionality for retrieving the country of origin of an applicant.
This only works for China and the Netherlands

Main functions:
    - is_cn() takes a row from a families dataframe
    and returns "CN" if most likely belongs to a Chinese applicant,
    None otherwise.
    - is_nl() does the same for Dutch applicants
    Note that a number of companies have been removed
    that are only classified as Dutch by the Epodoc classification 
    since they are registered in NL for tax evasion purposes, 
    but don't actually do their main R&D there, such as
    Schlumberger, Nike, Sabic.
    - is_eu() works on the basis of placenames, priority jurisdiction
    - is_us() works on the basis of main priority jurisdiction

@author: David
"""
import pandas as pd
from itertools import chain
from collections import defaultdict
from .constants import *
from .utilities import join, join_set, join_max, join_sum, join_earliest 
from .utilities import join_size, join_cols, join_mean, join_most
import os

DAT_DIR = os.path.join(os.path.dirname(__file__),"res/countries/")
CN_CTY = pd.read_excel(DAT_DIR+"cn-cities.xlsx", squeeze=True, header=None)
CN_PRV = pd.read_excel(DAT_DIR+"cn-provinces.xlsx", squeeze=True, header=None)
CN_APPS = pd.read_excel(DAT_DIR+"cn-apps.xlsx", squeeze=True, header=None)
CN_ACAD = pd.read_excel(DAT_DIR+"cn-acads.xlsx", squeeze=True, header=None)
CN_TERMS = pd.read_excel(DAT_DIR+"cn-terms.xlsx", squeeze=True, header=None)

NL_APPS = pd.read_excel(DAT_DIR+"nl-apps.xlsx", squeeze=True, header=None)
NL_TERMS = pd.read_excel(DAT_DIR+"nl-terms.xlsx", squeeze=True, header=None)
NL_TAX_EVADERS = pd.read_excel(DAT_DIR+"nl-tax-evaders.xlsx", squeeze=True, header=None)

EU_JURS = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "EU", "FI", 
           "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", 
           "PL", "PT", "RO", "SE", "SI", "SK"]

EU_TERMS = pd.read_excel(DAT_DIR+"eu-terms.xlsx", squeeze=True, header=None)
EU_COMPS = pd.read_excel(DAT_DIR+"eu-companies.xlsx", squeeze=True, header=None)
EU_COMP_TERMS = pd.read_excel(DAT_DIR+"eu-company-forms.xlsx", squeeze=True, 
                              header=None)

def _contains_word(word, str_sr):
    """
    Fast method to check if exactly whole word 'word' is contained in 'str_sr'
    That is: word=ai, str_sr=air pressure will return False, 
    but word=ai, str_sr=responsible ai, will return True
    """
    word = " "+word+" "
    str_sr = " "+str_sr+" "
    return str_sr.apply(lambda x: x in word).any()

def is_cn(row):
    """
    Check if an applicant is Chinese
    
    Returns "CN" if applicant is Chinese
    
    Parameters:
        row: Series which contains app_col, and has a priority number as index
        applicant in row needs to be a single applicant
        
    Returns: "CN" if Chinese, None otherwise
    """
    app = row.name
    
    if not isinstance(app, str):
        return False
    
    if app in CN_APPS.values:
        return True
    
    if app in CN_ACAD.values:
        return True
    
    if _contains_word(app, CN_PRV):
        return True
    
    if _contains_word(app, CN_CTY):
        return True
    
    if _contains_word(app, CN_TERMS):
        return True
    
    prios = row.name
    if "CN" in row[MJUR_COL]:
        return True
    
    return False
    
def is_nl(row):
    """
    Check if an applicant is Dutch
    
    Returns "NL" if applicant is Dutch
    
    Parameters:
        row: Series which contains app_col, and has a priority number as index
        applicant in row needs to be a single applicant
        
    Returns: "NL" if Dutch, None otherwise
    """
    app = row.name
    
    if not isinstance(app, str):
        return False
    
    if app in NL_TAX_EVADERS.values:
        return False
    
    if app in NL_APPS.values:
        return True
    
    if _contains_word(app, NL_TERMS):
        return True
    
    prios = row.name
    if "NL" in row[MJUR_COL]:
        return True
    
    return False
    
def is_eu(row):
    app = row.name
    
    if not isinstance(app, str):
        return False
    
    if _contains_word(app, EU_TERMS):
        return True
    
    if _contains_word(app, EU_COMPS):
        return True
    
    if _contains_word(app, EU_COMP_TERMS):
        return True
    
    prios = row.name
    for eu_jur in EU_JURS:
        if eu_jur in row[MJUR_COL]:
            return True
    
    return False
        
def is_us(row):
    app = row.name
    if not isinstance(app, str):
        return False

    if "US" in row[MJUR_COL]:
        return True

    return False
    


    
    
    
    