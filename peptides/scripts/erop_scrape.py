#EROP-Moscow scrubber
#pulls many files from EROP website
#leaves duplicates but assigns an activity to each instance
#Author: Jack McClure

import requests
import sys
import csv

#function cleans and combines data from separate urls to one csv
def cleanData(activity, data, destination):
    #delimitting based on newlines
    peptides = data.split('\n')
    seq = None

    #
    for line in peptides:
        line = line.rstrip()
        if line and line[0] == '>':
            tokens = line.split('|')
            #pulls out source
            contents = "%s" % tokens[2]
        #pull the peptide sequence, if statements to account for inconsistent entries
        if line and line[0] != '>' and line != seq and len(line) > 1:
            seq = line
            if seq[0] == '+':
                seq = seq[1:]
            if seq[-1] == '-':
                seq = seq[:-1]
            if len(seq) <=50:
                contents = "%s|%s|%s\n" % (contents, seq.upper(), activity)
                destination.write(contents.encode('ISO-8859-1'))
    return;
#very long URL, with key value in the middle
#separating into two strings for easier use later
url_prefix = ('http://erop.inbi.ras.ru/result1.php?EROP_NMB_K=&PEP_NAME_K=&FAM_NAME_K=&ALL_KAR__K=&ALL_KGD__K=&'
            'ALL_PHYL_K=&ALL_B_CL_K=&Organism=&SPECIES__K=&ALL_TISS_K=&SEQ_1____K=&AAR_SUM__K1=&'
            'AAR_SUM__K2=&M_W______K1=&M_W______K2=&PI_______K1=&PI_______K2=&FUNC_CL__K=')
url_suffix = ('&SEQ_REFA_V=&SEQ_REFT_V=&SEQ_REFJ_V=&YEAR_SEQ_V1=&YEAR_SEQ_V2=&'
            'COUNTRY__V=&page_mode=Download_Fasta&Submit=Download FASTA')

filepath = "../../data/downloads/erop.csv"
header = 'source|sequence|activities\n'

data_dict = {
    'allergic':'',
    'antimicrobial':'',
    'antitumour':'',
    'antiviral':'',
    'toxin':'',
}
#open file to write in binary
with open(filepath, "wb") as output_file:
    output_file.write(header.encode('ISO-8859-1'))
    #grabbing entries using website's function dropdown list
    for field in data_dict:
        url = '%s%s&FUNCTION_K=%s' % (url_prefix, field, url_suffix)
        data = requests.get(url)
        cleanData(field, data.content.decode('ISO-8859-1'), output_file)
    #grabbing entry using function keyword search
    field = 'antifungal'
    #correcting for strange error inconsistent with above example
    url = url_prefix + "&FUNCTION_K=%s" % field + url_suffix
    data = requests.get(url)
    cleanData(field, data.content.decode('ISO-8859-1'), output_file)
