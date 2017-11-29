#SATPdb scrubber
#pulls 8 csv files from the satp database and combines them into one
#leaves duplicates but assigns an activity to each sequence
#Author: Jack McClure

import requests
import sys
import csv

def dumpData(activity, data, destination):
    peptides = data.split('\n')

    for line in peptides:
        if line and line[0] != '>':
            line = line.rstrip()
            if len(line) <=50:
                contents = line + '|' + activity + '\n'
                destination.write(contents.encode('UTF-8'))
    return;

destination_path = '../../data/downloads/satpdb_combined.csv'
header = 'sequence|activity\n'

data_dict = {
    'antibacterial': '',
    'anticancer': '',
    'antifungal': '',
    'antihypertensive': '',
    'antimicrobial': '',
    'antiparasitic': '',
    'antiviral': '',
    'toxic': ''
}

with requests.session() as myRequests:
    bactData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antibacterial.fasta")
    cancData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/anticancer.fasta")
    fungData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antifungal.fasta")
    tensData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antihypertensive.fasta")
    micrData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antimicrobial.fasta")
    paraData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antiparasitic.fasta")
    viraData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/antiviral.fasta")
    toxiData = myRequests.get("http://crdd.osdd.net/raghava/satpdb/toxic.fasta")

with open(destination_path, 'wb') as output_file:
    output_file.write(header.encode('UTF-8'))
    dumpData('antibacterial', bactData.content.decode('UTF-8'), output_file)
    dumpData('anticancer', cancData.content.decode('UTF-8'), output_file)
    dumpData('antifungal', fungData.content.decode('UTF-8'), output_file)
    dumpData('antihypertensive', tensData.content.decode('UTF-8'), output_file)
    dumpData('antimicrobial', micrData.content.decode('UTF-8'), output_file)
    dumpData('antiparasitic', paraData.content.decode('UTF-8'), output_file)
    dumpData('antiviral', viraData.content.decode('UTF-8'), output_file)
    dumpData('toxic', toxiData.content.decode('UTF-8'), output_file)
