# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021
Functionality for grouping families from Lens .csv exports
Using merge_to_family() to create a dataframe of families with 
all covered jurisdictions, earliest publication data, 
all applicant names, etc.

The function makes use of dictionary 
FUNC_D that maps certain columns from the family DataFrame (key)
to new columns (value1) in the applicant DataFrame 
through a function (value2)
    
You can add or change these mappings by providing a custom_func_d

@author: David
"""
import pandas as pd
from .constants import *
from .utilities import join, join_set, join_max, join_sum, join_earliest 
from .utilities import join_size, join_cols, join_most

FUNC_D = {IPCR_COL:(IPCR_COL, join_set),
          FAM_SZ_COL:(SET_FAM_SZ_COL,join_max),
          CIT_COL:(TOT_CIT_COL, join_sum),
          JUR_COL:(JURS_COL, join_set),
          KIND_COL:(KINDS_COL, join_set),
          PDAT_COL:(ERL_PDAT_COL, join_earliest),
          PY_COL:(ERL_PY_COL, join_earliest),
          APP_NUM_COL:(APP_NUMS_COL, join_set),
          APP_COL:(APP_COL, join_set),
          INV_COL:(INV_COL, join_set),
          OWN_COL:(OWN_COL, join_set),
          TYP_COL:(TYPS_COL, join_set),
          REF_COL:(TOT_REF_COL, join_sum),
          EXT_FAM_SZ_COL:(SET_EXT_FAM_SZ_COL, join_max),
          NPL_COL:(NPL_COL,  join_sum),
          NPL_RES_COL :(NPL_RES_COL , join_sum),
          IX_COL:(RES_FAM_SZ_COL, join_size),
          PNUM_COL:(PNUMS_COL, join_set),
          LID_COL:(LIDS_COL, join_set),
          ANUM_COL:(ANUM_COL, join_set),
          ADAT_COL:(ERL_ADAT_COL, join_earliest),
          TIT_COL:(TIT_COL, join_set)}


def _sort_prios(prio):
    # Needed because otherwise simple families might be
    # missed (NL00918;NL988 should be same family as NL988;NL00918)
    return SEP.join(sorted(prio.split(SEP)))

def merge_to_family(df, func_d_custom={}):
    """
    Merges patent publications into families.
    
    Parameters:
        df: DataFrame with publication per row (index Lens index)
        This is directly the .csv export from Lens
        Has columns at least those that are included 
        in FUNC_D and func_d_custom
        
        func_d_custom: dict, with tuples of length 2 as values, optional
        A dictionary of which columns to map to which columns
        using which function. Uses same structure as FUNC_D
        and will override if there is overlap. The default is {}.
    
    Returns:
        fam: DataFrame of patent families with index sorted priority number
    """
    df[SRT_PRIO_COL] = df[PRIO_COL].apply(_sort_prios)
    
    groupby = df.groupby(SRT_PRIO_COL)
    
    # update function dictionary
    func_d = FUNC_D.copy()
    for key in func_d_custom:
        func_d[key] = func_d_custom[key]
    
    fam = groupby.apply(join_cols, func_d)
    return fam
    