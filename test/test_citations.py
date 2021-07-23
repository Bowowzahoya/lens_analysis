# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:30:01 2021

@author: David
"""

import unittest
from context import lens_analysis
from lens_analysis import citations as ct
import pandas as pd

FOLD = "res/"


class TestFuncs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fam = pd.read_excel(FOLD+"fam.xlsx")

    def testCalcMncs(self):
        fam = ct.calc_mncs(self.fam)

        assert fam.iloc[0]["Mean Normalized Citation Score"] > 0.202 and fam.iloc[0]["Mean Normalized Citation Score"] < 0.203
        assert str(fam.iloc[-1]["Mean Normalized Citation Score"]) == "nan"
    
    
if __name__ == '__main__':
    unittest.main()