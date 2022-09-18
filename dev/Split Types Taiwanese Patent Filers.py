# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:38:19 2022

@author: David

This script the splitting that led to the Taiwan labeler.
The data is based on EPO-API downloaded data listed as [TW] based on address.

pinyin_tools from github.com/bowowzahoya
"""



import pandas as pd
import pinyin_tools as pt

RES_FOLDER = "res/"
OUT_FOLDER = "out/"
THRESHOLD = 2

applicants = pd.read_excel(RES_FOLDER+"Largest_Taiwanese_Patent_Filers_EPO_API_2010-2022.xlsx", index_col=0, squeeze=True)

applicants = applicants[applicants >= THRESHOLD]

# clean up formatting with extra linebreaks
for app in applicants.index:
    if app[-1:] == "\n":
        amount = applicants[app]
        applicants = applicants.drop(app)
        shortened_app = app[:-1]
        if shortened_app in applicants.index:
            applicants[shortened_app] += amount
        else:
            applicants[shortened_app] = amount
            

# Non [TW] applicants (in this dataset because on same patent as [TW] applicant)
non_tw_applicants = applicants[applicants.index.str[-4:] != "[TW]"]

foreign_applicants = non_tw_applicants[non_tw_applicants.index.str[-1] == "]"]
print(foreign_applicants)
foreign_applicants.to_excel(OUT_FOLDER+"foreign_applicants.xlsx")

# No country listed as [] applicants (in this dataset because on same patent as [TW] applicant)
unknown_applicants = non_tw_applicants[non_tw_applicants.index.str[-1] != "]"]
print(unknown_applicants)
unknown_applicants.to_excel(OUT_FOLDER+"unknown_applicants.xlsx")

tw_applicants = applicants[applicants.index.str[-4:] == "[TW]"]
tw_applicants.index = tw_applicants.index.str[:-5]

# The following could also be Chinese inventors 
pinyin_name_applicants = tw_applicants[tw_applicants.index.str.replace("-"," ").str.lower().map(pt.is_name)]
print(pinyin_name_applicants)
pinyin_name_applicants.to_excel(OUT_FOLDER+"pinyin_name_applicants.xlsx")

# the following are at least not pinyin
non_pinyin_applicants = tw_applicants[tw_applicants.index.difference(pinyin_name_applicants.index)]
print(non_pinyin_applicants)
non_pinyin_applicants.to_excel(OUT_FOLDER+"non_pinyin_applicants.xlsx")

# more likely to be organizations or person?
likely_organizations = pd.Series()
likely_individual = pd.Series()

ORG_MARKERS = ["INST", "CO", "LTD", "UNIV", "CORP", "INC", "CORPORATION"]
for app in non_pinyin_applicants.index:
    if any([marker in app for marker in ORG_MARKERS]):
        likely_organizations[app] = non_pinyin_applicants[app]
    elif app.count(" ") == 2 and all([len(syl) <= 6 for syl in app.split(" ")]):
        likely_individual[app] = non_pinyin_applicants[app]
    elif app.count(" ") == 1 and (len(app.split(" ")[0]) <= 6 and len(app.split(" ")[1]) <= 12):
        likely_individual[app] = non_pinyin_applicants[app]
    else:
        likely_organizations[app] = non_pinyin_applicants[app]

likely_individual = likely_individual.sort_values(ascending=False)
likely_individual.to_excel(OUT_FOLDER+"likely_individual.xlsx")
likely_organizations = likely_organizations.sort_values(ascending=False)
likely_organizations.to_excel(OUT_FOLDER+"likely_organizations.xlsx")



