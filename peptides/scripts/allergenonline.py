import sys
sys.path.append('../')

import csv_tools
import definitions

#http://www.allergenonline.org/celiacbrowse.shtml

scrub = csv_tools.Scrub()
file_str = scrub.read_from_file("../../data/downloads/allergenonline.csv")
csv_str = scrub.csv_str_from_quoted_csv_str(file_str)

allergenonline = csv_tools.Dataset()
allergenonline.csv_into_table(csv_str)
allergenonline.remove_last_row()
allergenonline.conform_field_names()
allergenonline.create_bool_field_from_value("toxicity", "Immunogenic", assume_false=True)
allergenonline.create_bool_field_from_value("toxicity", "Toxic", assume_false=True)
allergenonline.conform_field_names()
allergenonline.remove_all_fields_except([k for k in definitions.collection_peptide["fields"]])
allergenonline.export_csv("../../data/clean/allergenonline.csv")
#scrub.write_to_file("../../data/clean/allergenonline.csv", allergenonline.to_csv_string())
