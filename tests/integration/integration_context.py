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

def dataframes_equal(df1, df2):
    if len(df1) != len(df2): 
        print("Lengths not equal")
        return False
    if len(df1.columns) != len(df2.columns):
        print("Columns not equal length")
        return False
    if not all(df1.columns == df2.columns):
        print("Columns not equal")
        return False

    for column_name in df1.columns:
        print(f"Asserting column {column_name}")
        column = df1[column_name]
        column2 = df2[column_name]
        if column.dtype == "object" and column2.dtype == "object":
            print("Testing objects")
            lengths = column.fillna("").str.len()
            lengths[lengths > 32767] = 32767 # maximum string length for pd.read_excel
            test_lengths = df2[column_name].fillna("").str.len()

            if not (lengths == test_lengths).all(): 
                print("Not equal")
                return False
        elif column.dtype == "bool":
            print("Testing Booleans")
            if not all(column == df2[column_name]): 
                print("Not equal")
                return False
        elif column.dtype == "object" and column2.dtype == "float64":
            print("Object types unequal")
            try:
                print("Trying testing float")
                if not (abs(column.fillna(0) - df2[column_name].fillna(0)) < 0.001).all(): 
                    print("Not equal")
                    return False
            except TypeError:
                print("Exception testing objects")
                lengths = column.fillna("").str.len()
                lengths[lengths > 32767] = 32767 # maximum string length for pd.read_excel
                test_lengths = df2[column_name].fillna("").str.len()

                if not (lengths == test_lengths).all(): 
                    print("Not equal")
                    return False
        else:
            print("Testing integers / floats")
            if not (abs(column.fillna(0) - df2[column_name].fillna(0)) < 0.001).all(): 
                print("Not equal")
                return False
    return True