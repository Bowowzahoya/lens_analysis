# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:25:32 2021

@author: David
"""
import pandas as pd

from .constants import *

def guess_aliases(applicants_dataframe, applicants_to_alias, custom_aliases={}):
    """
    merge_apps: dict of key applicant
    with value a list of applicants to be merged

    """
    SERIES_NAME = "Alias"
    INDEX_NAME = "Name"

    alias_series = pd.Series(name = SERIES_NAME)
    alias_series.index.name = INDEX_NAME

    company_forms = pd.read_excel(ALL_COMPANY_FORMS_FILENAME, index_col=0)
    
    for applicant in applicants_to_alias:
        joint_applicants = applicants_dataframe.loc[applicant, JOINT_PATENTS_WITH_COL]
        joint_applicants = joint_applicants.split(SEPARATOR)

        # occurs anywhere inside?
        more_applicants = find_extended_form_of_app(remove_common_terms(applicant, company_forms),
            applicants_dataframe.index)
        joint_applicants += more_applicants
        
        # check custom_alias:
        if applicant in custom_aliases.keys():
            custom_alias = custom_aliases[applicant]
            applicant_name = normal_case(custom_alias)
            more_applicants = find_extended_form_of_app(custom_alias, applicants_dataframe.index)
            joint_applicants += more_applicants
        else:
            applicant_name = normal_case(applicant)
        
        joint_applicants = sorted(set(joint_applicants))
        new_aliases = pd.Series(index=joint_applicants, data=applicant_name)
        
        no_overlap_index = [ix for ix in new_aliases.index if ix not in alias_series]
        new_aliases = new_aliases.loc[no_overlap_index]
        new_aliases.name = SERIES_NAME
        new_aliases.index.name = INDEX_NAME
        
        alias_series = alias_series.append(new_aliases)
        
    return alias_series
        
        
def normal_case(s):
    words = s.split(" ")
    for ix, word in enumerate(words):
        if len(word) > 1:
            words[ix] = word[0].upper()+word[1:].lower()
        
    return " ".join(words)

def find_extended_form_of_app(app_to_find, apps):
    return [app for app in apps if app_to_find in app]

def remove_common_terms(applicant, common_terms):
    applicant_words = applicant.split(" ")
    for term in common_terms:
        if term in applicant_words:
            applicant_words.remove(term)
    return " ".join(applicant_words)
    
        
        