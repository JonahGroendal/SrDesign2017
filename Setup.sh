#!/bin/sh
sudo apt-get update

#LAMP: Ubuntu 16.04, Apache2, MongoDB, PHP7
sudo apt-get install apache2 libapache2-mod-php7.0 mongodb -y

#Python3 (python3 should be installed by default on Ubuntu, this is precautionary)
sudo apt-get install python3 -y
#Need to install pip3 before you can use pip3 -y
sudo apt-get install python3-pip -y
sudo pip3 install xlrd
sudo pip3 install pymongo
sudo pip3 install beautifulsoup4
sudo apt-get update
