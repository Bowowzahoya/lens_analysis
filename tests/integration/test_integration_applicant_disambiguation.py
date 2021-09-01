import pandas as pd
import numpy as np

from integration_context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, assert_dataframes_equal
from lens_analysis import applicant_disambiguation as ad

TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-applicants.xlsx", index_col=0)
ALIASES_TEST = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech_aliases.xlsx", index_col=0, squeeze=True)

aliases = ad.guess_aliases(TEST_APPLICANTS, TEST_APPLICANTS.index[0:10], custom_aliases={})
aliases.to_excel(OUTPUT_FOLDER+"ai-and-nanotech_aliases.xlsx")

def test_aliases():
    assert all(aliases.index == ALIASES_TEST.index)
    assert all(aliases.values == ALIASES_TEST.values)

