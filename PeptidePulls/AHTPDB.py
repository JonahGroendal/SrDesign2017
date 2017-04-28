import requests
import os

r = requests.get('http://crdd.osdd.net/raghava/ahtpdb/downloads/pepic50.txt')
f = open(os.path.dirname(os.path.realpath(__file__)) + '/downloads/AHTPDB.txt', 'w')
f.write(r.text)
f.close()
