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

# First get patent families from Lens Export
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

eu_jurisdiction_mask = families["Jurisdictions"].apply(lambda jurs: any([jur in jurs for jur in la.EU_JURISDICTIONS]))
families_in_eu = families.loc[eu_jurisdiction_mask]
families_in_eu.to_excel(OUTPUT_FOLDER+"families_in_eu.xlsx")

families_out_china = families.loc[~chinese_jurisdiction_mask]
families_out_china.to_excel(OUTPUT_FOLDER+"families_out_china.xlsx")

# Merge families to applicants
print(f"{datetime.now().time()}: Merging to applicants.")
applicants = la.aggregate_to_applicants(families)
applicants.to_excel(OUTPUT_FOLDER+"applicants.xlsx")

print(f"{datetime.now().time()}: Guessing aliases of top 20.")
aliases = la.guess_aliases(applicants, applicants.index[0:20])
aliases.to_excel(OUTPUT_FOLDER+"aliases.xlsx")
input("Adapt the aliases file, save as 'aliases_adapted.xlsx' and press enter to continue...")

print(f"{datetime.now().time()}: Remerging applicants with aliases included.")
aliases_adapted = pd.read_excel(OUTPUT_FOLDER+"aliases_adapted.xlsx", index_col=0, squeeze=True)
applicants_aliased = la.aggregate_to_applicants(families, aliases=aliases_adapted)
applicants_aliased.to_excel(OUTPUT_FOLDER+"applicants_aliased.xlsx")

print(f"{datetime.now().time()}: Merging to applicants China.")
applicants_in_china = la.aggregate_to_applicants(families_in_china)
print(f"{datetime.now().time()}: Labeling applicants China.")
applicants_in_china = la.add_labels(applicants_in_china)
applicants_in_china.to_excel(OUTPUT_FOLDER+"applicants_in_china.xlsx")

print(f"{datetime.now().time()}: Merging to applicants EU.")
applicants_in_eu = la.aggregate_to_applicants(families_in_eu)
print(f"{datetime.now().time()}: Labeling applicants EU.")
applicants_in_eu = la.add_labels(applicants_in_eu)
applicants_in_eu.to_excel(OUTPUT_FOLDER+"applicants_in_eu.xlsx")

print(f"{datetime.now().time()}: Merging to applicants Outside China.")
applicants_out_china = la.aggregate_to_applicants(families_out_china)
print(f"{datetime.now().time()}: Labeling applicants Outside China.")
applicants_out_china = la.add_labels(applicants_out_china)
applicants_out_china.to_excel(OUTPUT_FOLDER+"applicants_out_china.xlsx")

# Merge applicants to applicant types
print(f"{datetime.now().time()}: Merging to applicant types China.")
applicant_types_in_china = la.aggregate_to_applicant_types(applicants_in_china)
applicant_types_in_china.to_excel(OUTPUT_FOLDER+"applicant_types_in_china.xlsx")

print(f"{datetime.now().time()}: Merging to applicant types EU.")
applicant_types_in_eu = la.aggregate_to_applicant_types(applicants_in_eu)
applicant_types_in_eu.to_excel(OUTPUT_FOLDER+"applicant_types_in_eu.xlsx")

print(f"{datetime.now().time()}: Merging to applicant types Outside China.")
applicant_types_out_china = la.aggregate_to_applicant_types(applicants_out_china)
applicant_types_out_china.to_excel(OUTPUT_FOLDER+"applicant_types_out_china.xlsx")
