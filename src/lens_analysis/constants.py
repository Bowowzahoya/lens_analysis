# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:46:57 2021
Constants used in the rest of the modules
@author: David
"""

# separators
SEPARATOR = ";;"
BIG_SEPARATOR = ";,;,"

# export column names:
POUND_COL = "#"
JURISDICTION_COL = "Jurisdiction"
KIND_COL = "Kind"
PUBLICATION_NUMBER_COL = "Display Key"
LENS_ID_COL = "Lens ID"
PUBLICATION_DATE_COL = "Publication Date"
PUBLICATION_YEAR_COL = "Publication Year"
APPLICATION_NUMBER_COL = "Application Number"
APPLICATION_DATE_COL = "Application Date"
PRIORITY_NUMBERS_COL = "Priority Numbers"
EARLIEST_PRIORITY_DATE_COL = "Earliest Priority Date"
TITLE_COL = "Title"
ABSTRACT_COL = "Abstract"
APPLICANTS_COL = "Applicants"
INVENTORS_COL = "Inventors"
OWNERS_COL = "Owners"
URL_COL = "URL"
DOCUMENT_TYPE_COL = "Document Type"
HAS_FULL_TEXT_COL = "Has Full Text"
CITES_PATENT_COUNT_COL = "Cites Patent Count"
CITED_PATENT_COUNT_COL = "Cited by Patent Count"
SIMPLE_FAMILY_SIZE_COL = "Simple Family Size"
EXTENDED_FAMILY_SIZE_COL = "Extended Family Size"
SEQUENCE_COUNT_COL = "Sequence Count"
CPC_CLASSIFICATIONS_COL = "CPC Classifications"
IPCR_CLASSIFICATIONS_COL = "IPCR Classifications"
US_CLASSIFICATIONS_COL = "US Classifications"
CITED_NPL_COUNT_COL = "NPL Citation Count"
RESOLVED_CITED_NPL_COUNT_COL = "NPL Resolved Citation Count"
RESOLVED_CITED_NPL_LENS_IDS_COL = "NPL Resolved Lens ID(s)"
RESOLVED_CITED_NPL_EXTERNAL_IDS_COL = "NPL Resolved External ID(s)"
NPL_CITATIONS_COL = "NPL Citations"

# fixed export entries
GRANTED_PATENT_ENTRY = "Granted Patent"
WO_JURISDICTION_ENTRY = "WO"
US_JURISDICTION_ENTRY = "US"

# families self-defined column names
JURISDICTIONS_COL = "Jurisdictions"
KINDS_COL = "Kinds"
GRANTED_JURISDICTIONS_COL = "Granted Jurisdictions"
PUBLICATION_NUMBERS_COL = "Publication Numbers"
LENS_IDS_COL = "Lens IDs"
EARLIEST_PUBLICATION_DATE_COL = "Earliest Publication Date"
EARLIEST_PUBLICATION_YEAR_COL = "Earliest Publication Year"
APPLICATION_NUMBERS_COL = "Application Numbers"
EARLIEST_APPLICATION_DATE_COL = "Earliest Application Date"
SORTED_PRIORITY_NUMBERS_COL = "Sorted Priority Numbers"
EARLIEST_PRIORITY_YEAR_COL = "Earliest Priority Year"
TITLES_COL = "Titles"
FIRST_ABSTRACT_COL = "First Abstract"
URLS_COL = "URLs"
DOCUMENT_TYPES_COL = "Document Types"
IS_GRANTED_COL = "Has Granted Family Member"
FAMILY_CITES_PATENT_COUNT_COL = "Total Cites Patent Count of Family"
FAMILY_CITED_PATENT_COUNT_COL = "Total Cited by Patent Count of Family"
INCLUDED_SIMPLE_FAMILY_SIZE_COL = "Simple Family Size in Original Lens Export"
WEIGHT_PER_APPLICANT_COL = "Weight per Applicant"
MARKET_COVERAGE_COL = "Market Coverage"
PATENT_POWER_COL = "Patent Power"
IS_TOP_PATENT_COL = "Is Top Patent"
PRIORITY_JURISDICTIONS_COL = "Priority Jurisdictions"
CITATION_SCORE_COL = "Citation Score"

# applicant self-defined column names
FRACTIONAL_COL_EXTENSION = "(Fractionally Counted)"
APPLICANT_COL = "Applicant"
ALIASED_APPLICANT_COL = "Standardized Applicant Name"
FAMILIES_COUNT_COL = "Number of Simple Patent Families"
FRACTIONAL_FAMILIES_COUNT_COL = FAMILIES_COUNT_COL+FRACTIONAL_COL_EXTENSION
MAIN_PRIORITY_JURISDICTION_COL = "Main Priority Jurisdiction"
MEAN_CITATION_SCORE_COL = "Mean Citation Score"
MEAN_MARKET_COVERAGE = "Mean Market Coverage"
MEAN_PATENT_POWER = "Mean Patent Power"
TOP_PATENTS_COL = "Top Patents"
FRACTIONAL_TOP_PATENTS_COL = TOP_PATENTS_COL+FRACTIONAL_COL_EXTENSION
IS_INVENTOR_COL = "Is Inventor"
JOINT_PATENTS_WITH_COL = "Joint Patents With"



