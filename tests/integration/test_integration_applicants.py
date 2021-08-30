import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, are_dataframes_equal
from lens_analysis import applicants as ap

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)
TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)

applicants = ap.aggregate_to_applicants(TEST_FAMILIES)
applicants.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants.xlsx")

def test_aggregate_to_families():
    are_dataframes_equal(applicants, TEST_APPLICANTS)