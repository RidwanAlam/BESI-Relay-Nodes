#!/bin/bash

ntpdate -b -s -u pool.ntp.org

# install dependencies
pip install https://gitlab.com/besi/libpebble2/repository/archive.zip?ref=master
apt-get update
apt-get install python-zmq
pip install msgpack-python
pip install redis
pip install supervisor

cp supervisord.service /etc/systemd/system/supervisord.service
