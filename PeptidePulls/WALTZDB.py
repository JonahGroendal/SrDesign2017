## separate directories for each website to avoid global var issues
##
## are there database lookups for canonical sequence names
## Sequence, name, length, source, "reactions"?, fereferences, type
## true or false per field
##
## raw dump - careful of comments
## check sequence length actually matches
##

from pymongo import MongoClient
import codecs
import os

client = MongoClient()
db = client.test
f = open(os.path.dirname(os.path.realpath(__file__)) + '/downloads/waltzdb_export.csv')

#f = open("aonline.csv",encoding='utf8')
i = 0
for line in f:
    input = line
    input = input.rstrip()
    input = input.replace('\n','')
    input = input.replace('"','')
    input = input.split(",")

    if(input[4].isdigit()):
        pass
    else:
        try:
            post =  {
                    "classification":input[0],
                    "subset":input[9],
                    "WALTZ":input[8],
                    "TANGO":input[5],
                    "proteostat binding":input[3],
                    "seqlen":len(input[4]),
                    "sequence":input[4],
                    "peptide source":"http://waltzdb.switchlab.org",
                    "_id":input[4] #sequence
            }
            result = db.test3.insert_one(post)
        except:
            print("key " + input[4] + " already in db")
    print(i)
    i = i + 1

#collection = db.test9
#cursor = collection.find({})
#for u in cursor:
#    print(u)
