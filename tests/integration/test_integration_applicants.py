import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, dataframes_equal
from lens_analysis import applicants as ap

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)
TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)
ALIASES_ADAPTED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech_aliases_adapted.xlsx", index_col=0, squeeze=True)
TEST_APPLICANTS_ALIASED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants_aliased.xlsx", index_col=0, squeeze=True)

applicants = ap.aggregate_to_applicants(TEST_FAMILIES)
applicants.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants.xlsx")

applicants_aliased = ap.aggregate_to_applicants(TEST_FAMILIES, aliases=ALIASES_ADAPTED)
applicants_aliased.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants_aliased.xlsx")

def test_aggregate_to_applicants():
    assert dataframes_equal(applicants, TEST_APPLICANTS)

test_aggregate_to_applicants()

def test_aggregate_to_applicants_aliased():
    assert dataframes_equal(applicants_aliased, TEST_APPLICANTS_ALIASED)

test_aggregate_to_applicants_aliased()