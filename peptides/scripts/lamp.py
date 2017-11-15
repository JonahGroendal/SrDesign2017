import sys
sys.path.append('../')

import csv_tools
import definitions

lamp = csv_tools.Dataset()
lamp.import_csv("../../data/downloads/lampdb.csv", encoding="ISO-8859-1")
# sequence is stored in every other row, combine to fix
for i in range(int(len(lamp.table) / 2)):
    lamp.combine_rows((i, i + 1))
# Insert header row
lamp.table.insert(0, ["id", "patent_details", "source", "syn_or_nat", "found", "activities", "sequence"])
# Fix rows that contained an extra "|"
lamp.table[1092][1] = lamp.table[1092][1] + lamp.table[1092][2]
del lamp.table[1092][2]
lamp.table[5446][1] = lamp.table[5446][1] + lamp.table[5446][2]
del lamp.table[5446][2]
lamp.table[5448][1] = lamp.table[5448][1] + lamp.table[5448][2]
del lamp.table[5448][2]
lamp.table[5449][1] = lamp.table[5449][1] + lamp.table[5449][2]
del lamp.table[5449][2]
lamp.table[5450][1] = lamp.table[5450][1] + lamp.table[5450][2]
del lamp.table[5450][2]
lamp.table[5451][1] = lamp.table[5451][1] + lamp.table[5451][2]
del lamp.table[5451][2]
lamp.table[5453][1] = lamp.table[5453][1] + lamp.table[5453][2]
del lamp.table[5453][2]
lamp.table[5454][1] = lamp.table[5454][1] + lamp.table[5454][2]
del lamp.table[5454][2]
# Exclude all besides "experimental"
lamp.remove_rows_where_equals("found", "Predicted")
# lamp.remove_rows_where_equals("found", "Patent")
# lamp.remove_rows_where_equals("found", "patent")
# Separate activities into their own boolean columns
# Only using assume_false=True if there are many records with this property
lamp.create_bool_column_from_value("activities", "Antibacterial", assume_false=True)
lamp.create_bool_column_from_value("activities", "Antiviral", assume_false=True)
lamp.create_bool_column_from_value("activities", "Antifungal", assume_false=True)
lamp.create_bool_column_from_value("activities", "Antimicrobial", assume_false=True)
lamp.create_bool_column_from_value("activities", "Anticancer", assume_false=False)
lamp.create_bool_column_from_value("activities", "Antiparasitic", assume_false=False)
lamp.create_bool_column_from_value("activities", "Insecticidal", assume_false=False)
# column_names to lowercase
lamp.conform_column_names()
# Shown to determine if we should assume_false in our previoulsy created bool columns
print("Num antibacterial rows:", len([v for v in lamp.table if v[lamp.table[0].index("antibacterial")] is True]))
print("Num antiviral rows:", len([v for v in lamp.table if v[lamp.table[0].index("antiviral")] is True]))
print("Num anticancer rows:", len([v for v in lamp.table if v[lamp.table[0].index("anticancer")] is True]))
print("Num antifungal rows:", len([v for v in lamp.table if v[lamp.table[0].index("antifungal")] is True]))
print("Num antiparasitic rows:", len([v for v in lamp.table if v[lamp.table[0].index("antiparasitic")] is True]))
print("Num insecticidal rows:", len([v for v in lamp.table if v[lamp.table[0].index("insecticidal")] is True]))
print("Num antimicrobial rows:", len([v for v in lamp.table if v[lamp.table[0].index("antimicrobial")] is True]))
# Remove undefined columns
lamp.remove_all_columns_except([k for k in definitions.collection_peptide["fields"]])

lamp.export_csv("../../data/clean/lamp.csv")
