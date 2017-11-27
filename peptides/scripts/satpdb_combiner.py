#author Jack McClure
#script to combine all satpdb files
#this leaves duplicates, peptides with multiple activities appear
#multiple times, once for each activity

import sys
sys.path.append('../')
import definitions


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
