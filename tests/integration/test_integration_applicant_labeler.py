import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, dataframes_equal
from lens_analysis import applicant_labeler as al

TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)
TEST_APPLICANTS_NL = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_nl.xlsx", index_col=0)
TEST_APPLICANTS_LABELED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_labels.xlsx", index_col=0)
TEST_APPLICANTS_LABELED_NL = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_labels_nl.xlsx", index_col=0)
TEST_APPLICANTS_LABELED_TW = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_labels_tw.xlsx", index_col=0)
TEST_APPLICANT_TYPES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicant_types.xlsx", index_col=0)

def test_add_labels_standard():
    applicants_labeled = al.add_labels(TEST_APPLICANTS)
    applicants_labeled.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants_labels.xlsx")
    assert dataframes_equal(applicants_labeled, TEST_APPLICANTS_LABELED)

def test_add_labels_nl():
    applicants_labeled_nl = al.add_labels(TEST_APPLICANTS_NL, labeler = al.NL_LABELER)
    applicants_labeled_nl.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants_labels_nl.xlsx")
    assert dataframes_equal(applicants_labeled_nl, TEST_APPLICANTS_LABELED_NL)

def test_add_labels_tw():
    applicants_labeled_tw = al.add_labels(TEST_APPLICANTS, labeler = al.TW_LABELER)
    applicants_labeled_tw.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants_labels_tw.xlsx")
    assert dataframes_equal(applicants_labeled_tw, TEST_APPLICANTS_LABELED_TW)

def test_aggregate_to_applicant_types():
    applicant_types = al.aggregate_to_applicant_types(TEST_APPLICANTS_LABELED)
    applicant_types.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicant_types.xlsx")
    assert dataframes_equal(applicant_types, TEST_APPLICANT_TYPES)
