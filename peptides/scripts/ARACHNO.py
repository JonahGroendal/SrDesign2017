import requests
import os

r = requests.get('http://www.arachnoserver.org/fasta/all.pep.fa')
f = open(os.path.dirname(os.path.realpath(__file__)) + '../downloads/ARACHNO.txt', 'w')
f.write(r.text)
f.close()
