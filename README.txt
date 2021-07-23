Module for doing analytics on downloaded Lens exports

-----------------------
-----------------------
BACKGROUND:
Lens offers some analytics and statistics on the website, but sometimes too limited for advanced analyses
For example, only the top 100 applicants are listed, most information is on publication level, not on family level, it is not possible to add different version of the same applicant together, and there are no citation scores or market coverage scores.

This module provides some of these basic metrics for analysis on applicant level. 
On top of above functionality, it also adds some functionality for recognizing Dutch and/or Chinese applicants.
Module can potentially be expanded to include other countries.

-----------------------
-----------------------
USAGE:
- family_dataframe = merge_to_family(export_dataframe) # merges a Lens export dataframe with index Lens ID to a family dataframe with index Priority Number

- family_dataframe["Standardized Applicant Name"] = alias_apps(family_dataframe, aliases) # add new column to merge different names of the same applicant

- family_dataframe = calc_mncs(family_dataframe) # calculate mean normalized citation score and add as new column

- family_dataframe = calc_mark_cov(family_dataframe) # calculate market coverage and add as new column

- applicant_dataframe = merge_to_applicant(family_dataframe) # merges to an applicant dataframe


- is_cn() and is_nl() can be used on a family_dataframe row to identify Chinese/Dutch applicants.

family_dataframe["Country"] = alias_apps(family_dataframe, alias_fs=[is_cn, is_nl], add_or=False) 
# row entry will be None if not Dutch or Chinese

def guess_nationality(sr):
    if sr.count("NL") > 0.7*len(sr):
        return "Dutch"
    elif sr.count("CN") > 0.7*len(sr):
        return "Chinese"
    else:
        return "Neither Chinese nor Dutch"

func_d_custom = {"Country":("Country", guess_nationality)}
applicant_dataframe = merge_to_applicant(family_dataframe, func_d_custom=func_d_custom)
# this will get you to an applicant dataframe where applicants are classified as Dutch 
# if at least 70% of families are guessed as having a Dutch applicant