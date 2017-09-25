source_path = "../PeptidePulls/downloads/AHTPDB.txt"
source = open(source_path, "r")
destination_path = "./scrubbed/AHTPDB_scrubbed.csv"
destination = open(destination_path, "w")

for line in source:
	line = line.rstrip()
	tokens = line.split('	')

	#Sequence:		tokens[1]
	#Source:		tokens[5]
	#Properties:	NA?
	#Source Data: http://crdd.osdd.net/raghava/ahtpdb/downloads/pepic50.txt

	for each in tokens:
		destination.write(each + ',')
	destination.write('\n')
