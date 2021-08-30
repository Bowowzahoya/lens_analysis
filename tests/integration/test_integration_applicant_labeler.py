import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, are_dataframes_equal
from lens_analysis import applicant_labeler as al

TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)
TEST_APPLICANTS_LABELED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_labels.xlsx", index_col=0)
TEST_APPLICANT_TYPES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicant_types.xlsx", index_col=0)

applicants_labeled = al.add_labels(TEST_APPLICANTS)
applicants_labeled.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants_labels.xlsx")

def test_add_labels():
    are_dataframes_equal(applicants_labeled, TEST_APPLICANTS_LABELED)


applicant_types = al.aggregate_to_applicant_types(TEST_APPLICANTS_LABELED)
applicant_types.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicant_types.xlsx")

def test_aggregate_to_applicant_types():
    are_dataframes_equal(applicant_types, TEST_APPLICANT_TYPES)
