# lens_analysis
A module for doing analytics on downloaded Lens patent exports

## Background
Lens offers some analytics and statistics on the website, but sometimes too limited for advanced analyses. For example, only the top 100 applicants are listed, most information is on publication level, and not on family level. This module makes it possible to count patents fractionally per applicant, and aggregate analytics such as citation scores or market coverages to the applicant or applicant type level. It is also possible to add different name versions of the same applicant together, using the 'alias' functionality.

This module provides some of these basic metrics for analysis on applicant level. On top of above functionality, it also adds some functionality for grouping applicants together per type
e.g. Chinese companies, Chinese academia, American companies, EU-27 companies, et cetera. The applicant types are now according to two axes: EU-27, Chinese, American, Rest of World on one axis, and Company, Academia, Individual, Other or Unknown on the other axis. It is possible to create you own grouping based on a collection of "dataframe compressors".

## Usage
Normal usage would be to first aggregate an export to patent families, then aggregate to applicants (possibly with aliases for applicants that exist under different names/spelling), then possibly aggregate even further to count patents for particular applicant types.

### aggregate_to_family()
Will group patent families together from a lens export (in pandas DataFrame format).
```
import pandas as pd
lens_export = pd.read_csv("lens-export.csv", index_col=0)
families = aggregate_to_family(lens_export)
```

Note that these are a plain version of simple patent families in the sense of patent documents that strictly share the same priority numbers. This is slightly different from the DOCDB definition, which will allow for continuations or divisions of patents to be included in the family, even though they have only some of the priorities. For the DOCDB definition, see: https://www.epo.org/searching-for-patents/helpful-resources/first-time-here/patent-families/docdb.html#:~:text=A%20simple%20patent%20family%20is,have%20exactly%20the%20same%20priorities.

### add_extra_family_information()
Will add extra columns with additional family information (such as citation scores, market coverage, etc.)

```
families = add_extra_family_information(families)
```
### aggregate_to_applicants()
Will group patent applicants together from a patent families DataFrame to an alias. Can be used to rename different version of the same applicant to a single applicant (e.g. IBM UK, IBM CO LTD, 国际商机公司, et cetera are all IBM). 

```
aliases = pd.read_excel("aliases.xlsx", index_col=0, squeeze=True)
applicants = aggregate_to_applicants(families, aliases=aliases)
```

Note that you need to first use add_extra_family_information() on the families DataFrame to also get citation information in the resultant applicant DataFrame. Aliases needs to be a pandas Series with index applicant name and values alias.

### guess_aliases()
Will guess aliases for a number of applicants, based on joint patents, and shortened versions of the applicant name.

Please note that inventors that appear in tandem with the applicant will also appear in this list, as well as any collaboration partners with whom joint patents have been filed. You have to get rid of these yourself.

```
# to guess aliases for top 20 applicants
aliases = guess_aliases(applicants, applicants.index[0:20])
aliases.to_excel("guessed_aliases.xlsx")
```
### add_labels()
Will classify patent applicants and give them a label according to applicant type.

Classification is based on a list of known applicants; keywords to indicate university, company; company types per country; applicant in inventor list (indicates individual); main priority jurisdiction.

```
from lens_analysis import EU_US_CHINA_LABELER
applicants = add_labels(applicants, labeler=EU_US_CHINA_LABELER)
```

Other labelers that are available are TW_LABELER (for Taiwanese applicants), NL_LABELER (for Dutch applicants).

### aggregate_to_applicant_types()
Will group patent applicants together from a patent applicants DataFrame. The patent applicants DataFrame will need to have labels added first using the function add_labels()

```
applicant_types = aggregate_to_applicant_types(applicants)
```