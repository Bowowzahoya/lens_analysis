import pandas as pd
import numpy as np
import re

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import utilities as ut

# different columns
COLUMNS = pd.DataFrame({0:{0:np.nan, 1:"string1;;string1", 2:"string1;;string1", 3:"string3;;string1", 4:None, 5:1, 6:1, 7:2, 8:0}})
COLUMNS_NUMBERS = pd.DataFrame({0:{0:None, 1:3.5, 2:-1000, 3:1/3., 4:None, 5:1, 6:1, 7:2, 8:0}})
COLUMNS_DATES = pd.DataFrame({0:{0:np.nan, 1:"2010-02-01", 2:"2010-02-01", 3:None, 4:"2012-02-01", 5:"2010-01-03"}})
COLUMNS_NANS = pd.DataFrame({0:{0:np.nan}})
COLUMNS_ABSTRACTS = pd.DataFrame({0:{0:"【課題】迅速にニューラルネットワークの最適パラメータを知ること。【解決手段】",
1:"A chemical sensing system is described. The chemical sensing system can."}})
COLUMNS_ABSTRACTS_NO_ENGLISH = pd.DataFrame({0:{0:"【課題】迅速にニューラルネットワークの最適パラメータを知ること。【解決手段】",
1:"본 발명에 따른 머신러닝을 이용한 양자 얽힘 변환 방법은, "}})

TEST_DF = pd.DataFrame({1:{"text_col":"string1;;string1","number_col":1.5, "date_col":"2010-01-01"}, 
                        2:{"text_col":"string2;;string3","number_col":1.5, "date_col":"2011-01-01"},
                        3:{"text_col":"string1;;string1","number_col":None, "date_col":"2010-02-01"},
                        4:{"text_col":"string3","number_col":2, "date_col":"2010-01-15"}}).transpose()
WEIGHTED_COLUMNS = pd.DataFrame({"value":{0:2, 1:3, 2:np.nan}, "weight":{0:0.5, 1:1, 2:1}})
DICT_DF = pd.DataFrame({0:{"Citations":1, "Jurisdiction":"NL"}, 
    1:{"Citations":3, "Jurisdiction":np.nan},
    2:{"Citations":2, "Jurisdiction":"EP"},
    3:{"Citations":1, "Jurisdiction":"CN"},
    4:{"Citations":2, "Jurisdiction":"CN"},
    5:{"Citations":np.nan, "Jurisdiction":"NL"}}).transpose()

# test individual join functions
def test_join():
    joined_columns = ut.join(pd.DataFrame(COLUMNS))
    assert joined_columns[0] == "string1;;string1;,;,string1;;string1;,;,string3;;string1;,;,1;,;,1;,;,2;,;,0"

def test_join_first():
    joined_columns = ut.join_first(pd.DataFrame(COLUMNS))
    assert joined_columns[0] == "string1;;string1"

def test_join_first_english():
    joined_columns = ut.join_first_english(COLUMNS_ABSTRACTS)
    assert joined_columns[0] == "A chemical sensing system is described. The chemical sensing system can."

def test_join_first_english_no_english():
    joined_columns = ut.join_first_english(COLUMNS_ABSTRACTS_NO_ENGLISH)
    assert np.isnan(joined_columns[0])

def test_join_set():
    joined_columns = ut.join_set(COLUMNS)
    assert set(joined_columns[0].split(";;")) == set("string1;;string3;;1;;2;;0".split(";;"))

def test_join_size():
    joined_columns = ut.join_size(COLUMNS)
    assert joined_columns[0] == 9

def test_join_most():
    joined_columns = ut.join_most(COLUMNS)
    assert joined_columns[0] == "string1"

def test_join_max():
    joined_columns = ut.join_max(COLUMNS_NUMBERS)
    assert joined_columns[0] == 3.5

def test_join_sum():
    joined_columns = ut.join_sum(COLUMNS_NUMBERS)
    assert round(joined_columns[0],2) == -992.17

