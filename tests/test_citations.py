import pandas as pd
import numpy as np
import os

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import citations as ct

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)

def test_get_citation_score():
    citation_scores = ct.get_citation_score(TEST_FAMILIES, skip_years=[2019,2020,2021])
    assert len(citation_scores.dropna()) == 51
    assert round(citation_scores["US 201762520167 P"], 2) == 0.47

test_get_citation_score()