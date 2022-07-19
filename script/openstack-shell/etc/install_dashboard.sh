#!/bin/bash
NAMEHOST=$HOSTNAME
line=`wc -l /var/log/install_log | awk '{print$1}'`
if [ $line -eq 10 ]
then
	echo "graph had installed."
else
	echo -e "\033[41;37m you should install graph first. \033[0m"
	exit
fi

cat /var/log/install_log | grep dashboard
if [ $? -eq 0 ]
then
	echo "you had install dashboard ."
	exit
fi

yum install openstack-dashboard && [ -f /etc/openstack-dashboard/local_settings.bak ] || mv /etc/openstack-dashboard/local_settings /etc/openstack-dashboard/local_settings.bak
cp $PWD/lib/local_settings /etc/openstack-dashboard/local_settings && systemctl restart httpd.service memcached.service && echo "Access the dashboard using a web browser at http://controller/dashboard." && echo "dashboard" >> /var/log/install_log
echo -e "\033[32m ################################# \033[0m"
echo -e "\033[32m ##   install dashboard sucessed.# \033[0m"
echo -e "\033[32m ################################# \033[0m"
