#author Jack McClure
#script to put records in canonical form
#this leaves duplicates, peptides with multiple activities appear
#multiple times, once for each activity

import sys
sys.path.append('../')
import definitions
import csv_tools

erop = csv_tools.Dataset()
erop.import_csv("../../data/downloads/erop.csv", encoding="ISO-8859-1")

erop.column_names = ["source","sequence", "activities"]

erop.create_bool_column_from_value("activities", 'allergic', assume_false=False)
erop.create_bool_column_from_value("activities", 'antifungal', assume_false=False)
erop.create_bool_column_from_value("activities", 'antimicrobial', assume_false=False)
erop.create_bool_column_from_value("activities", 'antitumour', assume_false=False)
erop.create_bool_column_from_value("activities", 'antiviral', assume_false=False)
erop.create_bool_column_from_value("activities", 'toxin', assume_false=False)

erop.conform_column_names(rename={"allergic": "allergen", "antitumour": "anticancer", "toxin": "toxic"})
erop.remove_column("activities")

erop.export_csv("../../data/clean/eropdb.csv")
