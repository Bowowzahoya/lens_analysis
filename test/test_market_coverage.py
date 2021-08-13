import pandas as pd
import numpy as np
import os

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import market_coverage as mc

TEST_FAMILIES = pd.read_excel(RESOURCES_FOLDER+"ai-and-nanotech-families.xlsx", index_col=0)

def test_get_market_coverage():
    market_coverage = mc.get_market_coverage(TEST_FAMILIES)
    assert market_coverage["US 201962908841 P;;US 202017036428 A"] == 0.7
    assert market_coverage["US 201962907142 P;;US 201962911673 P;;US 202062983022 P"] == 0.973
