#!/bin/bash
NAMEHOST=$HOSTNAME
line=`wc -l  /var/log/install_log | awk '{print$1}'`
if [ $line -eq 6 ]
then
	echo "glance had installed."
else
	echo -e "\033[41;37m you should install glance first. \033[0m"
	exit
fi

cat /var/log/install_log | grep glance
if [ $? -eq 0 ]
then
	echo "you had install glance ."
fi

cat /var/log/install_log | grep nova
if [ $? -eq 0 ]
then
	echo "you had install nova ."
	exit
fi

function fn_create_nova_database(){
mysql -e "CREATE DATABASE nova_api;CREATE DATABASE nova;" && mysql -e "GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'controller' IDENTIFIED BY 'NOVA_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'controller' IDENTIFIED BY 'NOVA_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';"
echo "create nova database"
}
netstat -luntp | grep 3306 > /dev/null
if [ $? -eq 0 ]
then
	exit
else
	echo "check the mysql is running or die?"
	fn_create_nova_database
fi

source /root/admin-openrc.sh 
USER_NOVA=`openstack user list | grep nova | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_NOVA}x = novax ]
then
	echo "openstack user had created  nova"
else
	openstack user create nova --password nova --domain default
	echo "openstack user create nova --password nova --domain default"
	openstack role add --project service --user nova admin
	echo "openstack role add --project service --user nova admin"
fi

SERVICE_NOVA=`openstack service list | grep nova | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [  ${SERVICE_NOVA}x = novax ]
then 
	echo "openstack service create nova."
else
	openstack service create --name nova --description "OpenStack Compute" compute
	echo "create nova service"
fi

ENDPOINT_NOVA=`openstack endpoint list | grep nova | awk -F "|" '{print$4}' | awk '{if($1=="nova"){print $1,$2,$3;exit}}'`
if [ ${ENDPOINT_NOVA}x = novax ]
then
	echo "openstack endpoint create nova."
else
    openstack endpoint create --region RegionOne compute public http://$HOSTNAME:8774/v2.1/%\(tenant_id\)s && openstack endpoint create --region RegionOne compute internal http://$HOSTNAME:8774/v2.1/%\(tenant_id\)s && openstack endpoint create --region RegionOne compute admin http://$HOSTNAME:8774/v2.1/%\(tenant_id\)s
    echo "create nova endpoint  "
fi

yum clean all && yum install openstack-nova-api openstack-nova-conductor openstack-nova-console openstack-nova-novncproxy openstack-nova-scheduler
[ -f /etc/nova/nova.conf.bak ] || mv /etc/nova/nova.conf /etc/nova/nova.conf.bak
cp $PWD/lib/nova.conf /etc/nova/nova.conf

su -s /bin/sh -c "nova-manage api_db sync" nova && su -s /bin/sh -c "nova-manage db sync" nova
echo "sync db nova" 
systemctl enable openstack-nova-api.service  openstack-nova-consoleauth.service openstack-nova-scheduler.service  openstack-nova-conductor.service openstack-nova-novncproxy.service
echo "Start the Compute services and configure them to start when the system boots:"
systemctl start openstack-nova-api.service  openstack-nova-consoleauth.service openstack-nova-scheduler.service  openstack-nova-conductor.service openstack-nova-novncproxy.service
echo "is doing restart service ..."

yum clean all &&  yum install openstack-nova-compute 
[ -f /etc/nova/nova.conf ] || cp  -a $PWD/lib/nova.conf

HWRDWARE=`egrep -c '(vmx|svm)' /proc/cpuinfo`
if [ ${HWRDWARE} -eq 0 ]
then
   openstack-config --set  /etc/nova/nova.conf libvirt virt_type  qemu 
   echo "auto use  QEMU instead of KVM. "
else
	openstack-config --set  /etc/nova/nova.conf libvirt virt_type  kvm
    exit
fi

systemctl enable libvirtd.service openstack-nova-compute.service && systemctl start libvirtd.service openstack-nova-compute.service
echo "Start the Compute service including its dependencies and configure them to start automatically when the system boots ...."

source /root/admin-openrc.sh
openstack compute service list
NOVA_STATUS=`nova service-list | awk -F "|" '{print$7}' | grep -v "State" | grep -v "^$" | awk -F " " '{print $1}' | awk 'NR==1' | grep down`
if [ -z ${NOVA_STATUS} ]
then
	echo "nova status is running"
	echo "nova" >> /var/log/install_log
else
	echo "nova status is died"
	exit
fi

NOVA_IMAGE_STATUS=`nova image-list | grep cirros | awk -F "|" '{print $4}'`
if [ ${NOVA_IMAGE_STATUS} = ACTIVE ]
then
	echo -e "\033[32m nova image status is ok \033[0m"
else
	echo "nova image status is error."
	exit
fi

echo "wait to restart nova service ... "
systemctl start openstack-nova-api.service  openstack-nova-consoleauth.service openstack-nova-scheduler.service  openstack-nova-conductor.service openstack-nova-novncproxy.service libvirtd.service openstack-nova-compute.service
echo -e "\033[32m ################################################ \033[0m"
echo -e "\033[32m ###         install nova sucessed           #### \033[0m"
echo -e "\033[32m ################################################ \033[0m"
