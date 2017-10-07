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
f = open(os.path.dirname(os.path.realpath(__file__)) + '../downloads/AHTPDB.txt')

#f = open("aonline.csv",encoding='utf8')
i = 0
for line in f:
    input = line
    input = input.replace('\n','')
    input = input.replace('"','')
    input = input.split("\t")
    #print(input[1] + "    " + input[2])

    if(1):
        pass
    else:
        try:
            post =  {
                    "assay":input[8],
                    "bitter":input[9],
                    "pi":input[10],
                    "bp":input[11],
                    "method":input[7],
                    "mice":input[6],
                    "source":input[5],
                    "ic50":input[4],
                    "molecular weight":input[3],
                    "seqlen":input[2],
                    "sequence":input[1],
                    "peptide source":"http://crdd.osdd.net/raghava/ahtpdb/downloads/pepic50.txt",
                    "_id":input[1] #sequence
            }
            result = db.test3.insert_one(post)
        except:
            print("key " + input[1] + " already in db")
    i = i + 1

#collection = db.test9
#cursor = collection.find({})
#for u in cursor:
#    print(u)
