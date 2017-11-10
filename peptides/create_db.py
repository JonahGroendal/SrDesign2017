import db
import definitions

# create database
db_object = db.PeptideDB(db_name="peptide")

# import csv
db_object.import_dataset("../data/clean/allergenonline.csv", {
    "url": "http://www.allergenonline.org/celiacbrowse.shtml",
    "institution": "University of Nebraska-Lincoln",
    "authors": ["Richard Goodman", "John Wise", "Sreedevi Lalithambika"]
})
db_object.import_dataset("../data/clean/amper.csv", {
    "url": "http://www.cnbi2.com/cgi-bin/amp.pl",
    "institution": ("Division of Infectious Diseases, Department of Medicine, Faculty"
            " of Medicine, University of British Columbia, Vancouver, BC, Canada"),
    "authors": ["Fjell CD", "Hancock RE", "Cherkasov A"]
})
#db_object.import_dataset("../csv/lampCleaned.csv")
