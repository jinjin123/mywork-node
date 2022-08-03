#!/bin/bash
#VPN gz
IP=192.168.50.15
ping -c 5 $IP &> /dev/null
if [ "$?" != 0 ];then
	echo "0"
else
	echo "1"
fi
