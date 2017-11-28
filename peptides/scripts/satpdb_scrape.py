#SATPdb scrubber
#pulls 8 csv files from the satp database and combines them into one
#leaves duplicates but assigns an activity to each sequence
#Author: Jack McClure

import requests
import sys
import csv

myRequests = requests.session()

bactData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antibacterial.fasta")

cancData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/anticancer.fasta")

fungData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antifungal.fasta")

toxiData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/toxic.fasta")

tensData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antihypertensive.fasta")

micrData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antimicrobial.fasta")

paraData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antiparasitic.fasta")

viraData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antiviral.fasta")

header = 'sequence|activity\n'

destination_path = '../../data/downloads/satpdb_combined.csv'
destination = open(destination_path, 'w')
destination.write(header)

def readFile(activity, data):
	peptides = data.split("\n")

	for line in peptides:
		if line[0] != ">":
			line = line.rstrip()
			if len(line) <=50:
				destination.write(line + '|' + activity + '\n')
	return;

readFile('antibacterial', bactData.content.decode('utf-8'))
readFile('anticancer', cancData.content.decode('utf-8'))
readFile('antifungal', fungData.content.decode('utf-8'))
readFile('antihypertensive', tensData.content.decode('utf-8'))
readFile('antimicrobial', micrData.content.decode('utf-8'))
readFile('antiparasitic', paraData.content.decode('utf-8'))
readFile('antiviral', viraData.content.decode('utf-8'))
readFile('toxic', toxiData.content.decode('utf-8'))

myRequests.close()
destination.close()
