# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:24:43 2021

This module provides functionality for finding the biggest applicant
from patent family data

Main functions:
    - merge_to_applicants(), takes a patent family DataFrame and
    groups them into families per applicant, also distilling other
    information like covered jurisdiction, market coverage, citation scores
    
    The function makes use of dictionary 
    FUNC_D that maps certain columns from the family DataFrame (key)
    to new columns (value1) in the applicant DataFrame 
    through a function (value2)
    
    You can add or change these mappings by providing a custom_func_d
    
    - alias_apps(), maps applicant names in a family DataFrame to
    other names. Can be used to add different variants of a name together.
    For example IBM Licensing, IBM China and I.B.M. all map to IBM.
    This can be done using either a dict or a function.
    After this, merge_to_applicants() can be used on the new applicant column
    to get a fairer picture.

@author: David
"""
import pandas as pd
from itertools import chain
from collections import defaultdict
from .constants import *
from .utilities import join, join_set, join_max, join_sum, join_earliest 
from .utilities import join_size, join_cols, join_mean, join_most

FUNC_D = {MNCS_COL:(MNCS_COL, join_mean),
          APP_COL:(CO_APP_COL, join_set),
          NPL_COL:(AM_COL, join_size),
          JURS_COL:(TOP_JUR_COL, join_most),
          MCOV_COL:(MCOV_COL, join_mean)}

def _get_all_apps(col):
    """ 
    Takes the column of applicants (multiple ; separated per entry)
    and expands them into a dict of priority numbers/indexes per applicant
    """
    apps = [[(app, ix) for app in str(col[ix]).split(SEP)] for ix in col.index]
    apps_d = defaultdict(list)
    for app, ix in chain(*apps):
        apps_d[app].append(ix)
    return apps_d


def _alias_apps_d(row, alias_d={}, app_col=APP_COL):
    """ 
    Retrieves an alias for an applicant based on a dict
    """
    apps = row.loc[app_col]
    return SEP.join(set([alias_d.get(app, app) for app in apps.split(SEP)]))

def _alias_apps_f(row, alias_fs=[], add_or=True, app_col=APP_COL, **kwargs):
    """
    Retrieves an alias for an applicant based on a list of functions
    
    Each function should accept a series and
    return a string value (assign that value)

    if None or False, will not add
    
    If add_or will add original when not found
    
    As soon as an assignment, will not use next function
    """
    apps = row.loc[app_col]
    
    aliases = set()
    if not isinstance(apps, str):
        apps = ""
    for app in apps.split(SEP):
        found = False
        for alias_f in alias_fs:
            row_single = row.copy() # make a row with a single applicant
            row_single[app_col] = app
            alias = alias_f(row_single)

            if isinstance(alias, str):
                aliases.add(alias)
                found = True
                break
            elif isinstance(alias, type(None)) or alias == False:
                # function returned nothing, trying next function
                continue
            else:
                raise Exception(f"Invalid format of {alias}")
        if add_or and not found:
            aliases.add(app)
    return SEP.join(aliases)
    
    
    
def alias_apps(fam, alias_d={}, alias_fs=[], **kwargs):
    """
    Maps patent applicant names to other names

    This function is necessary as there can be more applicants 
    per patent family, which makes using a direct mapping harder.
    
    It can be used to get rid of different name variants of applicants
    in the family DataFrame, after which merge_to_applicants can be used
    to count number of patents, etc.
    
    Parameters
    ----------
    fam : DataFrame
        Patent family data, with index priority numbers
    alias_d : dict-like, optional (one of two)
        Direct mapping of applicants to other names. The default is {}.
    alias_fs : list of string, optional (one of two)
        List of functions to use for mapping. The default is [].
    **kwargs : dict
        Arguments for the alias functions (see above)

    Returns
    -------
    aliases
        Series of new names for applicants

    """
    if len(alias_fs) > 1 and len(alias_d) > 1:
        raise Exception("Please use either an alias dict or alias functions")
    elif len(alias_d) > 1:
        return fam.apply(_alias_apps_d, axis=1, alias_d=alias_d, **kwargs)
    elif len(alias_fs) > 1:
        return fam.apply(_alias_apps_f, axis=1, alias_fs=alias_fs, **kwargs)
    else:
        raise Exception("Please use either an alias dict or alias functions")

def merge_to_applicants(fam, func_d_custom={}, app_col=APP_COL):   
    """
    Merges patent family data to patent applicant data

    Parameters
    ----------
    fam : DataFrame
        Patent family data, with index priority numbers
        and columns at least those that are included 
        in FUNC_D and func_d_custom
    func_d_custom : dict, with tuples of length 2 as values, optional
        A dictionary of which columns to map to which columns
        using which function. Uses same structure as FUNC_D
        and will override if there is overlap. The default is {}.
    app_col : str, optional
        The name of the applicant column in the fam DataFrame.
        The default is APP_COL.

    Returns
    -------
    apps : DataFrame
        Patent applicant data, with index applicant names

    """
    # update function dictionary
    func_d = FUNC_D.copy()
    for key in func_d_custom:
        func_d[key] = func_d_custom[key]
        
    apps = pd.DataFrame(columns=[func_d[key][0] for key in func_d])
        
    apps_d = _get_all_apps(fam[app_col])
    for app in apps_d:
        ixs = apps_d[app]
        sub_fam = fam.loc[ixs]
        apps.loc[app] = join_cols(sub_fam, func_d)
        
    apps = apps.sort_values(AM_COL, ascending=False)
    return apps

    
    
    
    