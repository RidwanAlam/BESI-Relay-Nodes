#!/bin/bash
mkdir /media/card
mount -v /dev/mmcblk1p1 /media/card
cp uEnv.txt /media/card/uEnv.txt
sed -i '$ a /dev/mmcblk0p1 /media/card auto auto,rw,async,user,nofail 0 0' /etc/fstab
reboot
