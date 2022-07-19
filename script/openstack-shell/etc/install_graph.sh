#!/bin/bash
NAMEHOST=$HOSTNAME
line=`wc -l /var/log/install_log | awk '{print$1}'`
if [ $line -eq 9 ]
then
	echo "neutron had installed."
else
	echo -e "\033[41;37m you should install neutron first. \033[0m"
	exit
fi
cat /var/log/install_log | grep graph
if [ $? -eq 0 ]
then
	echo "you had install graph ."
	exit
fi

mongo --host ${HOSTNAME} --eval '
  db = db.getSiblingDB("ceilometer");
  db.createUser({user: "ceilometer",
  pwd: "CEILOMETER_DBPASS",
  roles: [ "readWrite", "dbAdmin" ]})'

source /root/admin-openrc.sh 
USER_CEILOMETER=`openstack user list | grep neutron | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_CEILOMETER}x = ceilometerx ]
then
	echo "openstack user had created  ceilometer"
else
	openstack user create ceilometer --password ceilometer --domain default
	echo "openstack user create ceilometer --password ceilometer --domain default"
	openstack role add --project service --user ceilometer admin
	echo "openstack role add --project service --user ceilometer admin"
fi

SERVICE_CEILOMETER=`openstack service list | grep ceilometer | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${SERVICE_CEILOMETER}x = ceilometerx ]
then
	echo "openstack service  created  ceilometer"
else
	openstack service create --name ceilometer --description "Telemetry" metering
    echo "create ceilometer service"
fi

ENDPOINT_CEILOMETER=`openstack endpoint list | grep ceilometer | awk -F "|" '{print$4}' | awk '{if($1=="ceilometer"){print $1,$2,$3;exit}}'`
if [ ${ENDPOINT_CEILOMETER}x = ceilmeterx ]
then
	echo "openstack endpoint create ceilometer"
else
	 openstack endpoint create --region RegionOne metering public http://controller:8777 && openstack endpoint create --region RegionOne metering internal http://controller:8777 && openstack endpoint create --region RegionOne metering admin http://controller:8777
	 echo "openstack endpoint create ceilometer"
fi

echo "install ceilometer packages,wait for minute..."
yum clean all && yum install openstack-ceilometer-api openstack-ceilometer-collector openstack-ceilometer-notification openstack-ceilometer-central python-ceilometerclient
[ -f /etc/ceilometer/ceilometer.conf.bak ] ||  mv /etc/ceilometer/ceilometer.conf /etc/ceilometer/ceilometer.conf.bak
cp -a $PWD/lib/ceilometer.conf /etc/ceilometer/ceilometer.conf

systemctl enable openstack-ceilometer-api.service openstack-ceilometer-notification.service openstack-ceilometer-central.service openstack-ceilometer-collector.service
systemctl start openstack-ceilometer-api.service openstack-ceilometer-notification.service openstack-ceilometer-central.service openstack-ceilometer-collector.service && \
systemctl restart openstack-glance-api.service openstack-glance-registry.service || result=1
if [ ${result} -eq 1 ] 
then
	echo "check the glance and ceilometer log"
fi

echo "wait for minute to  restart  nova service..."
yum install openstack-ceilometer-compute python-ceilometerclient python-pecan && systemctl enable openstack-ceilometer-compute.service && systemctl start openstack-ceilometer-compute.service && systemctl restart openstack-nova-compute.service
systemctl restart openstack-cinder-api.service openstack-cinder-scheduler.service && systemctl restart openstack-cinder-volume.service && cinder-volume-usage-audit && echo "it is ok,no problem"

function fn_create_aodh_database(){
mysql -e "CREATE DATABASE aodh;" && mysql -e "GRANT ALL PRIVILEGES ON aodh.* TO 'aodh'@'controller' IDENTIFIED BY 'AODH_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON aodh.* TO 'aodh'@'%' IDENTIFIED BY 'AODH_DBPASS';"
}
netstat -luntp | grep 3306 > /dev/null
if [ $? -eq 0 ]
then
	exit
else
	echo "check the mysql is running or die?"
	fn_create_aodh_database
fi

source /root/admin-openrc.sh 
USER_AODH=`openstack user list | grep aodh | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_AODH}x = aodhx ]
then
	echo "openstack user had created  aodh"
else
	openstack user create aodh --password aodh --domain default
	echo "openstack user create aodh --password aodh --domain default"
	openstack role add --project service --user aodh admin
	echo "openstack role add --project service --user aodh admin"
fi

SERVICE_AODH=`openstack service list | grep aodh | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${SERVICE_AODH}x = aodhx ]
then
	echo "openstack service  created  aodh"
else
	openstack service create --name aodh --description "Telemetry" alarming
    echo "create  aodh service"
fi

ENDPOINT_AODH=`openstack endpoint list | grep aodh | awk -F "|" '{print$4}' | awk '{if($1=="aodh"){print $1,$2,$3;exit}}'`
if [ ${ENDPOINT_AODH}x = aodhx ]
then
	echo "openstack endpoint create aodh."
else
	 openstack endpoint create --region RegionOne alarming public http://controller:8042 && openstack endpoint create --region RegionOne alarming internal http://controller:8042 && openstack endpoint create --region RegionOne alarming admin http://controller:8042
	echo "create aodh endpoint"
fi

yum install openstack-aodh-api openstack-aodh-evaluator openstack-aodh-notifier openstack-aodh-listener openstack-aodh-expirer python-ceilometerclient
[ -f /etc/aodh/aodh.conf.bak ] || mv /etc/aodh/aodh.conf /etc/aodh/aodh.conf.bak
cp -a $PWD/lib/aodh.conf /etc/aodh/aodh.conf && systemctl enable openstack-aodh-api.service openstack-aodh-evaluator.service openstack-aodh-notifier.service openstack-aodh-listener.service && systemctl start openstack-aodh-api.service openstack-aodh-evaluator.service openstack-aodh-notifier.service openstack-aodh-listener.service

SERVICE_STATUS=`ceilometer meter-list | grep image | awk -F "|" '{print $4}' | grep -v B`
if [ -z ${SERVICE_STATUS} ]
then 
	systemctl restart openstack-aodh-api.service openstack-aodh-evaluator.service openstack-aodh-notifier.service openstack-aodh-listener.service
	echo "check the aodh service is running or error?"
fi
 
IMAGE_ID=$(glance image-list | grep 'cirros' | awk '{ print $2 }') &&  glance image-download $IMAGE_ID > /tmp/cirros.img
echo "IMAGE_ID=$(glance image-list | grep 'cirros' | awk '{ print $2 }') &&  glance image-download $IMAGE_ID > /tmp/cirros.img"

echo "checking the ceilometer statistics..."
ceilometer statistics -m image.download -p 60 |grep 60| awk 'NR==1' | awk -F "|" '{print $2}'` && rm /tmp/cirros.img || echo "please input commond 'ceilometer meter-list' when the output had image.download ,it is ok . or hadn't ,please check last step. "

echo -e "\033[32m ################################# \033[0m"
echo -e "\033[32m ##   install graph sucessed.##### \033[0m"
echo -e "\033[32m ################################# \033[0m"
echo "graph" >> /var/log/install_log
