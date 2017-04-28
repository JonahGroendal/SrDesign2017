from lxml import html
import csv
import requests

#This should get the csv from the website.
#Also prints to .csv files
#Author: Jack McClure

myRequests = requests.session()

lampData = myRequests.get("http://biotechlab.fudan.edu.cn/database/lamp/db/lamp.fasta")

with open('lampdb.csv','wb') as csvfile:
	csvfile.write(lampData.content)
	csvfile.close()
	