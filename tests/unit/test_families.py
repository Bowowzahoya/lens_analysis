import pandas as pd
import numpy as np
import os

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER, dataframes_equal
from lens_analysis import families as fm
from lens_analysis.constants import SEPARATOR


TEST_LENS_EXPORT = pd.read_csv(RESOURCES_FOLDER+"lens-8-ai-and-nanotech.csv", index_col=0)
TEST_LENS_EXPORT2 = pd.read_csv(RESOURCES_FOLDER+"didgeridoo-expanded.csv", index_col=0)
TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)

def test_sort_priority_numbers():
    priority_numbers = "NL 0009810/0;;NL3429181;;NL389"
    output1 = fm._sort_priority_numbers(priority_numbers)

    priority_numbers = "NL3429181;;NL 0009810/0;;NL389"
    output2 = fm._sort_priority_numbers(priority_numbers)

    assert output1 == output2

def test_get_jurisdictions_from_numbers():
    priority_number = "IL 2018050149 W;;US 201762456781 P;;US 201816484490 A" 
    jurisdictions = fm._get_jurisdictions_from_numbers(priority_number)
    assert set(jurisdictions.split(SEPARATOR)) == set(["IL","US"])

def test_get_is_top_patents():
    patent_powers = pd.Series({1:8.9, 2:3, 3:1, 4:2.5, 5:6.5, 6:np.nan, 7:8, 8:4.5, 9:2, 10:11, 11:0, 12:np.nan, 13:4})
    is_top_patents = fm._get_is_top_patents(patent_powers, top_percentage=0.5)
    assert is_top_patents[1] == True
    assert is_top_patents[2] == False
    assert is_top_patents[5] == True
    assert np.isnan(is_top_patents[6])

def test_get_is_top_patents_empty():
    patent_powers = pd.Series(dtype="object")
    is_top_patents = fm._get_is_top_patents(patent_powers, top_percentage=0.5)
    assert all(is_top_patents == pd.Series(dtype="object"))

def test_get_is_top_patents_nan():
    patent_powers = pd.Series({1:np.nan, 2:np.nan, 3:np.nan, 4:np.nan})
    is_top_patents = fm._get_is_top_patents(patent_powers, top_percentage=0.5)
    assert np.isnan(is_top_patents[1])

def test_get_is_top_patents_long():
    patent_powers = TEST_FAMILIES["Patent Power"]
    is_top_patents = fm._get_is_top_patents(patent_powers, top_percentage=0.1)
    top_patents_number = len(is_top_patents[is_top_patents.fillna(False)])
    non_top_patents_number = len(is_top_patents[~is_top_patents.fillna(True)])
    assert top_patents_number == 5
    assert non_top_patents_number == 46

def test_get_is_top_patents_short():
    patent_powers = pd.Series({1:2, 2:3})
    is_top_patents = fm._get_is_top_patents(patent_powers, top_percentage=0.1)
    assert is_top_patents[1] == False

def test_get_priority_years():
    priority_dates = pd.Series({0:np.nan, 1:"2010-02-02", 3:"2017/01/06", 4:"07/12/2019"})
    priority_years = fm._get_years(priority_dates)
    assert np.isnan(priority_years[0])
    assert priority_years[1] == 2010
    assert priority_years[3] == 2017
    assert priority_years[4] == 2019

def test_get_weight_per_applicant():
    applicants = pd.Series({0:"IBM UK;;IBM", 1:np.nan, 2:"", 3:"HUAWEI"})
    weights_per_applicant = fm._get_weight_per_applicant(applicants)
    assert weights_per_applicant[0] == 0.5
    assert weights_per_applicant[2] == 1
    assert weights_per_applicant[3] == 1
    assert np.isnan(weights_per_applicant[1])

def test_get_calculated_family_size():
    
    sizes = fm._get_calculated_family_size(TEST_LENS_EXPORT2["Priority Numbers"])
    assert sizes[1] == 2
    assert sizes[2] == 1

def test_get_imperfect_families_index():
    perfect_index = fm._get_imperfect_families_index(TEST_LENS_EXPORT2, priority_numbers_col="Priority Numbers")
    assert 2 not in perfect_index
    assert 1 in perfect_index
    assert 17 in perfect_index

def test_guess_relevant_priorities_for_imperfect_families():
    df = fm._guess_relevant_priorities_for_imperfect_families(TEST_LENS_EXPORT2, priority_numbers_col="Priority Numbers")
    assert df.loc[6, "Family Relevant Priority Numbers"] == "GB 9812315 A"

def test_guess_relevant_priorities_for_imperfect_family_one_family():
    df = pd.DataFrame({0:{"Priority Numbers":"AU 2001/063561 A;;AU PQ971400 A;;AU 2004/002000 W", "Family Relevant Priority Numbers":"AU 2001/063561 A;;AU PQ971400 A", "Simple Family Size":3},
        1:{"Priority Numbers":"AU 2004/002000 W", "Family Relevant Priority Numbers":"AU 2004/002000 W", "Simple Family Size":3},
        2:{"Priority Numbers":"AU 2001/063561 A;;AU PQ971400 A;;AU 2004/002000 W", "Family Relevant Priority Numbers":"AU 2001/063561 A;;AU PQ971400 A", "Simple Family Size":3}}).transpose()
    
    relevant_priority_numbers = fm._guess_relevant_priorities_for_imperfect_family(df)
    assert (relevant_priority_numbers == "AU 2004/002000 W").all()


