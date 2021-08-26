import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import applicant_labeler as al
from lens_analysis.constants import LEGAL_TYPE_COL, COUNTRY_OF_ORIGIN_COL, APPLICANT_LABEL_COL

TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)
TEST_APPLICANTS_LABELED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_labels.xlsx", index_col=0)
TEST_APPLICANT_TYPES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicant_types.xlsx", index_col=0)

def tst_eu_us_china_labeler():
    labels = TEST_APPLICANTS.apply(al.EU_US_CHINA_LABELER.label, axis=1)
    for column_name in labels.columns:
        print(f"Testing column {column_name}")
        column = TEST_APPLICANTS_LABELED[column_name]
        if column.dtype == "object":
            assert (column.str.len() == TEST_APPLICANTS_LABELED[column_name].str.len()).all()
        else:
            assert (abs(column - TEST_APPLICANTS_LABELED[column_name]) < 0.001).all()

    applicants_labeled = TEST_APPLICANTS.copy()
    applicants_labeled[[COUNTRY_OF_ORIGIN_COL, LEGAL_TYPE_COL]] = labels
    applicants_labeled.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants_labels.xlsx")

applicant_types = al.merge_to_applicant_types(TEST_APPLICANTS)

def test_per_column():
    for column_name in applicant_types.columns:
        print(f"Testing column {column_name}")
        column = applicant_types[column_name]
        if column.dtype == "object":
            assert (column.str.len() == TEST_APPLICANT_TYPES[column_name].str.len()).all()
        else:
            assert (abs(column - TEST_APPLICANT_TYPES[column_name]) < 0.001).all()

test_per_column()

applicant_types.to_excel(OUTPUT_FOLDER+"ai-and-nanotech_applicant_types.xlsx")