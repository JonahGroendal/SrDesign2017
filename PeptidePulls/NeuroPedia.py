from lxml import html
import csv
import requests


myRequests = requests.session()

neuroData = myRequests.get("http://proteomics.ucsd.edu/Software/NeuroPedia/Downloads/Database_NeuroPedia_063011.xls")

with open('NeuroPedia.csv', 'wb') as csvfile:
	csvfile.write(neuroData.content)
	csvfile.close()
