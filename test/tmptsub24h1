# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:30:01 2021

@author: David
"""

import unittest
from context import lens_analysis
from lens_analysis import applicants as ap
from lens_analysis import countries as ct
from collections import defaultdict
import pandas as pd

FOLD = "res/"

class TestMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fam = pd.read_excel(FOLD+"fam_mcov.xlsx")

    def testMergeToApplicants(self):
        apps = ap.merge_to_applicants(self.fam)        
        #apps.to_excel("apps.xlsx")
        assert apps.loc["ITERIS INC", "Amount of Patents"] == 17
        
    def testGetAllApps(self):
        apps = ap._get_all_apps(self.fam[ap.APP_COL])
        assert apps['WINDWISDEM CORP'] == [995]
        

class TestAlias(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fam = pd.read_excel(FOLD+"fam_mcov.xlsx", index_col=0)
        cls.alias_d = {"SZ DJI TECHNOLOGY CO LTD":"DJI",
                       "エスゼット ディージェイアイ テクノロジー カンパニー リミテッドＳＺ ＤＪＩ ＴＥＣＨＮＯＬＯＧＹ ＣＯ．，ＬＴＤ":"DJI",
                       "DJI-INNOVATIONS":"DJI"}

    def testAliasAppsD(self):
        apps_s = "SZ DJI TECHNOLOGY CO LTD;;エスゼット ディージェイアイ テクノロジー カンパニー リミテッドＳＺ ＤＪＩ ＴＥＣＨＮＯＬＯＧＹ ＣＯ．，ＬＴＤ"
        apps = pd.Series({"Applicants":apps_s}, name="NL84110000")
        apps = ap._alias_apps_d(apps, alias_d=self.alias_d)
        assert apps == "DJI"
        
    def testAliasAppsF(self):
        apps_s = "DJI OK;;SZ DJI TECHNOLOGY CO LTD;;エスゼット ディージェイアイ テクノロジー カンパニー リミテッドＳＺ ＤＪＩ ＴＥＣＨＮＯＬＯＧＹ ＣＯ．，ＬＴＤ"
        apps = pd.Series({"Applicants":apps_s}, name="NL84110000")
        def func_1(row):
            app = row["Applicants"]
            if "TECHNOLOGY" in app:
                return "Func1"
            
        def func_2(row):
            app = row["Applicants"]
            if "DJI" in app:
                return "Func2"
        
        apps = ap._alias_apps_f(apps, alias_fs=[func_1, func_2])
        assert "Func1" in apps
        assert "Func2" in apps
        assert "エスゼット ディージェイアイ テクノロジー カンパニー リミテッドＳＺ ＤＪＩ ＴＥＣＨＮＯＬＯＧＹ ＣＯ．，ＬＴＤ" in apps
        
    def testAliasApps(self):
        aliases = ap.alias_apps(self.fam, alias_d=self.alias_d)
        self.fam["Aliases"] = aliases
        self.fam.to_excel("fam_aliases.xlsx")

    def testAliasAppsCountries(self):
        funcs = [ct.is_nl, ct.is_cn]
        aliases = ap.alias_apps(self.fam, alias_fs=funcs, add_or=False)
        self.fam["Aliases"] = aliases
        self.fam.to_excel("fam_aliases.xlsx")
        
        
        
    
    
if __name__ == '__main__':
    unittest.main()