import requests
import os

r = requests.get('http://www.allergenonline.org/celiacbrowse.shtml')
f = open(os.path.dirname(os.path.realpath(__file__)) + '../downloads/ALLERGINONLINE.txt', 'w')
f.write(r.text)
f.close()
