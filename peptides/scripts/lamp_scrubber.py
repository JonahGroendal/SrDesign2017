#author Jack McClure
#scrubbing script to standardize lampdb.csv
import sys
sys.path.append('../')

#import csv_tools
import definitions

source_path = "../../data/downloads/lampdb.csv"
source = open(source_path, "r")
destination_path = "../../data/clean/lampclean.csv"
destination = open(destination_path, "w")
header = "sequence|name|source|activity|\n"
destination.write(header)
while True:
    line = source.readline()
    if not line: break  # EOF
    line = line.rstrip()
    line += "|" + source.readline().rstrip()
    line = line.lstrip('>')
    record = line.split('|')
    record[5] = record[5].replace(',','|')
    if len(record) == 7:
        if len(record[6]) <= 50:
            if record[4] != "predicted":
                destination.write(record[6]+"|"+record[1]+"|"+record[2]+"|"+record[5]+"|\n")
    if len(record) == 8: #accounts for discrepencies/typos that extend a record
        if len(record[7]) <=50:
            if record[5] != "predicted":
                destination.write(record[7]+"|"+record[1]+"-"+record[2]+"|"+record[3]+"|"+record[6]+"|\n")
