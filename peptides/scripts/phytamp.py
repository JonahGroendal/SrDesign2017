import sys
sys.path.append('../')

import csv_tools

scrub = csv_tools.Scrub()
inspect = csv_tools.Inspect()

print(inspect.get_excel_sheet_names("../../data/downloads/phytamp.xls"))

#with open("../../data/clean/phytamp.csv", "w") as f:
#    f.write(file_str)
