import sys
sys.path.append('peptides/')
import db
import db_schema

d = db.PeptideDB()
fields_to_print = [k for k in db_schema.peptide_db_schema["peptide"]["_for_each"]["_schema"] if k != "source"]
d.export_peptides_to_csv("site/res/db_dump.csv", fields_to_print, pretty=True)
