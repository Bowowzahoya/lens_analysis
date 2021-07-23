# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:30:01 2021

@author: David
"""

import unittest
from context import lens_analysis
from lens_analysis import applicants as ap
from lens_analysis import countries as ct
import pandas as pd

FOLD = "res/"   

class TestIsCn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fam = pd.read_excel(FOLD+"fam_mcov.xlsx", index_col=0)
        
    def testIsCn(self):
        app = "SZ DJI TECHNOLOGY CO LTD"
        row = pd.Series({"Applicants":app}, name="NL840000")
        ctry = ct.is_cn(row)
        assert ctry == "CN"
        
    def testIsCnNot(self):
        app = "JUST SOME COMPANY CO LTD"
        row = pd.Series({"Applicants":app}, name="NL840000")
        ctry = ct.is_cn(row)
        assert ctry != "CN"
        
    def testIsCnCity(self):
        app = "ANHUI OTHER COMPANY CO LTD YO"
        row = pd.Series({"Applicants":app}, name="NL840000")
        ctry = ct.is_cn(row)
        assert ctry == "CN"

    
if __name__ == '__main__':
    unittest.main()