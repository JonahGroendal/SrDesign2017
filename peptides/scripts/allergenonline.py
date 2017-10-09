import sys
sys.path.append('../')

import csv_tools

scrub = csv_tools.Scrub()
inspect = csv_tools.Inspect()

with open("../../data/downloads/allergenonline.csv") as rf:
    file_str = rf.read()

file_list = scrub.quoted_csv_str_to_list(file_str)
file_list = scrub.prepend_list(file_list, ("http://www.allergenonline.org/celiacbrowse.shtml", "University of Nebraska-Lincoln", "Richard Goodman", "John Wise", "Sreedevi Lalithambika"))
file_list = scrub.conform_field_names(file_list)

file_list = scrub.create_bool_field_from_value(file_list, "toxicity", "Immunogenic", assume_false=True)
file_list = scrub.create_bool_field_from_value(file_list, "toxicity", "Toxic", assume_false=True)
file_list = scrub.conform_field_names(file_list)
file_list = scrub.remove_unwanted_fields(file_list, "peptide")

file_str = scrub.list_to_csv_str(file_list)

with open("../../data/clean/allergenonline.csv", "w") as wf:
    wf.write(file_str)
