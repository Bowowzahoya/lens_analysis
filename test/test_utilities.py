import pandas as pd
import numpy as np

from context import lens_analysis
from lens_analysis import utilities as ut

# different columns
COLUMN = pd.Series({0:np.nan, 1:"string1;;string1", 2:"string1;;string1", 3:"string3;;string1", 4:None, 5:1, 6:1, 7:2, 8:0})
COLUMN_NUMBERS = pd.Series({0:None, 1:3.5, 2:-1000, 3:1/3., 4:None, 5:1, 6:1, 7:2, 8:0})
COLUMN_DATES = pd.Series({0:np.nan, 1:"2010-02-01", 2:"2010-02-01", 3:None, 4:"2012-02-01", 5:"2010-01-03"})
COLUMN_NANS = pd.Series({0:np.nan})

TEST_DF = pd.DataFrame({1:{"text_col":"string1;;string1","number_col":1.5, "date_col":"2010-01-01"}, 
                        2:{"text_col":"string2;;string3","number_col":1.5, "date_col":"2011-01-01"},
                        3:{"text_col":"string1;;string1","number_col":None, "date_col":"2010-02-01"},
                        4:{"text_col":"string3","number_col":2, "date_col":"2010-01-15"}}).transpose()

# test individual join functions
def test_join():
    joined_column = ut.join(COLUMN)
    assert joined_column == "string1;;string1;,;,string1;;string1;,;,string3;;string1;,;,1;,;,1;,;,2;,;,0"

def test_join_first():
    joined_column = ut.join_first(COLUMN)
    assert joined_column == "string1;;string1"

def test_join_set():
    joined_column = ut.join_set(COLUMN)
    assert set(joined_column.split(";;")) == set("string1;;string3;;1;;2;;0".split(";;"))

def test_join_size():
    joined_column = ut.join_size(COLUMN)
    assert joined_column == 9

def test_join_most():
    joined_column = ut.join_most(COLUMN)
    assert joined_column == "string1"

def test_join_max():
    joined_column = ut.join_max(COLUMN_NUMBERS)
    assert joined_column == 3.5

def test_join_sum():
    joined_column = ut.join_sum(COLUMN_NUMBERS)
    assert round(joined_column,2) == -992.17

def test_join_mean():
    joined_column = ut.join_mean(COLUMN_NUMBERS)
    assert round(joined_column,2) == -141.74

def test_join_earliest():
    joined_column = ut.join_earliest(COLUMN_DATES)
    assert joined_column == "2010-01-03"

def test_join_nans():
    joined_column = ut.join(COLUMN_NANS)
    assert joined_column == ""

def test_join_first_nans():
    joined_column = ut.join_first(COLUMN_NANS)
    assert np.isnan(joined_column)

def test_join_set_nans():
    joined_column = ut.join_set(COLUMN_NANS)
    assert joined_column == ""

def test_join_size_nans():
    joined_column = ut.join_size(COLUMN_NANS)
    assert joined_column == 1

def test_join_most_nans():
    joined_column = ut.join_most(COLUMN_NANS)
    assert np.isnan(joined_column)

def test_join_max_nans():
    joined_column = ut.join_max(COLUMN_NANS)
    assert np.isnan(joined_column)

def test_join_sum_nans():
    joined_column = ut.join_sum(COLUMN_NANS)
    assert joined_column == 0

def test_join_mean_nans():
    joined_column = ut.join_mean(COLUMN_NANS)
    assert np.isnan(joined_column)

def test_join_earliest_nans():
    joined_column = ut.join_earliest(COLUMN_NANS)
    assert np.isnan(joined_column)

# test join_columns
def test_join_columns():
    conversion_function_dict = {"text_col":("text_index", ut.join_set),
                                "number_col":("number_index", ut.join_max)}
    sr = ut.join_columns(TEST_DF, conversion_function_dict)
    assert len(sr) == 2
    assert "text_index" in sr.index
    assert "number_index" in sr.index
    assert "text_col" not in sr.index
    assert sr["number_index"] == 2

# test contains / ends on / starts with
def test_contains_word():
    series_of_words = pd.Series({0:"ai", 1:"artificial intelligence"})
    string = "air is a word"
    assert not ut.contains_word(string, series_of_words)

    string = "ai is another word"
    assert ut.contains_word(string, series_of_words)

    string = "i can also put at the end ai"
    assert ut.contains_word(string, series_of_words)

def test_contains_string():
    series_of_words = pd.Series({0:"公司", 1:"CORP"})
    string = "荷兰公司"
    assert ut.contains_string(string, series_of_words)

    string = "荷兰恭喜"
    assert not ut.contains_string(string, series_of_words)

def test_ends_on_word():
    series_of_words = pd.Series({0:"ai", 1:"artificial intelligence"})
    string = "test the word bai"
    assert not ut.ends_on_word(string, series_of_words)

    string = "test the word ai"
    assert ut.ends_on_word(string, series_of_words)

def test_get_mode_or_modes():
    list_ = [1,1,2,3,4,5,5]
    modes = ut.get_mode_or_modes(list_)
    assert modes == [1,5]

    list_ = [1,1,2,3,4,5,6]
    modes = ut.get_mode_or_modes(list_)
    assert modes == [1]

def test_unfold_cell_overloaded_column():
    df = pd.DataFrame({1:{"Applicants":"IBM UK;;IBM", "Weight per Applicant":0.5},
                    2:{"Applicants":"IBM UK", "Weight per Applicant":1},
                    3:{"Applicants":"TOMAHAWK INC", "Weight per Applicant":1}}).transpose()
    new_df = ut.unfold_cell_overloaded_column(df, "Applicants")
    assert new_df.loc[1].size == 4
    assert new_df.loc[1, "Weight per Applicant"].sum() == 1
    assert all(new_df.loc[2] == pd.Series({"Applicants":"IBM UK", "Weight per Applicant":1}))
