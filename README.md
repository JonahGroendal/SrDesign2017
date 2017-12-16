#Copyright notice GNU GPL 2.0
Copyright (C) 2017  Angelo Danducci II, Jonah Groendal, Joshua Looney, Jack McClure, Jacob Schuurmans

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


#data
data/clean contains csv files that are ready to be inserted into the database
data/downloads contains raw data pulled from the sources, it is in various formats
data/svn contains a sample json object retrieved from the database

#peptides
contains libraries and scripts to create the databases
peptides/scripts contains scripts for downloading and cleaning the data into canonical form.
csv_tools.py is a library with tools for cleaning data in some sort of csv format
db.py is a library with functions necessary for interacting with the database
db_schema.py is the schema for our database, it contains a dict with each activity
    when adding or removing an activity from the database, it must be added to this file as well
    if an activity is removed you must remove it from each csv in data/clean as well.
create_db.py is a script to create the database or update it
    when adding or removing a csv to the database the file must be added to this script
    information regarding the source of the data must also be added to this script
new data collection scripts should go in the peptides/scripts folder
    scripts are named based on the database they retrieve data from
    if you create a separate download and cleaning script make sure to name them as such


#canonical form
the format for inputting data into the database is a csv file separated by '|' character
there should be a column for each activity exhibited in the data, where a 1 is True, 0 is False
non boolean if the activity is not true/false
None indicates there is no data for that peptide regarding the activity
csv files should be encoded in UTF-8

#website
contained in site directory
site/css contains css code
site/js contains javascript code
site/res contains resource such as text files the website uses
site/vendor contains php mongo driver so the website can access database
res/activities.txt contains a list of active activities in the database. The website uses this to dynamically build the site. Update these with more activities when more data is entered into the site.
index.php is the primary website page

#setup
run the Setup.sh script to install necessary components for the project to run on a Ubuntu 16.04 system
python code is written in python3.6.3 so to run it in Ubuntu 16.04 LTS. use command python3
