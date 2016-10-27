#!/bin/bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus git -y
sudo apt-get install python-lightblue bluez python-gobject python-dbus bluez-utils python-bluez -y
sudo pip install Adafruit_BBIO 
ntpdate -b -u -s pool.ntp.org
git clone https://github.com/RidwanAlam/besi-relay-station.git
cd /opt/scripts/tools/
./update_kernel.sh
reboot
