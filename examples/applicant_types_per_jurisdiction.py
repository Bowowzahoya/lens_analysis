import os
import sys


package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                            '../src'))
if package_path not in sys.path:
    sys.path.insert(0, package_path)

RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/")
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),"out/")

import lens_analysis as la
import pandas as pd
from datetime import datetime

lens_export = pd.read_csv(RESOURCES_FOLDER+"invasive-species.csv", index_col=0)

print(f"{datetime.now().time()}: Merging to families.")
families = la.aggregate_to_family(lens_export)
print(f"{datetime.now().time()}: Adding extra family information.")
families = la.add_extra_family_information(families)
print(f"{datetime.now().time()}: Exporting families.")
families.to_excel(OUTPUT_FOLDER+"families.xlsx")

print(f"{datetime.now().time()}: Splitting per jurisdiction and exporting.")
chinese_jurisdiction_mask = families["Jurisdictions"].str.contains("CN")
families_in_china = families.loc[chinese_jurisdiction_mask]
families_in_china.to_excel(OUTPUT_FOLDER+"families_in_china.xlsx")

families_in_rest = families.loc[~chinese_jurisdiction_mask]
families_in_rest.to_excel(OUTPUT_FOLDER+"families_in_rest.xlsx")

print(f"{datetime.now().time()}: Merging to applicants China.")
applicants_in_china = la.aggregate_to_applicants(families_in_china)
print(f"{datetime.now().time()}: Labeling applicants China.")
applicants_in_china = la.add_labels(applicants_in_china)
applicants_in_china.to_excel(OUTPUT_FOLDER+"applicants_in_china.xlsx")


print(f"{datetime.now().time()}: Merging to applicants Rest of World.")
applicants_in_rest = la.aggregate_to_applicants(families_in_rest)
print(f"{datetime.now().time()}: Labeling applicants Rest of World.")
applicants_in_rest = la.add_labels(applicants_in_rest)
applicants_in_rest.to_excel(OUTPUT_FOLDER+"applicants_in_rest.xlsx")


print(f"{datetime.now().time()}: Merging to applicant types China.")
applicant_types_in_china = la.aggregate_to_applicant_types(applicants_in_china)
applicant_types_in_china.to_excel(OUTPUT_FOLDER+"applicant_types_in_china.xlsx")

print(f"{datetime.now().time()}: Merging to applicant types Rest of World.")
applicant_types_in_rest = la.aggregate_to_applicant_types(applicants_in_rest)
applicant_types_in_rest.to_excel(OUTPUT_FOLDER+"applicant_types_in_rest.xlsx")