def test_join_sum_weighted():
    joined_columns = ut.join_sum_weighted(WEIGHTED_COLUMNS)
    assert joined_columns[0] == 4

def test_join_mean():
    joined_columns = ut.join_mean(COLUMNS_NUMBERS)
    assert round(joined_columns[0],2) == -141.74

def test_join_mean_weighted():
    joined_columns = ut.join_mean_weighted(WEIGHTED_COLUMNS)
    assert round(joined_columns[0],2) == 2.67

def test_join_earliest():
    joined_columns = ut.join_earliest(COLUMNS_DATES)
    assert joined_columns[0] == "2010-01-03"

def test_join_size_not_nan():
    joined_columns = ut.join_size_not_nan(COLUMNS_NUMBERS)
    assert joined_columns[0] == 7

def test_join_size_not_nan_weighted():
    joined_columns = ut.join_size_not_nan_weighted(WEIGHTED_COLUMNS)
    print(joined_columns)
    assert joined_columns[0] == 1.5

def test_join_nans():
    joined_columns = ut.join(COLUMNS_NANS)
    assert joined_columns[0] == ""

def test_join_first_nans():
    joined_columns = ut.join_first(COLUMNS_NANS)
    assert np.isnan(joined_columns[0])

def test_join_first_english_nan():
    joined_columns = ut.join_first_english(COLUMNS_NANS)
    assert np.isnan(joined_columns[0])

def test_join_set_nans():
    joined_columns = ut.join_set(COLUMNS_NANS)
    assert joined_columns[0] == ""

def test_join_size_nans():
    joined_columns = ut.join_size(COLUMNS_NANS)
    assert joined_columns[0] == 1

def test_join_most_nans():
    joined_columns = ut.join_most(COLUMNS_NANS)
    assert np.isnan(joined_columns[0])

def test_join_max_nans():
    joined_columns = ut.join_max(COLUMNS_NANS)
    assert np.isnan(joined_columns[0])

def test_join_sum_nans():
    joined_columns = ut.join_sum(COLUMNS_NANS)
    assert joined_columns[0] == 0

def test_join_mean_nans():
    joined_columns = ut.join_mean(COLUMNS_NANS)
    assert np.isnan(joined_columns[0])

def test_join_earliest_nans():
    joined_columns = ut.join_earliest(COLUMNS_NANS)
    assert np.isnan(joined_columns[0])

def test_join_size_not_nan_nans():
    joined_columns = ut.join_size_not_nan(COLUMNS_NANS)
    assert joined_columns[0] == 0

def test_join_dict_sum():
    joined_columns = ut.join_dict_sum(DICT_DF[["Jurisdiction", "Citations"]])
    assert joined_columns[0] == 'CN:3;;EP:2;;NL:1'

# test join_columns and conversion functions
def test_join_columns():
    dataframe_compressor = ut.DataFrameCompressor([\
                    (["text_col"], ut.join_set, ["text_index"]),
                    (["number_col"], ut.join_max, ["number_index"])])
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
    column_out = lambda col: col[0]+" (fractionally counted)"
    compression_function = ut.CompressionFunction([column_in], ut.join_sum, [column_out])
    in_out_pairs = list(compression_function.get_in_out_pairs(df))
    assert in_out_pairs[0] == (['2010'], ['2010 (fractionally counted)'])
    assert in_out_pairs[1] == (['2011'], ['2011 (fractionally counted)'])

def test_compression_function_convert_one():
    df = pd.DataFrame({0:{"column in":1, "weight column":1}, 
                    1:{"column in":2, "weight column":2}}).transpose()
    compression_function = ut.CompressionFunction(["column in"], ut.join_sum, ["column out"])
    value = compression_function.convert_one(df, ["column in"])
    assert value[0] == 3

def test_compression_function_convert_one_weighted():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":0.5}}).transpose()
    compression_function = ut.CompressionFunction(["column in", "weight column"], ut.join_sum_weighted, ["column out"])
    value = compression_function.convert_one(df, ["column in", "weight column"])
    assert value[0] == 6

