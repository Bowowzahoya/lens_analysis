import pandas as pd
import numpy as np
import os

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import families as fm


TEST_LENS_EXPORT = pd.read_csv(RESOURCES_FOLDER+"lens-8-ai-and-nanotech.csv", index_col=0)
TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)
DEFAULT_EXPORT_COLUMNS = set([fm.DEFAULT_CONVERSION_FUNCTION_DICT[ix][0] for ix in fm.DEFAULT_CONVERSION_FUNCTION_DICT.keys()])

def test_sort_priority_numbers():
    priority_numbers = "NL 0009810/0;;NL3429181;;NL389"
    output1 = fm._sort_priority_numbers(priority_numbers)

    priority_numbers = "NL3429181;;NL 0009810/0;;NL389"
    output2 = fm._sort_priority_numbers(priority_numbers)

    assert output1 == output2

def test_merge_to_family():
    families = fm.merge_to_family(TEST_LENS_EXPORT)
    assert len(families) == 185
    assert set(families.columns) == DEFAULT_EXPORT_COLUMNS

def test_get_jurisdictions_from_number():
    priority_number = "IL 2018050149 W;;US 201762456781 P;;US 201816484490 A" 
    jurisdictions = fm.get_jurisdictions_from_number(priority_number)
    assert set(jurisdictions) == set(["IL","US"])

def test_add_extra_family_information():
    families = fm.add_extra_family_information(TEST_FAMILIES)
    families.to_excel(OUTPUT_FOLDER+"families_df.xlsx")

test_add_extra_family_information()