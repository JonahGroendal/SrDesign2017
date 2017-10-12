import db

# create database
db_object = db.PeptideDB()

# import csv
db_object.import_csv("../data/clean/allergenonline.csv")
db_object.import_csv("../data/clean/amper.csv")
#db_object.import_csv("../csv/lampCleaned.csv")
