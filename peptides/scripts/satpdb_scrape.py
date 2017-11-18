#SATPdb scrubber
#Author: Jack McClure

import requests
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
