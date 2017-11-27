__author__ = "Jonah Groendal"

import sys
sys.path.append('../')
import csv_tools
from bs4 import BeautifulSoup
import definitions

scrub = csv_tools.Scrub()

# Download page
html = scrub.download_html_to_file("../../data/downloads/amper.html",
        "https://web.archive.org/web/20080212035640/http://www.cnbi2.com/cgi-bin/amp.pl?peptide=1&type=MATURE")

# Extract data from html table
soup = BeautifulSoup(html, "lxml")
table = soup.find("table", attrs={"border": 1})

# Convert html table to list
table_list = []
for row in table.find_all("tr"):
    table_list.append([td.get_text() for td in row.find_all("td")])
del table_list[0][len(table_list[0])-1]

# Conform column names and remove undefined columns
amper = csv_tools.Dataset()
amper.table = table_list
amper.conform_column_names(rename={"HydrophobicFraction": "hydrophobicity", "Source Organism": "source"})
amper.remove_all_columns_except([k for k in definitions.collections_def["peptide"]["_list_def"]["_dict_def"]])
# Remove rows where lenth of sequence > 50
amper.remove_rows_where("sequence", lambda value: len(value) > 50)

scrub.write_to_file("../../data/clean/amper.csv", amper.to_csv_string())
