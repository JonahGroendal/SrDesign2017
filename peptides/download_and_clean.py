import sys
sys.path.insert(0, './scripts')
import allergenonline
import amper
import lamp
import satpdb_scrape
import satpdb_clean
import kalium_scrape
import kalium_clean

# Download and clean sources
allergenonline.run()
amper.run()
lamp.run()
satpdb_scrape.run()
satpdb_clean.run()
kalium_scrape.run()
kalium_clean.run()
