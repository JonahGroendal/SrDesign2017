from lxml import html
import csv
import requests

#This should get the csv from the website.
#Also prints to .csv files
#Author: Jack McClure

myRequests = requests.session()

waltData = myRequests.get("http://waltzdb.switchlab.org/sequences/csv?field_hydrophobicity_value[min]=0&amp;field_hydrophobicity_value[max]=100")

with open('waltzdb.csv', 'wb') as csvfile:
	csvfile.write(waltData.content)
	csvfile.close()
