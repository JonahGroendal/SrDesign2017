#automatically runs each download and clean script
#author: Jack McClure

import subprocess

#if a script downloads data, even if it cleans it in the script, insert here
downloads = ["allergenonline.py",
            "amper.py",
            "kalium_scrape.py",
            "satpdb_scrape.py"]

#if a script only cleans data insert it here
cleans = ["lamp.py",
        "kalium_clean.py",
        "satpdb_clean.py"]

for script in downloads:
    print(script)
    subprocess.run(script, shell = True)
for script in cleans:
    print(script)
    subprocess.run(script, shell = True)
