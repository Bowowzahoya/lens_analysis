import pandas as pd
import numpy as np

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import applicants as ap

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)

def test_get_aliases():
    aliases = pd.Series({"IBM UK":"IBM", "IBM CO LTD":"IBM"})
    applicants = pd.Series({0:"IBM", 1:"IBM UK", 2:"TOMAHAWK INC"})
    aliased_applicants = ap._get_aliases(applicants, aliases)
    assert aliased_applicants[0] == "IBM"
    assert aliased_applicants[1] == "IBM"
    assert aliased_applicants[2] == "TOMAHAWK INC"

def test_one_hot_encode_years():
    families_add_on = ap._one_hot_encode_years(TEST_FAMILIES.iloc[0:4])
    assert families_add_on.iloc[0]["2015"] == 1
    assert families_add_on.iloc[1]["2015"] == 1
    assert families_add_on.iloc[2]["2016"] == 1
    assert families_add_on.iloc[3]["2017"] == 1

def test_merge_to_applicants():
    applicants = ap.merge_to_applicants(TEST_FAMILIES)
    applicants.to_excel(OUTPUT_FOLDER+"applicants_df.xlsx")

test_merge_to_applicants()