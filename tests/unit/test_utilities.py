import pandas as pd
import numpy as np
import re

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
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

def test_join_size_not_nan():
    joined_column = ut.join_size_not_nan(COLUMN_NUMBERS)
    print(joined_column)
    assert joined_column == 7

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

def test_join_size_not_nan_nans():
    joined_column = ut.join_size_not_nan(COLUMN_NANS)
    assert joined_column == 0

# test join_columns and conversion functions
def test_join_columns():
    dataframe_compressor = ut.DataFrameCompressor([\
                    (ut.join_set, "text_col", "text_index"),
                    (ut.join_max, "number_col", "number_index")])
    sr = ut.join_columns(TEST_DF, dataframe_compressor)
    assert len(sr) == 2
    assert "text_index" in sr.index
    assert "number_index" in sr.index
    assert "text_col" not in sr.index
    assert sr["number_index"] == 2

def test_compression_function_get_in_out_pairs():
    df = pd.DataFrame({0:{"2010":1, "2011":0, "weight column":1},
                    1:{"2010":0, "2011":1, "weight column":0.5},
                    2:{"2010":0, "2011":1, "weight column":1}}).transpose()
    column_in = re.compile("[0-9]{4}")
    column_out = lambda s: s+" (fractionally counted)"
    compression_function = ut.CompressionFunction(ut.join_sum, column_in, column_out)
    in_out_pairs = list(compression_function.get_in_out_pairs(df))
    assert in_out_pairs[0] == ('2010', '2010 (fractionally counted)')
    assert in_out_pairs[1] == ('2011', '2011 (fractionally counted)')

def test_compression_function_convert_one():
    df = pd.DataFrame({0:{"column in":1, "weight column":1}, 
                    1:{"column in":2, "weight column":2}}).transpose()
    compression_function = ut.CompressionFunction(ut.join_sum, "column in", "column out")
    value = compression_function.convert_one(df, "column in")
    assert value == 3

def test_compression_function_convert_one_weighted():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":0.5}}).transpose()
    compression_function = ut.CompressionFunction(ut.join_sum, "column in", "column out", 
                                                weight_column_name="weight column")
    value = compression_function.convert_one(df, "column in")
    assert value == 6

def test_compression_function_convert_one_weighted_mean():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":2}}).transpose()
    compression_function = ut.CompressionFunction(ut.join_mean, "column in", "column out", 
                                                weight_column_name="weight column")
    value = compression_function.convert_one(df, "column in")
    assert value == 3

def test_compression_function_convert_one_weighted_mean_nan():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":2},
                    3:{"column in":np.nan, "weight column":3}}).transpose()
    compression_function = ut.CompressionFunction(ut.join_mean, "column in", "column out", 
                                                weight_column_name="weight column")
    value = compression_function.convert_one(df, "column in")
    assert value == 3

def test_compression_function_convert_one_weighted_size():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":2},
                    2:{"column in":np.nan, "weight column":3}}).transpose()
    compression_function = ut.CompressionFunction(ut.join_size_not_nan, "column in", "column out", 
                                                weight_column_name="weight column")
    value = compression_function.convert_one(df, "column in")
    assert value == 3

def test_compression_function_convert_multiple():
    df = pd.DataFrame({0:{"2010":1, "2011":0, "weight column":1},
                    1:{"2010":0, "2011":1, "weight column":0.5},
                    2:{"2010":0, "2011":1, "weight column":1}}).transpose()
    column_in = re.compile("[0-9]{4}")
    column_out = lambda s: s+" (fractionally counted)"
    compression_function = ut.CompressionFunction(ut.join_sum, column_in, column_out, weight_column_name="weight column")
    values = compression_function.convert(df)
    assert all(values == pd.Series({"2010 (fractionally counted)":1, "2011 (fractionally counted)":1.5}))
    
def test_dataframe_compressor_convert_weighted():
    df = pd.DataFrame({0:{"column in":5, "column in2":3, "weight column":1}, 
                    1:{"column in":2, "column in2":4, "weight column":2}}).transpose()
    dataframe_compressor = ut.DataFrameCompressor(\
        [(ut.join_sum, "column in", "column out weighted", {"weight_column_name":"weight column"}),
        (ut.join_mean, "column in2", "column out2"),
        (ut.join_sum, "column in", "column out")])
    sr = dataframe_compressor.convert(df)
    assert all(sr == pd.Series({"column out weighted": 9, "column out2": 3.5, "column out":7}))

def test_dataframe_compressor_convert_re():
    dataframe_compressor = ut.DataFrameCompressor([
        (ut.join_sum, re.compile("^[0-9]{4}"+" (extension)".replace("(", "\(").replace(")","\)")+"$"), lambda x: x)])
    
    dataframe = pd.DataFrame(
        {0:{"2010 (extension)":1, "2011":2, "2012 (extension) junk":3},
        1:{"2010 (extension)":2, "2011":3, "2012 (extension) junk":3}}).transpose()

    series = dataframe_compressor.convert(dataframe)
    assert all(series == pd.Series({"2010 (extension)":3}))

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

# applicant utilities
def test_unfold_cell_overloaded_column():
    df = pd.DataFrame({1:{"Applicants":"IBM UK;;IBM", "Weight per Applicant":0.5},
                    2:{"Applicants":"IBM UK", "Weight per Applicant":1},
                    3:{"Applicants":"TOMAHAWK INC", "Weight per Applicant":1}}).transpose()
    new_df = ut.unfold_cell_overloaded_column(df, "Applicants", "Applicant")
    assert new_df.loc[1].size == 6
    assert new_df.loc[1, "Weight per Applicant"].sum() == 1
    assert all(new_df.loc[2] == pd.Series({"Applicants":"IBM UK", "Weight per Applicant":1, "Applicant":"IBM UK"}))

def test_unfold_cell_overloaded_column_real_case():
    df = pd.read_excel(RESOURCES_FOLDER+"test-families.xlsx")
    new_df = ut.unfold_cell_overloaded_column(df, "Applicants", "Applicant")
    assert len(new_df) == 11
