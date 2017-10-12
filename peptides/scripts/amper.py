import sys
sys.path.append('../')

import csv_tools
import urllib.request
from bs4 import BeautifulSoup

scrub = csv_tools.Scrub()

table_list = []
table_list = scrub.prepend_list(table_list, ("http://www.cnbi2.com/cgi-bin/amp.pl", "Division of Infectious Diseases, Department of Medicine, Faculty of Medicine, University of British Columbia, Vancouver, BC, Canada", "Fjell CD", "Hancock RE", "Cherkasov A"))

# Download page
response = urllib.request.urlopen("https://web.archive.org/web/20080212035640/http://www.cnbi2.com/cgi-bin/amp.pl?peptide=1&type=MATURE")
data = response.read()      # bytes object
html = data.decode('utf-8') # str
with open("../../data/downloads/amper.html", "w") as f1:
    f1.write(html)

# Extract data from html table
soup = BeautifulSoup(html, "lxml")
table = soup.find("table", attrs={"border": 1})

# Convert html table to list
for row in table.find_all("tr"):
    table_list.append([td.get_text() for td in row.find_all("td")])
del table_list[1][len(table_list[1])-1]

# Conform field names and remove unwanted fields
table_list = scrub.conform_field_names(table_list, rename={"HydrophobicFraction": "hydrophobicity", "Source Organism": "source"})
table_list = scrub.remove_unwanted_fields(table_list, "peptide")

# Write to file
table_csv = scrub.csv_str_from_list(table_list)
with open("../../data/clean/amper.csv", "w") as f2:
    f2.write(table_csv)
