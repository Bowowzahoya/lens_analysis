
import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import families as fm

TEST_LENS_EXPORT = pd.read_csv(RESOURCES_FOLDER+"lens-8-ai-and-nanotech.csv", index_col=0)
TEST_FAMILIES_EXTENDED = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)
TEST_FAMILIES_RAW = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families_not_extended.xlsx", index_col=0)

families_raw = fm.merge_to_family(TEST_LENS_EXPORT)
families_raw.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-families_not_extended.xlsx")

def test_size():
    assert len(families_raw) == 185

def test_column_names():
    families_raw = fm.merge_to_family(TEST_LENS_EXPORT)
    TEST_FAMILIES_RAW = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families_not_extended.xlsx", index_col=0)
    assert (families_raw.columns == TEST_FAMILIES_RAW.columns).all()

test_column_names()
def test_per_column():
    for column_name in families_raw.columns:
        print(f"Testing column {column_name}")
        column = families_raw[column_name]
        if column.dtype == "object":
            lengths = column.fillna("").str.len()
            lengths[lengths > 32767] = 32767 # maximum string length for pd.read_excel
            test_lengths = TEST_FAMILIES_RAW[column_name].fillna("").str.len()

            assert (lengths == test_lengths).all()
        else:
            assert (abs(column - TEST_FAMILIES_RAW[column_name]) < 0.001).all()

families_raw.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-families_not_extended.xlsx")


families_extended = fm.add_extra_family_information(TEST_FAMILIES_RAW.copy())
families_extended.to_excel(OUTPUT_FOLDER+"ai-and-nanotech-families.xlsx")

