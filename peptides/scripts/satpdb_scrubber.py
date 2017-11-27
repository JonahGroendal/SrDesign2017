#author Jack McClure
#script to put records in canonical form
#this leaves duplicates, peptides with multiple activities appear
#multiple times, once for each activity

import sys
sys.path.append('../')
import definitions
import csv_tools

satp = csv_tools.Dataset()
satp.import_csv("../../data/downloads/satpdb_combined.csv", encoding="ISO-8859-1")

satp.column_names = ["sequence", "activities"]

satp.create_bool_column_from_value("activities", 'antibacterial', assume_false=False)
satp.create_bool_column_from_value("activities", 'anticancer', assume_false=False)
satp.create_bool_column_from_value("activities", 'antifungal', assume_false=False)
satp.create_bool_column_from_value("activities", 'antihypertensive', assume_false=False)
satp.create_bool_column_from_value("activities", 'antimicrobial', assume_false=False)
satp.create_bool_column_from_value("activities", 'antiparasitic', assume_false=False)
satp.create_bool_column_from_value("activities", 'antiviral', assume_false=False)
satp.create_bool_column_from_value("activities", 'toxic', assume_false=False)

satp.conform_column_names()

satp.export_csv("../../data/clean/satpdb.csv")
