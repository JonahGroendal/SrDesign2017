source_path = "../downloads/AHTPDB.txt"
source = open(source_path, "r")
destination_path = "../clean/AHTPDB_scrubbed.csv"
destination = open(destination_path, "w")

for line in source:
	line = line.rstrip()
	tokens = line.split('	')

	#Place in file
	for each in tokens:
		destination.write(each + ',')
		destination.write('\n')
	#
	#
	#Sequence:		tokens[1]
	#Source:		tokens[5]
	#Properties:	NA?
	#Source Data: http://crdd.osdd.net/raghava/ahtpdb/downloads/pepic50.txt
