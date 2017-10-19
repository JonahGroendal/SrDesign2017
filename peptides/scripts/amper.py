import sys
sys.path.append('../')
import csv_tools
from bs4 import BeautifulSoup

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

# Conform field names and remove undefined fields
amper = csv_tools.Dataset(("http://www.cnbi2.com/cgi-bin/amp.pl", ("Division of Infectious Diseases, "
        "Department of Medicine, Faculty of Medicine, University of British Columbia, Vancouver, BC, "
"Canada"), "Fjell CD", "Hancock RE", "Cherkasov A"), table=table_list)
amper.conform_field_names(rename={"HydrophobicFraction": "hydrophobicity", "Source Organism": "source"})
amper.remove_undefined_fields("peptide")

scrub.write_to_file("../../data/clean/amper.csv", amper.to_csv_string())
