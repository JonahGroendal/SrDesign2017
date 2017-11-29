import requests
import sys
import json

data = requests.get('http://kaliumdb.org/data/toxins')

with open('../../data/downloads/kaliumdb.json', 'wb') as output:
    output.write(data.content)

data2 = json.loads(data.content.decode())
print(data2.keys())
