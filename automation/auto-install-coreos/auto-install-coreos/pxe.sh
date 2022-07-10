#!/bin/bash
mac_addr=`ip a | grep -A3 'enp' | grep ether | awk '{print $2}' | tr '[a-z]' '[A-Z]'`
wget http://192.168.1.4/${mac_addr}.yml
sudo coreos-install -d /dev/sda -c ${mac_addr}.yml -b http://192.168.1.4
sudo reboot
