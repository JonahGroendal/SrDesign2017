#!/bin/sh

#Author:Jake Schuurmans
#Peptide Database Setup bash script

sudo apt-get update

#LAMP: Ubuntu 16.04, Apache2, MongoDB, PHP7
sudo apt-get install apache2 php7.0 libapache2-mod-php7.0 -y

#MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

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

sudo apt-get install php-pear php-dev libcurl4-openssl-dev pkg-config python-software-properties software-properties-common -y
sudo apt-get update
sudo apt-get install php7.0 libapache2-mod-php7.0
sudo apt-get install mongodb
#Install the Driver
sudo pecl install mongodb

#Text that needs to be inserted for PHP MongoDB driver
sudo bash -c "echo 'extension=mongodb.so' >> /etc/php/7.0/apache2/php.ini"

echo "***********************************ATTENTION**************************************\nVerify the root directory of Apache2 is that of SrDesign2017/site/\n\nHowTo:\n";
echo "Once everything is installed, you must either move 'site/*' to apache's root directory, or move apache'2 root directory to 'site'. To move the root directory, there are two things you must change\n.";
echo "In /etc/apache2, you must find '<Directory /var/www/html >' and replace it with '<Directory /path/to/site>'.\n";
echo "Then in '/etc/apache2/sites-available' you must change 'DocumentRoot /var/www/html' to 'DocumentRoot /path/to/site'.";
