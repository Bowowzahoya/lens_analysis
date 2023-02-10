import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, dataframes_equal
from lens_analysis import families as fm

TEST_LENS_EXPORT = pd.read_csv(RESOURCES_FOLDER+"lens-8-ai-and-nanotech_with_legal_status.csv", index_col=0)
TEST_FAMILIES_EXTENDED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families_no-missing-priority.xlsx", index_col=0)
TEST_FAMILIES_RAW_LEGAL = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families_not_extended_with_legal_status.xlsx", index_col=0)
TEST_FAMILIES_RAW= pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families_not_extended.xlsx", index_col=0)

families_raw = fm.aggregate_to_family(TEST_LENS_EXPORT)
families_raw.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-families_not_extended.xlsx")

def test_aggregate_to_family():
    assert dataframes_equal(families_raw, TEST_FAMILIES_RAW)

families_extended = fm.add_extra_family_information(TEST_FAMILIES_RAW.copy(), year_for_citations=2022)
families_extended.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-families.xlsx")

def test_add_extra_family_information():
    assert dataframes_equal(families_extended, TEST_FAMILIES_EXTENDED)