def test_compression_function_convert_one_weighted_mean():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":2}}).transpose()
    compression_function = ut.CompressionFunction(["column in", "weight column"], ut.join_mean_weighted, ["column out"])
    value = compression_function.convert_one(df, ["column in", "weight column"])
    assert value[0] == 3

def test_compression_function_convert_one_weighted_mean_nan():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":2},
                    3:{"column in":np.nan, "weight column":3}}).transpose()
    compression_function = ut.CompressionFunction(["column in", "weight column"], ut.join_mean_weighted, ["column out"])
    value = compression_function.convert_one(df, ["column in", "weight column"])
    assert value[0] == 3

def test_compression_function_convert_one_weighted_size():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":2},
                    2:{"column in":np.nan, "weight column":3}}).transpose()
    compression_function = ut.CompressionFunction(["column in", "weight column"], ut.join_size_not_nan_weighted, ["column out"])
    value = compression_function.convert_one(df, ["column in", "weight column"])
    assert value[0] == 3

def test_compression_function_convert_one_remove_duplicate_index_false():
    df = pd.DataFrame({0:{"column in":5, "weight column":1}, 
                    1:{"column in":2, "weight column":1}}).transpose()
    df = pd.concat([df, pd.DataFrame.from_records([{"column in":3, "weight column":0.5}])], axis=0)
    print(df)
    compression_function = ut.CompressionFunction(["column in"], ut.join_sum, ["column out"], remove_duplicate_index=False)
    value = compression_function.convert_one(df, ["column in"])
    assert value[0] == 10

def test_compression_function_convert_multiple():
    df = pd.DataFrame({0:{"2010":1, "2011":0, "weight column":1},
                    1:{"2010":0, "2011":1, "weight column":0.5},
                    2:{"2010":0, "2011":1, "weight column":1}}).transpose()
    column_in_pattern = re.compile("[0-9]{4}")
    column_out_function = lambda cols: cols[0]+" (fractionally counted)"
    compression_function = ut.CompressionFunction([column_in_pattern, "weight column"], ut.join_sum_weighted, [column_out_function])
    values = compression_function.convert(df)
    print(values)
    assert all(pd.Series(values) == pd.Series({"2010 (fractionally counted)":1, "2011 (fractionally counted)":1.5}))

def test_dataframe_compressor_convert_weighted():
    df = pd.DataFrame({0:{"column in":5, "column in2":3, "weight column":1}, 
                    1:{"column in":2, "column in2":4, "weight column":2}}).transpose()
    dataframe_compressor = ut.DataFrameCompressor(\
        [(["column in","weight column"], ut.join_sum_weighted, ["column out weighted"]),
        (["column in2"], ut.join_mean, ["column out2"]),
        (["column in"], ut.join_sum, ["column out"])])
    sr = dataframe_compressor.convert(df)
    assert all(sr == pd.Series({"column out weighted": 9, "column out2": 3.5, "column out":7}))

def test_dataframe_compressor_convert_re():
    dataframe_compressor = ut.DataFrameCompressor([
        ([re.compile("^[0-9]{4}"+" (extension)".replace("(", "\(").replace(")","\)")+"$")], 
        ut.join_sum, 
        [lambda cols: cols[0]])])
    
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
    print(new_df)
    assert new_df.loc[1].size == 6
    assert new_df.loc[1, "Weight per Applicant"].sum() == 1
    assert all(new_df.loc[2] == pd.Series({"Applicants":"IBM UK", "Weight per Applicant":1, "Applicant":"IBM UK"}))

def test_unfold_cell_overloaded_column_real_case():
    df = pd.read_excel(RESOURCES_FOLDER+"test-families.xlsx")
    new_df = ut.unfold_cell_overloaded_column(df, "Applicants", "Applicant")
    assert len(new_df) == 11
