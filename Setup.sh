#!/bin/sh

#Author:Jake Schuurmans
#Peptide Database Setup bash script

sudo apt-get update

#LAMP: Ubuntu 16.04, Apache2, MongoDB, PHP7
sudo apt-get install apache2 php7.0 libapache2-mod-php7.0 mongodb -y

#Python3 (python3 should be installed by default on Ubuntu, this is precautionary)
sudo apt-get install python3 -y
#Need to install pip3 before you can use pip3 -y
sudo apt-get install python3-pip -y

#Python Mongodb API
sudo pip3 install pymongo

#Python extensions for all types of things that the writer of this setup.sh does not know
sudo pip3 install xlrd
sudo pip3 install beautifulsoup4
sudo pip3 install requests

#Install PHP MongoDB Driver

sudo apt-get install php-pear php7.0-dev libcurl4-openssl-dev -y
#Install the Driver
sudo pecl install mongodb

echo "\n*******************************************************\n*ADD \"extension=mongodb.so\" to \"apache2/php.ini\"     *\n*Type \"php --ini\" to find the files location. *\n*******************************************************"
