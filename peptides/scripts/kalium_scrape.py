#downloads data from kaliumdb.org and saves in json
#Author: Jack McClure 11/28/2017

import requests
import sys
import json

def run():
    data = requests.get('http://kaliumdb.org/data/toxins')

    with open('../../data/downloads/kaliumdb.json', 'wb') as output:
        output.write(data.content)
