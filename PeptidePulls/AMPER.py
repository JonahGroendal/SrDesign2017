import requests
import os

r = requests.get('https://web.archive.org/web/20080212035640/http://www.cnbi2.com/cgi-bin/amp.pl?peptide=1&type=MATURE')
f = open(os.path.dirname(os.path.realpath(__file__)) + '/downloads/AMPER.txt', 'w')
f.write(r.text)
f.close()
