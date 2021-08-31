Module for doing analytics on downloaded Lens exports

-----------------------
-----------------------
BACKGROUND:
Lens offers some analytics and statistics on the website, but sometimes too limited for advanced analyses
For example, only the top 100 applicants are listed, most information is on publication level, not on family level, it is not possible to add different version of the same applicant together, and there are no citation scores or market coverage scores.

This module provides some of these basic metrics for analysis on applicant level. 
On top of above functionality, it also adds some functionality for grouping applicants together per type
e.g. Chinese companies, Chinese academia, American companies, EU-27 companies, etc.

-----------------------
-----------------------
USAGE
Normal usage would be to first aggregate an export to patent families,
then aggregate to applicants (possibly with aliases for applicants that exist under different names/spelling)
then possibly aggregate even further to count patents for particular types,
e.g. Chinese companies, Chinese universities, American companies, etc.

USAGE BY FUNCTION:
- aggregate_to_family()
Will group patent families together from a lens export (in pandas DataFrame format)

import pandas as pd
lens_export = pd.read_csv("lens-export.csv", index_col=0)
families = aggregate_to_family(lens_export)

-------------------------------
- add_extra_family_information()
Will add extra columns with additional family information (such as citation scores, market coverage, etc.)

families = add_extra_family_information(families)

-------------------------------
- aggregate_to_applicants()
Will group patent applicants together from a patent families DataFrame
Can possibly include aliases for different version of the same applicant (e.g. IBM UK, IBM CO LTD, 国际商机公司, etc.)
You need to first use add_extra_family_information() on the families DataFrame to also get citation information in the
resultant applicant DataFrame.

aliases = pd.read_excel("aliases.xlsx", index_col=0, squeeze=True)
applicants = aggregate_to_applicants(families, aliases=aliases)

-------------------------------
- guess_aliases()
Will guess aliases for a number of applicants, based on joint patents, and shortened versions of the applicant name
Please note that inventors that appear in tandem with the applicant will also appear in this list
As well as any collaboration partners with whom joint patents have been filed.
You have to get rid of these yourself.

# to guess aliases for top 20 applicants
aliases = guess_aliases(applicants, applicants.index[0:20])
aliases.to_excel("guessed_aliases.xlsx")

-------------------------------
- add_labels()
Will classify patent applicants and give them a label according to applicant type (e.g. Chinese company, American academia).
Classification is based on a list of known applicants; keywords to indicate university, company; company types per country; applicant in inventor list (indicates individual); main priority jurisdiction.

applicants = add_labels(applicants)

-------------------------------
- aggregate_to_applicant_types()
Will group patent applicants together from a patent applicants DataFrame
patent applicants DataFrame will need to have labels added first using the function add_labels()

applicant_types = aggregate_to_applicant_types(applicants)
