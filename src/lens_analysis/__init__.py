# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:17:35 2021

@author: David
"""

from .applicants import aggregate_to_applicants
from .families import aggregate_to_family, add_extra_family_information
from .applicant_labeler import aggregate_to_applicant_types, add_labels, NL_LABELER, TW_LABELER, EU_US_CHINA_LABELER
from .applicant_disambiguation import guess_aliases
from .constants import CN_JURISDICTION, US_JURISDICTION, EU_JURISDICTIONS, REST_OF_WORLD_JURISDICTIONS