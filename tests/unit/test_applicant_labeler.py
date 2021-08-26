import pandas as pd
import numpy as np

from context import lens_analysis, RESOURCES_FOLDER, OUTPUT_FOLDER
from lens_analysis import applicant_labeler as al
from lens_analysis.constants import CHINESE_ACADEMIA_FILENAME, CHINESE_COMPANIES_FILENAME

TEST_APPLICANTS = pd.read_excel(RESOURCES_FOLDER+"ai-nanotech_applicants.xlsx", index_col=0)
APPLICANT_ROW1 = TEST_APPLICANTS.iloc[0]
APPLICANT_ROW2 = TEST_APPLICANTS.iloc[1]
APPLICANT_ROW35 = TEST_APPLICANTS.iloc[34] # first Chinese applicant

def test_applicant_identifier_type_no_filename():
    identification_functions = [al.main_priority_jurisdiction_equals]
    reference_data = ["US"]
    applicant_identifier = al.ApplicantTypeIdentifier(identification_functions, reference_data,
        args_are_filenames=False)

    is_identified = applicant_identifier.identify(APPLICANT_ROW1)
    assert is_identified

    identification_functions = [al.main_priority_jurisdiction_equals]
    reference_data = ["CN"]
    applicant_identifier = al.ApplicantTypeIdentifier(identification_functions, reference_data,
        args_are_filenames=False)

    is_identified = applicant_identifier.identify(APPLICANT_ROW1)
    assert not is_identified

def test_applicant_identifier_type_filename():
    identification_functions = [al.applicant_has_string]
    reference_data = [RESOURCES_FOLDER+"test_reference_data.xlsx"]
    applicant_identifier = al.ApplicantTypeIdentifier(identification_functions, reference_data,
        args_are_filenames=True)

    is_identified = applicant_identifier.identify(APPLICANT_ROW1)
    assert is_identified

    is_identified = applicant_identifier.identify(APPLICANT_ROW2)
    assert not is_identified

def test_applicant_identifier_type_no_value():
    identification_functions = [al.applicant_is_inventor]
    applicant_identifier = al.ApplicantTypeIdentifier(identification_functions,
        args_are_filenames=False)

    is_identified = applicant_identifier.identify(APPLICANT_ROW1)
    assert is_identified


def test_applicant_labeler():
    applicant_identifier1 = al.ApplicantTypeIdentifier([al.applicant_is_inventor])
    applicant_identifier2 = al.ApplicantTypeIdentifier([al.applicant_has_string], [CHINESE_ACADEMIA_FILENAME], 
        args_are_filenames=True)
    identifier_label_list = [
        (applicant_identifier1, ("Unknown", "Inventor")),
        (applicant_identifier2, ("Chinese", "Academia"))]

    applicant_labeler = al.ApplicantTypeLabeler(identifier_label_list)
    label_pair = applicant_labeler.label(APPLICANT_ROW1)
    assert all(label_pair == pd.Series(("Unknown","Inventor")))

    label_pair = applicant_labeler.label(APPLICANT_ROW35)
    assert all(label_pair == pd.Series(("Chinese","Academia")))


