#SATPdb scrubber
#pulls 8 csv files from the satp database and combines them into one
#leaves duplicates but assigns an activity to each sequence
#Author: Jack McClure

import requests
import sys
import csv

#function cleans and combines data from separate urls to one csv
def dumpData(activity, data, destination):
    #delimitting based on newlines
    peptides = data.split('\n')

    #step through the entire buffer
    for line in peptides:
        if( line and line[0] != '>' and
        '-' not in line and '(' not in line): #skip to lines with sequences only
            line = line.rstrip()
            if len(line) <=50:
                contents = '%s|%s\n' % (line.upper(), activity)
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

with open(destination_path, 'wb') as output_file:
    output_file.write(header.encode('UTF-8'))
    #iterate through dictionary, downloading corresponding files and combining them
    for field in data_dict:
        data = requests.get("http://crdd.osdd.net/raghava/satpdb/%s.fasta" % field)
        dumpData(field, data.content.decode('UTF-8'), output_file)
