import sys
sys.path.append('peptides/')
import db
import db_schema

d = db.PeptideDB()
fields_to_print = [k for k in definitions.collection_peptide["_dict_def"] if k != "source"]
d.export_peptides_to_csv("db_dump.csv", fields_to_print)
