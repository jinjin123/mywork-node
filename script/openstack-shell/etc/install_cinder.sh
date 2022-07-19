#!/bin/bash
NAMEHOST=$HOSTNAME
line=`wc -l /var/log/install_log | awk '{print$1}'`
if [ $line -eq 7 ]
then
	echo "nova had installed."
else
	echo -e "\033[41;37m you should install nova first. \033[0m"
	exit
fi

cat /var/log/install_log | grep nova
if [ $? -eq 0 ]
then
	echo "you had install nova ."
fi

cat /var/log/install_log | grep cinder
if [ $? -eq 0 ]
then
	echo "you had install cinder ."
	exit
fi

#create cinder database
function fn_create_cinder_database(){
mysql -e "CREATE DATABASE cinder;" && mysql -e "GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'controller' IDENTIFIED BY 'CINDER_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'CINDER_DBPASS';"
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
USER_CINDER=`openstack user list | grep cinder | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_CINDER}x = cinderx ]
then
	echo "openstack user had created  cinder"
else
	openstack user create cinder --password cinder --domain default
	echo "openstack user create cinder --password cinder --domain default"
	openstack role add --project service --user cinder admin
	echo "openstack role add --project service --user cinder admin"
fi

SERVICE_CINDER=`openstack service list | grep cinder | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [  ${SERVICE_CINDER}x = cinderx ]
then 
	echo "openstack service create cinder."
else
	openstack service create --name cinder --description "OpenStack Block Storage" volume &&  openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
	echo "create cinder service"
fi

ENDPOINT_CINDER=`openstack endpoint list | grep cinder | awk -F "|" '{print$4}' | awk '{if($1=="cinder"){print $1,$2,$3;exit}}'`
if [ ${ENDPOINT_CINDER}x = cinderx ]
then
	echo "openstack endpoint create cinder."
else
	openstack endpoint create --region RegionOne volume public http://$HOSTNAME:8776/v1/%\(tenant_id\)s && openstack endpoint create --region RegionOne \
    volume internal http://$HOSTNAME:8776/v1/%\(tenant_id\)s && openstack endpoint create --region RegionOne volume admin http://$HOSTNAME:8776/v1/%\(tenant_id\)s && openstack endpoint create --region RegionOne \
    volumev2 public http://$HOSTNAME:8776/v2/%\(tenant_id\)s && openstack endpoint create --region RegionOne volumev2 internal http://$HOSTNAME:8776/v2/%\(tenant_id\)s && openstack endpoint create --region RegionOne volumev2 admin http://$HOSTNAME:8776/v2/%\(tenant_id\)s
	echo "openstack endpoint create cinder "    
fi

yum clean all && yum install openstack-cinder  targetcli
[ -f /etc/cinder/cinder.conf.bak ] || mv /etc/cinder/cinder.conf  /etc/cinder/cinder.conf.bak
cp -a $PWD/lib/cinder.conf /etc/cinder/cinder.conf
FIRST_ETH=`ip addr | grep ^2: |awk -F ":" '{print$2}'`
FIRST_ETH_IP=`ifconfig ${FIRST_ETH}  | grep netmask | awk -F " " '{print$2}'`
sed -i "s/my_ip = 192.168.1.101/my_ip = ${FIRST_ETH_IP}/g" /etc/cinder/cinder.conf
su -s /bin/sh -c "cinder-manage db sync" cinder
echo "sync cinder db"

echo "restart nova-api and cinder service , wait for minutes..."
systemctl restart openstack-nova-api.service && systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service && systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service

yum install lvm2  
[ -f /etc/lvm/lvm.conf.bak ] || mv /etc/lvm/lvm.conf /etc/lvm/lvm.conf.bak
cp -a $PWD/lib/lvm.conf /etc/lvm/lvm.conf
fn_filter_disk
function fn_filter_disk(){
cat <<EOF
0) add / partting for cinder,you must open other terminal
1) not add / partting for cinder,you must open other terminal
2) next step
EOF
read -p "please input number"  install_number
expr ${install_number}+0 >/dev/null
if[ $? -eq 0 ]
then
	echo "input is number."
else
	echo "please input one number [0-2]"
	echo "input is string."
	fn_filter_disk
fi	 
if [ -z ${install_number} ]
then
	echo "please input one right number[0-2]"
	fn_filter_disk
elif [  ${install_number} -eq 0 ]
then
	echo "let's edit /etc/lvm/lvm.conf,find the example 'devices { filter = [ "a/sda/", "r/.*/" ]}',and add other disk in it"
	fn_filter_disk
elif [ ${install_number} -eq 1 ]
then
	echo "let's edit /etc/lvm/lvm.conf,find the example 'devices { filter = [ "a/sdb/", "r/.*/" ]}',if you / is sda not add sda in "
	fn_filter_disk
elif [ ${install_number} -eq 2 ]
then
	echo "let's go to the next step."
	exit
else
	fn_filter_disk
fi
}

systemctl enable lvm2-lvmetad.service && systemctl start lvm2-lvmetad.service
echo "start lvm service..."

CINDER_DISK=`cat  $PWD/lib/cinder_disk | grep ^CINDER_DISK | awk -F "=" '{print$2}'`

function fn_create_cinder_volumes(){
if [ -z ${CINDER_DISK} ]
then
	echo "there is not disk for cinder."
else
	pvcreate ${CINDER_DISK}  && vgcreate cinder-volumes ${CINDER_DISK}
	echo "Create the LVM physical volume /dev/sdb: and Create the LVM volume group cinder-volumes:"
fi
}

VOLUNE_NAME=`vgs | grep cinder-volumes | awk -F " " '{print$1}'`
if [ ${VOLUNE_NAME}x = cinder-volumesx ]
then
	log_info "cinder-volumes had created."
else
	fn_create_cinder_volumes
fi

systemctl enable openstack-cinder-volume.service target.service && systemctl start openstack-cinder-volume.service target.service

source /root/admin-openrc.sh && cinder service-list

sleep 5
CINDER_STATUS=`source /root/admin-openrc.sh && cinder service-list |grep -v "backup"| awk -F "|" '{print$6}' | grep -v State  | grep -v ^$ | grep -i down`
if [  -z  ${CINDER_STATUS} ]
then
	echo -e "\033[32m cinder status is ok \033[0m"
else
   	echo -e "\033[41;37m cinder status is down. \033[0m"
	exit
fi

echo -e "\033[32m ################################################ \033[0m"
echo -e "\033[32m ###         install cinder sucessed         #### \033[0m"
echo -e "\033[32m ################################################ \033[0m"
echo "cinder" >> /var/log/install_log
