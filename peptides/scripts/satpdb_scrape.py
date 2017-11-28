#SATPdb scrubber
#pulls 8 csv files from the satp database and combines them into one
#Author: Jack McClure

import requests
import sys
import csv

myRequests = requests.session()

bactData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antibacterial.fasta")
with open('../../data/downloads/satpdb/antibacterial.csv', 'wb') as csvfile:
    csvfile.write(bactData.content)
    csvfile.close()

cancData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/anticancer.fasta")
with open('../../data/downloads/satpdb/anticancer.csv', 'wb') as csvfile:
    csvfile.write(cancData.content)
    csvfile.close()

fungData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antifungal.fasta")
with open('../../data/downloads/satpdb/antifungal.csv', 'wb') as csvfile:
    csvfile.write(fungData.content)
    csvfile.close()

toxiData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/toxic.fasta")
with open('../../data/downloads/satpdb/toxic.csv', 'wb') as csvfile:
    csvfile.write(toxiData.content)
    csvfile.close()

tensData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antihypertensive.fasta")
with open('../../data/downloads/satpdb/antihypertensive.csv', 'wb') as csvfile:
    csvfile.write(tensData.content)
    csvfile.close()

micrData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antimicrobial.fasta")
with open('../../data/downloads/satpdb/antimicrobial.csv', 'wb') as csvfile:
    csvfile.write(micrData.content)
    csvfile.close()

paraData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antiparasitic.fasta")
with open('../../data/downloads/satpdb/antiparasitic.csv', 'wb') as csvfile:
    csvfile.write(paraData.content)
    csvfile.close()

viraData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antiviral.fasta")
with open('../../data/downloads/satpdb/antiviral.csv', 'wb') as csvfile:
    csvfile.write(viraData.content)
    csvfile.close()


header = 'sequence|activity\n'

destination_path = '../../data/downloads/satpdb_combined.csv'
destination = open(destination_path, 'w')
destination.write(header)

def readFile(activity):
    source_path = '../../data/downloads/satpdb/' + activity + '.csv'
    with open(source_path, 'r') as source:
        while True:
            line = source.readline()
            if not line: break  # EOF
            line = source.readline().rstrip()
            if len(line) <=50:
                destination.write(line + '|' + activity + '\n')
        source.close()
    return;

readFile(activity = 'antibacterial')
readFile(activity = 'anticancer')
readFile(activity = 'antifungal')
readFile(activity = 'antihypertensive')
readFile(activity = 'antimicrobial')
readFile(activity = 'antiparasitic')
readFile(activity = 'antiviral')
readFile(activity = 'toxic')

destination.close()
