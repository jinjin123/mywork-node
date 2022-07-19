#!/bin/bash
NAMEHOST=$HOSTNAME
line=` wc -l /var/log/install_log | awk '{print$1}'`
if [ $line -eq 5 ]
then
	echo "keystone had installed."
else
	echo -e "\033[41;37m you should install keystone first. \033[0m"
	exit
fi

cat /var/log/install_log | grep glance
if [ $? -eq 0 ]
then
	echo "you had install glance ."
	exit
fi

function fn_create_glance_database(){
mysql -e "CREATE DATABASE glance;" &&  mysql -e "GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'controller' IDENTIFIED BY 'GLANCE_DBPASS';"  && mysql -e "GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'GLANCE_DBPASS';"
}
netstat -luntp | grep 3306 > /dev/null
if [ $? -eq 0 ]
then
	exit
else
	echo "check the mysql is running or die?"
	fn_create_glance_database
fi

source /root/admin-openrc.sh 
USER_GLANCE=`openstack user list | grep glance | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_GLANCE}x = glancex ]
then
	log_info "openstack user had created  glance"
else
	openstack user create glance --password glance --domain default
	echo "openstack user create glance --password glance --domain default"
	openstack role add --project service --user glance admin
	echo "openstack role add --project service --user glance admin"
fi

SERVICE_IMAGE=`openstack service list | grep glance | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [  ${SERVICE_IMAGE}x = glancex ]
then 
	echo  "openstack service create glance."
else
	openstack service create --name glance --description "OpenStack Image service" image
	echo "create glance service"
fi

ENDPOINT_GLANCE=`openstack endpoint list | grep glance | awk -F "|" '{print$4}' | awk '{if($1=="glance"){print $1,$2,$3;exit}}'`
if [ ${ENDPOINT_GLANCE}x = glancex ]
then
	echo "openstack endpoint create glance."
else
	openstack endpoint create --region RegionOne image public http://$HOSTNAME:9292 && openstack endpoint create --region RegionOne image internal http://$HOSTNAME:9292 && openstack endpoint create --region RegionOne image admin http://$HOSTNAME:9292
	echo "create glance endpoint"
fi

yum clean all &&  yum install openstack-glance
echo "yum clean all && yum install openstack-glance"

[ -f /etc/glance/glance-api.conf_bak ] || mv /etc/glance/glance-api.conf /etc/glance/glance-api.conf_bak
[ -f /etc/glance/glance-registry.conf_bak ] || mv /etc/glance/glance-registry.conf /etc/glance/glance-registry.conf_bak
cp $PWD/lib/glance-api.conf /etc/glance/glance-api.conf  && cp $PWD/lib/glance-registry.conf /etc/glance/glance-registry.conf

su -s /bin/sh -c "glance-manage db_sync" glance
echo "su -s /bin/sh -c "glance-manage db_sync" glance"

systemctl enable openstack-glance-api.service openstack-glance-registry.service && systemctl start openstack-glance-api.service openstack-glance-registry.service
echo "systemctl enable openstack-glance-api.service openstack-glance-registry.service && systemctl start openstack-glance-api.service openstack-glance-registry.service"

function fn_create_image(){
source /root/admin-openrc
cp -a $PWD/lib/cirros-0.3.4-x86_64-disk.img /tmp/ && \
openstack image create "cirros" --file /tmp/cirros-0.3.4-x86_64-disk.img --disk-format qcow2 --container-format bare --public
echo "create image"
glance image list
echo "glance image list"
}

echo -e "\033[32m ################################################ \033[0m"
echo -e "\033[32m ###        install glance sucessed         #### \033[0m"
echo -e "\033[32m ################################################ \033[0m"
echo "glance" >> /var/log/install_log
