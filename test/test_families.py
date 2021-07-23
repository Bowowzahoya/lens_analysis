# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:30:01 2021

@author: David
"""

import unittest
from context import lens_analysis
from lens_analysis import families as fm
import pandas as pd

FOLD = "res/"

@unittest.skip
class TestMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(FOLD+"cp-ag-auton.csv")
        print(cls.df)

    def testMergeToFamily(self):
        fam = fm.merge_to_family(self.df)
        print(fam)
        
        fam.to_excel("fam.xlsx")
    
class TestMergeFuncs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        df = pd.read_csv(FOLD+"cp-ag-auton.csv")
        prio = "CN 2015089689 W 20150916"
        cls.sub_df = df[df["Priority Numbers"] == prio]  
    
    def testJoinSet(self):
        val = fm.join_set(self.sub_df["IPCR Classifications"])
        assert val == "G01S19/41;;G01S5/00;;F41G9/00;;G01S19/51;;G01S19/45;;G01S19/48;;G01S19/23;;G01S19/52;;G01S19/43"
    
    def testJoinMax(self):
        val = fm.join_max(self.sub_df["Simple Family Size"])
        assert val == 7
      
    def testJoinSum(self):
        val = fm.join_sum(self.sub_df["Cited by Patent Count"])
        assert val == 12
        
    def testJoinEarliest(self):
        val = fm.join_earliest(self.sub_df["Publication Date"])
        assert val == "2017-03-23"
        
    def testJoinSize(self):
        val = fm.join_size(self.sub_df["#"])
        assert val == 7
        
    def testJoinMost(self):
        val = fm.join_most(self.sub_df["Jurisdiction"])
        assert val == "EP;;JP"
        
        
        
    
    
if __name__ == '__main__':
    unittest.main()