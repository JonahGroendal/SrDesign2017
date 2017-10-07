import re

source_path = "../downloads/aonline.csv"
source = open(source_path, "r")
destination_path = "../clean/aonline_scrubbed.csv"
destination = open(destination_path, "w")

for line in source:

	#Replace ','s with '	' when between '"'s.
	#Replace commas with tabs when between double quotes
	i = 0
	inside_quotes = 0
	while i < len(line):
		if line[i] == "\"":
			if inside_quotes == 0:
				inside_quotes = 1
			else:
				inside_quotes = 0
		#if inside a quote, remove ','s
		elif line[i] == ',' and inside_quotes == 1:
			line = line[:i].strip() + "	" + line[i + 1:].strip()
			i -= 1
		i += 1

	#Remove double quotes
	line = line.strip()
	tokens = line.split(',')

	#Place in file
	for each in tokens:
		destination.write(each.strip("\"") + ',')
	destination.write('\n')
	#
	#
	#Sequence:		tokens[8]
	#Source:		NA?
	#Properties:	Toxic: + tokens[3]
	#Source Data:	?
