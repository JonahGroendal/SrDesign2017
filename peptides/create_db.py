import db

# create database
db_object = peptide_db.PeptideDB()

# import csv
db_object.import_csv("../csv/aonline_scrubbed.csv", delimiter=",")
#db_object.import_csv("../csv/lampCleaned.csv")
