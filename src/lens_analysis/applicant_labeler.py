# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021

Functionality for retrieving the country of origin of an applicant.

@author: David
"""
import os
from collections import OrderedDict

import pandas as pd

from .constants import *
from .utilities import contains_word, contains_string, ends_on_word, has_string
from .utilities import join_columns, APPLICANT_TYPES_DEFAULT_DATAFRAME_COMPRESSOR
from .applicants import _order_applicants_columns


class ApplicantTypeLabeler():
    """
    Labels applicants by type (country of origin, and legal type (company/academia/individual))
    based on the applicant row, using instances of ApplicantTypeIdentifier
    that each have their own associated label pair
    """
    def __init__(self, identifier_label_list, unknown_label=UNKNOWN_LABEL):
        self.identifiers = [x[0] for x in identifier_label_list]
        self.label_pairs = [x[1] for x in identifier_label_list]
        self.unknown_label = unknown_label

    def label(self, row, single_identification=True):
        if not single_identification:
            raise NotImplementedError()

        country_of_origin = self.unknown_label
        legal_type = self.unknown_label
        for identifier, label_pair in zip(self.identifiers, self.label_pairs):
            if identifier.identify(row):
                if country_of_origin == self.unknown_label:
                    country_of_origin = label_pair[0]
                if legal_type == self.unknown_label:
                    legal_type = label_pair[1]
            
            if country_of_origin != self.unknown_label and legal_type != self.unknown_label:
                return pd.Series((country_of_origin, legal_type))

        return pd.Series((country_of_origin, legal_type))

class ApplicantTypeIdentifier():
    """
    Identifies a single type of patent applicant (country of origin, legal type (company/academia/individual))
    based on the applicant row, and functions using reference data 
    that can be preloaded for performance (e.g. known applicants or placename identifiers).
    """
    def __init__(self, identification_functions, *identification_args, args_are_filenames=False):
        """
            identification_functions (list of functions): 
            - Should be functions that accept a string and a second argument.
            reference_data_filenames (list of strings):
            - If arguments for identification function can be anything that works as second argument,
            - If reference files should be .xlsx files with a single column that can be squeezed into a series.
        """
        self.identification_functions = identification_functions
        self.args_are_filenames = args_are_filenames
        self.identification_args = identification_args
        
    @property
    def identification_arguments(self):
        if self.args_are_filenames:
            identification_arguments = []
            for filename in self.identification_args[0]:
                identification_arguments.append(pd.read_excel(filename, squeeze=True, header=None))
            return identification_arguments
        elif len(self.identification_args) == 0:
            return [None]*len(self.identification_functions)
        else:
            return self.identification_args[0]

    def identify(self, row):
        for identification_function, identification_argument in zip(self.identification_functions, self.identification_arguments):
            if identification_function(row, identification_argument):
                return True
        return False


def main_priority_jurisdiction_equals(row, jurisdiction):
    return row[MAIN_PRIORITY_JURISDICTION_COL] == jurisdiction

def applicant_is_inventor(row, *args):
    return row[IS_INVENTOR_COL]

def applicant_contains_word(row, series_of_words):
    """
    Fast method to check if any of a series of words is contained
    exactly in a string
    That is: series_of_words=[ai], string=air pressure will return False, 
    but series_of_words=[ai], str_sr=responsible ai, will return True
    """
    applicant = row.name
    if not isinstance(applicant, str):
        return False
    return contains_word(applicant, series_of_words)

def applicant_contains_string(row, series_of_strings):
    """
    Fast method to check if any of a series of words is contained
    exactly in a string
    That is: series_of_words=[ai], string=air pressure will return False, 
    but series_of_words=[ai], str_sr=responsible ai, will return True
    """
    applicant = row.name
    if not isinstance(applicant, str):
        return False
    return contains_string(applicant, series_of_strings)

def applicant_ends_on_word(row, series_of_words):
    """
    Fast method to check if a string ends with any in a series of words
    """
    applicant = row.name
    if not isinstance(applicant, str):
        return False
    return ends_on_word(applicant, series_of_words)

def applicant_has_string(row, series_of_strings):
    applicant = row.name
    if not isinstance(applicant, str):
        return False
    return has_string(applicant, series_of_strings)


EU_ACADEMIA_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string], [EU_ACADEMIA_FILENAME], args_are_filenames=True)
EU_COMPANIES_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string], [EU_COMPANIES_FILENAME], args_are_filenames=True)
EU_COMPANY_FORMS_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string], [EU_COMPANY_FORMS_FILENAME], args_are_filenames=True)
EU_APPLICANTS_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_contains_word]*2, EU_GEOGRAPHICAL_FILENAMES, args_are_filenames=True)
EU_JURISDICTION_IDENTIFIER = ApplicantTypeIdentifier(
    [main_priority_jurisdiction_equals]*len(EU_JURISDICTIONS),EU_JURISDICTIONS, args_are_filenames=False)
CHINESE_ACADEMIA_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string],[CHINESE_ACADEMIA_FILENAME], args_are_filenames=True)
CHINESE_COMPANY_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string], [CHINESE_COMPANIES_FILENAME],args_are_filenames=True)
CHINESE_APPLICANT_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_contains_word]*3,CHINESE_GEOGRAPHICAL_FILENAMES, args_are_filenames=True)
CHINESE_JURISDICTION_IDENTIFIER = ApplicantTypeIdentifier(
    [main_priority_jurisdiction_equals],[CN_JURISDICTION],args_are_filenames=False)
AMERICAN_ACADEMIA_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string], [AMERICAN_ACADEMIA_FILENAME], args_are_filenames=True)
AMERICAN_COMPANY_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string], [AMERICAN_COMPANIES_FILENAME],args_are_filenames=True)
AMERICAN_APPLICANT_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_contains_word],[AMERICAN_GEOGRAPHICAL_TERMS_FILENAME],args_are_filenames=True)
AMERICAN_JURISDICTION_IDENTIFIER = ApplicantTypeIdentifier(
    [main_priority_jurisdiction_equals],[US_JURISDICTION],args_are_filenames=False)
REST_OF_WORLD_ACADEMIA_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string],[REST_OF_WORLD_ACADEMIA_FILENAME],args_are_filenames=True)
REST_OF_WORLD_COMPANY_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_has_string],[REST_OF_WORLD_COMPANIES_FILENAME],args_are_filenames=True)
REST_OF_WORLD_COMPANY_FORMS_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_contains_word],[REST_OF_WORLD_COMPANY_FORMS_FILENAME],args_are_filenames=True)
REST_OF_WORLD_JURISDICTION_IDENTIFIER = ApplicantTypeIdentifier(
    [main_priority_jurisdiction_equals]*len(REST_OF_WORLD_JURISDICTIONS),REST_OF_WORLD_JURISDICTIONS, args_are_filenames=False)
COMPANY_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_contains_word], [ALL_COMPANY_FORMS_FILENAME], args_are_filenames=True)
INDIVIDUAL_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_is_inventor])
ACADEMIA_IDENTIFIER = ApplicantTypeIdentifier(
    [applicant_contains_word], [ALL_ACADEMIA_TERMS_FILENAME], args_are_filenames=True)

EU_US_CHINA_LABELER = ApplicantTypeLabeler([
    (EU_ACADEMIA_IDENTIFIER, (EU_LABEL, ACADEMIA_LABEL)),
    (EU_COMPANIES_IDENTIFIER, (EU_LABEL, COMPANY_LABEL)),
    (REST_OF_WORLD_ACADEMIA_IDENTIFIER, (REST_OF_WORLD_LABEL, ACADEMIA_LABEL)),
    (REST_OF_WORLD_COMPANY_IDENTIFIER, (REST_OF_WORLD_LABEL, COMPANY_LABEL)),
    (CHINESE_ACADEMIA_IDENTIFIER, (CHINESE_LABEL, ACADEMIA_LABEL)),
    (CHINESE_COMPANY_IDENTIFIER, (CHINESE_LABEL, COMPANY_LABEL)),
    (AMERICAN_ACADEMIA_IDENTIFIER, (AMERICAN_LABEL, ACADEMIA_LABEL)),
    (AMERICAN_COMPANY_IDENTIFIER, (AMERICAN_LABEL, COMPANY_LABEL)),
    (EU_JURISDICTION_IDENTIFIER, (EU_LABEL, UNKNOWN_LABEL)),
    (CHINESE_JURISDICTION_IDENTIFIER, (CHINESE_LABEL, UNKNOWN_LABEL)),
    (EU_COMPANY_FORMS_IDENTIFIER, (EU_LABEL, UNKNOWN_LABEL)),
    (REST_OF_WORLD_COMPANY_FORMS_IDENTIFIER, (REST_OF_WORLD_LABEL, UNKNOWN_LABEL)),
    (EU_APPLICANTS_IDENTIFIER, (EU_LABEL, UNKNOWN_LABEL)),
    (CHINESE_APPLICANT_IDENTIFIER, (CHINESE_LABEL, UNKNOWN_LABEL)),
    (AMERICAN_APPLICANT_IDENTIFIER, (AMERICAN_LABEL, UNKNOWN_LABEL)),
    (AMERICAN_JURISDICTION_IDENTIFIER, (AMERICAN_LABEL, UNKNOWN_LABEL)),
    (REST_OF_WORLD_JURISDICTION_IDENTIFIER, (REST_OF_WORLD_LABEL, UNKNOWN_LABEL)),
    (COMPANY_IDENTIFIER, (UNKNOWN_LABEL, COMPANY_LABEL)),
    (ACADEMIA_IDENTIFIER, (UNKNOWN_LABEL, ACADEMIA_LABEL)),
    (INDIVIDUAL_IDENTIFIER, (UNKNOWN_LABEL, INDIVIDUAL_LABEL))])


def aggregate_to_applicant_types(applicants: pd.DataFrame,
        dataframe_compressor=APPLICANT_TYPES_DEFAULT_DATAFRAME_COMPRESSOR):
    """
    Merges a applicants dataframe into applicant types
    
    Parameters:
        applicants: DataFrame
        dataframe_compressor: DataFrameCompressor
        - Provides how to compress the different columns to a single value per applicant
    Returns:
        applicant_types: DataFrame of applicants with as index the applicant types
    """

    groupby = applicants.groupby(APPLICANT_LABEL_COL)
    
    applicant_types = groupby.apply(join_columns, dataframe_compressor)

    applicant_types = _order_applicant_types_columns(applicant_types)
    applicant_types.sort_values(by=FRACTIONAL_FAMILIES_COUNT_COL, ascending=False, inplace=True)
    return applicant_types

def add_labels(applicants, labeler=EU_US_CHINA_LABELER):
    applicants[[COUNTRY_OF_ORIGIN_COL, LEGAL_TYPE_COL]] = applicants.apply(labeler.label, axis=1)
    applicants[APPLICANT_LABEL_COL] = applicants[COUNTRY_OF_ORIGIN_COL] + " " + applicants[LEGAL_TYPE_COL]
    applicants = _order_applicants_columns(applicants)
    return applicants

def _order_applicant_types_columns(applicant_types):
    ordered_fixed_columns = [column for column in APPLICANT_TYPES_FIXED_ORDERED_COLUMNS if column in applicant_types.columns]

    fractional_yearly_amount_columns = [
        column for column in applicant_types.columns if bool(FRACTIONAL_YEARLY_AMOUNTS_COL_RE_PATTERN.match(column))]

    sorted_columns = ordered_fixed_columns+sorted(fractional_yearly_amount_columns)

    applicant_types = applicant_types[sorted_columns]
    return applicant_types