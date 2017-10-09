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
f = open(os.path.dirname(os.path.realpath(__file__)) + '../downloads/aonline.csv')

#f = open("aonline.csv",encoding='utf8')
i = 0
for line in f:
    input = line
    input = input.rstrip()
    input = input.replace('\n','')
    input = input.replace('"','')
    input = input.split(",")

    if(input[8].isdigit()):
        pass
    else:
        try:
            post =  {
                    "type":input[1],
                    "description":input[2],
                    "form":input[4],
                    "toxicity":input[3],
                    "HLADQ":input[5],
                    "refs":input[6],
                    "seqlen":input[7],
                    "sequence":input[8],
                    "peptide source":"http://www.allergenonline.org/celiacbrowse.shtm",
                    "_id":input[8] #sequence
            }
            result = db.test3.insert_one(post)
        except:
            print("key " + input[8] + " already in db")
    i = i + 1

#collection = db.test9
#cursor = collection.find({})
#for u in cursor:
#    print(u)
