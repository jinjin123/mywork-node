#!/bin/bash
rpm -qa | grep  -E "python-openstackclient|centos-release-openstack-mitaka"
if[ $? -eq 0 ]
then
	echo "basic env have  installed."
else
	echo -e "\033[41;37m you should config basic env first. \033[0m"
fi
rpm -qa | grep  -E "mariadb-10.1.12-4.el7.x86_64|mariadb-server-10.1.12-4.el7.x86_64|python2-PyMySQL-0.6.7-2.el7.noarch"
if[ $? -eq 0 ]
then
	echo -e "\033[32m you had install mariadb \033[0m"
	exit
fi

FIRST_ETH=`ip addr | grep ^2: |awk -F ":" '{print$2}'`
FIRST_ETH_IP=`ifconfig ${FIRST_ETH}  | grep netmask | awk -F " " '{print$2}'`

function fn_install_mariadb(){
yum clean all &&  yum install mariadb mariadb-server python2-PyMySQL  -y
echo "yum clean all &&  yum install mariadb mariadb-server python2-PyMySQL  -y"
cat > /etc/my.cnf.d/openstack.cnf <<EOF
[mysqld]
default-storage-engine = innodb
innodb_file_per_table
collation-server = utf8_general_ci
character-set-server = utf8
max_connections = 1000
thread_cache_size = 16
skip-name-resolve
query_cache_type = 1
query_cache_limit = 256K
query_cache_min_res_unit = 2k
query_cache_size = 80M
tmp_table_size= 64M
max_heap_table_size= 64M
wait_timeout=60
EOF
echo "bind-address = ${FIRST_ETH_IP}" >> /etc/my.cnf.d/openstack.cnf
#start mariadb
systemctl enable mariadb.service &&  systemctl start mariadb.service 
echo "have no set passwd"
}
MARIADB_STATUS=`systemctl status mariadb | grep Active | awk -F "("  '{print$2}' | awk -F ")"  '{print$1}'`
if [ "${MARIADB_STATUS}" = running ]
then
	echo "mariadb had install."
	echo "mariadb" >> /var/log/install_log
else
	fn_install_mariadb
fi

function fn_install_mongodb(){
ip=`cat /etc/mongod.conf | grep bind_ip`
small=`cat /etc/mongod.conf | grep smallfiles`
MONGODB_STATUS=`systemctl status mongod | grep Active | awk -F "("  '{print$2}' | awk -F ")"  '{print$1}'` 
yum clean all && yum install mongodb-server mongodb -y
echo "yum clean all && yum install mongodb-server mongodb -y"
if [ -f /etc/mongod.conf ] 
then
	sed -i "s#bind_ip = ${ip}#bind_ip = ${FIRST_ETH_IP}#g" /etc/mongod.conf && sed -i "s/#smallfiles = true/smallfiles = true/g" /etc/mongod.conf
	echo "mongodb" >> /var/log/install_log
else
	fn_install_mongodb
fi
}

function fn_install_rabbit(){
yum clean all && yum install  rabbitmq-server -y
echo "yum clean all && yum install  rabbitmq-server -y"
#start rabbitmq-server.service
systemctl enable rabbitmq-server.service && systemctl start rabbitmq-server.service
echo "systemctl start rabbitmq-server.service"
rabbitmqctl add_user openstack jinjin123
echo "rabbitmqctl add_user openstack jinjin123"
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
echo "rabbitmqctl set_permissions openstack ".*" ".*" ".*""
}
function fn_test_rabbit(){
RABBIT_STATUS=`rabbitmqctl list_users | grep openstack | awk -F " " '{print$1}'`
if [ ${RABBIT_STATUS}x  = openstackx ]
then 
	echo "rabbit had installed."
	echo "rabbit" >> /var/log/install_log
else
	fn_install_rabbit
fi
}
if [ -f /usr/sbin/rabbitmqctl  ]
then
	echo "rabbit had installed."
else
	fn_test_rabbit
fi

function fn_install_memcached(){
yum clean all && yum install  memcached python-memcached
echo "yum clean all && yum install  memcached python-memcached"
systemctl enable memcached.service && systemctl start memcached.service
echo " systemctl enable memcached.service &&systemctl start memcached.service"
}
memcached-tool 127.0.0.1:11211 stats
if [ $? -eq 0 ]
then
	echo "memcached had install"
	echo "memcached" >> /var/log/install_log
else
	fn_install_memcached
fi

echo -e "\033[32m ################################################ \033[0m"
echo -e "\033[32m ###   install mariadb and rabbitmq sucessed.#### \033[0m"
echo -e "\033[32m ###   install mongodb and memcached sucessed.### \033[0m"
echo -e "\033[32m ################################################ \033[0m"
