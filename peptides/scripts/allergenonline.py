import sys
sys.path.append('../')

import csv_tools

scrub = csv_tools.Scrub()
inspect = csv_tools.Inspect()

with open("../../data/downloads/allergenonline.csv") as rf:
    file_str = rf.read()

file_str = "http://www.allergenonline.org/celiacbrowse.shtml|University of Nebraska-Lincoln|Richard Goodman|John Wise|Sreedevi Lalithambika\n" + file_str
file_str = scrub.convert_quoted_csv(file_str)
file_str = scrub.conform_field_names(file_str,replace={"toxicity": "toxic"})

print(inspect.get_field_values(file_str, "toxic", only_unique=True))

with open("../../data/clean/allergenonline.csv", "w") as wf:
    wf.write(file_str)
