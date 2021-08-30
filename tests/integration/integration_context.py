# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:30:43 2020

@author: david
"""

import os
import sys
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                            '../../src'))
if package_path not in sys.path:
    sys.path.insert(0, package_path)
print(package_path)

import lens_analysis

RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/")
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"out/")

def are_dataframes_equal(df1, df2):
    assert all(df1.columns == df2.columns)

    assert len(df1) == len(df2)

    for column_name in df1.columns:
        print(f"Testing column {column_name}")
        column = df1[column_name]
        if column.dtype == "object":
            lengths = column.fillna("").str.len()
            lengths[lengths > 32767] = 32767 # maximum string length for pd.read_excel
            test_lengths = df2[column_name].fillna("").str.len()

            assert (lengths == test_lengths).all()
        elif column.dtype == "bool":
            assert all(column == df2[column_name])
        else:
            assert (abs(column.fillna(0) - df2[column_name].fillna(0)) < 0.001).all()