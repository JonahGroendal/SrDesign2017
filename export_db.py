import sys
sys.path.append('peptides/')
import db
import definitions

d = db.PeptideDB()
fields_to_print = [k for k in definitions.collection_peptide["fields"] if k not in "source"]
d.export_peptides_to_csv("db_dump.csv", fields_to_print)
