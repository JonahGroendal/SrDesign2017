#Cleans json from kaliumdb
#Author: Jack McClure 11/29/2017

import sys
import json

with open('../../data/downloads/kaliumdb.json') as raw_data:
    data = json.loads(raw_data.read())
header = 'sequence|source|toxic\n'
record = [header]
for i in data['pl']:
    sequence = i['fields']['seq']
    source = i['fields']['organism'][0]
    #name = i['fields']['trivial_names'] omitted due to conflicts
    if len(sequence) <= 50:
        entry = '%s|%s|1\n' % (sequence,source)
        record.append(entry)

with open('../../data/clean/kaliumdb.csv','wb') as out:
    for i in record:
        out.write(i.encode("utf-8"))
