#SATPdb cleaner
#script to put records in canonical form
#each sequence occurs once with multiple features
#Author: Jack McClure

import sys
sys.path.append('../')
import csv_tools

def run():
    satp = csv_tools.Dataset()
    satp.import_csv("../../data/downloads/satpdb_combined.csv")

    satp.column_names = ["sequence", "activities"]

    satp.create_bool_column_from_value("activities", 'antibacterial', assume_false=False)
    satp.create_bool_column_from_value("activities", 'anticancer', assume_false=False)
    satp.create_bool_column_from_value("activities", 'antifungal', assume_false=False)
    satp.create_bool_column_from_value("activities", 'antihypertensive', assume_false=False)
    satp.create_bool_column_from_value("activities", 'antimicrobial', assume_false=False)
    satp.create_bool_column_from_value("activities", 'antiparasitic', assume_false=False)
    satp.create_bool_column_from_value("activities", 'antiviral', assume_false=False)
    satp.create_bool_column_from_value("activities", 'toxic', assume_false=False)
    satp.remove_rows_where_equals("sequence","STRUCTURE GIVEN")


    satp.conform_column_names()
    satp.remove_column("activities")

    satp.export_csv("../../data/clean/satpdb.csv")
