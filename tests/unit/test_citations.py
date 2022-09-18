import pandas as pd
import numpy as np
import os

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import citations as ct

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families_not_extended.xlsx", index_col=0)

def test_get_citation_score():
    citation_scores = ct.get_citation_score(TEST_FAMILIES, skip_years=[2019,2020,2021], citation_score_per_jurisdiction=False)
    assert len(citation_scores.dropna()) == 51
    assert round(citation_scores["US 201762520167 P"], 2) == 0.47

def test_get_mean_citations_per_year_per_jurisdiction():
    cits_dict = ct._get_mean_citations_per_year_per_jurisdiction(TEST_FAMILIES)
    assert cits_dict[2019]["US"] == 1.5
    assert cits_dict[2019]["AU"] == 0

def test_get_citations_per_jurisdiction():
    dict_string = "US:0;;NL:12;;CN:3"
    citations_dict = ct._get_citations_per_jurisdiction(dict_string)
    assert citations_dict["NL"] == 12

def test_get_all_jurisdictions():
    jurs = ct._get_all_jurisdictions(TEST_FAMILIES["Jurisdictions"])
    assert {'IL', 'FR', 'JP', None, 'SG', 'ZA', 'DE', 'CN', 'CA', 'KR', 'US', 'RU', 'AU', 'WO', 'GB', 'EP', 'TW'} == jurs

def test_get_citation_score():
    dict_string = "US:0;;NL:12;;CN:3"
    citations_per_jurisdiction = {"US":5, "NL":12, "CN":1}
    citation_score = ct._get_citation_score(dict_string, citations_per_jurisdiction=citations_per_jurisdiction)
    assert round(citation_score, 2) == 1.06

def test_get_citation_score_per_jurisdiction():
    citation_scores = ct.get_citation_score(TEST_FAMILIES, skip_years=[2019,2020,2021], citation_score_per_jurisdiction=True)
    citation_scores.to_excel(OUTPUT_FOLDER+"citation scores.xlsx")
    assert len(citation_scores.dropna()) == 51
    assert round(citation_scores["CN 201610872541 A"], 2) == 2.35