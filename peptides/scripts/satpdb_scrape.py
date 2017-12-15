#SATPdb scrape
#pulls 8 csv files from the satp database and combines them into one
#eliminates duplicates from each file and adds multiple features per line
#Author: Jack McClure

import requests
import sys
import csv
import re
from collections import defaultdict

def run():
    #regular expression to limit sequences to our standard, only a-z
    seq_req = re.compile('^[a-zA-Z]+$')
    destination_path = '../../data/downloads/satpdb_combined.csv'
    header = 'sequence|activity\n'

    #dictionary to store all of our data, contains lists which will hold activities
    data_dict = defaultdict(list)

    #list of activities and filenames
    file_list = ['antibacterial',
                'anticancer',
                'antifungal',
                'antihypertensive',
                'antimicrobial',
                'antiparasitic',
                'antiviral',
                'toxic']


    #iterate through list, downloading corresponding files and combining them
    for field in file_list:

        #download the data from the website and store it into a list separated by lines
        #data for this website is arranged in separate files which only contain sequences
        #these sequences are confirmed for the activity named by the file
        #if a new activity is added to the database add it to file_list
        download = requests.get("http://crdd.osdd.net/raghava/satpdb/%s.fasta" % field).content.decode('UTF-8').split('\n')

        #store the data downloaded into a set to eliminate duplicates in each file
        #sequences with only capital letters of length 50 or less
        rawdata = set([line.upper() for line in download if seq_req.match(line) and len(line) <= 50])
        #add the activity from the filename to our list for the given sequence
        for sequence in rawdata:
            data_dict[sequence].append(field)

    with open(destination_path, 'wb') as output_file:
        output_file.write(header.encode('UTF-8'))
        #sorts first by length then by alphabetical order
        #short sequences should appear first, in alphabetical order
        for sequence in sorted(data_dict, key=lambda k: "%02d_%s" % (len(k), k)):

            output_file.write(("%s|%s\n" % (sequence, ','.join(data_dict[sequence]))).encode('UTF-8'))
