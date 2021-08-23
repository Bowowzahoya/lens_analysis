import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import applicants as ap

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)
TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)

applicants = ap.merge_to_applicants(TEST_FAMILIES)

def test_column_names():
    assert (applicants.columns == TEST_APPLICANTS.columns).all()

def test_per_column():
    for column_name in applicants.columns:
        print(f"Testing column {column_name}")
        column = applicants[column_name]
        if column.dtype == "object":
            assert (column.str.len() == TEST_APPLICANTS[column_name].str.len()).all()
        else:
            assert (abs(column - TEST_APPLICANTS[column_name]) < 0.001).all()

applicants.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-applicants.xlsx")