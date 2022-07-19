#!/bin/bash
NAMEHOST=$HOSTNAME
line=`wc -l /var/log/install_log | awk '{print$1}'`
if [ $line -eq 8 ]
then
	echo "cinder had installed."
else
	echo -e "\033[41;37m you should install cinder first. \033[0m"
	exit
fi
cat /var/log/install_log | grep neutron
if [ $? -eq 0 ]
then
	echo "you had install nuetron ."
	exit
fi
source $PWD/lib/neutron_net_config
function fn_create_neutron_database(){
mysql -e "CREATE DATABASE neutron;" && mysql -e "GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'controller' IDENTIFIED BY 'NEUTRON_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'NEUTRON_DBPASS';"
}
netstat -luntp | grep 3306 > /dev/null
if [ $? -eq 0 ]
then
	exit
else
	echo "check the mysql is running or die?"
	fn_create_neutron_database
fi

source /root/admin-openrc.sh 
USER_NEUTRON=`openstack user list | grep neutron | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_NEUTRON}x = neutronx ]
then
	echo "openstack user had created  neutron"
else
	openstack user create neutron --password neutron --domain default
	echo "openstack user create neutron --password neutron --domain default"
	openstack role add --project service --user neutron admin
	echo "openstack role add --project service --user neutron admin"
fi

SERVICE_NEUTRON=`openstack service list | grep neutron | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${SERVICE_NEUTRON}x = neutronx ]
then
	echo "openstack service  created  neutron"
else
	openstack service create --name neutron --description "OpenStack Networking" network 
    echo "create neutron service"
fi

ENDPOINT_NEUTRON=`openstack endpoint list | grep neutron | awk -F "|" '{print$4}' | awk '{if($1=="neutron"){print $1,$2,$3;exit}}'`
if [ ${ENDPOINT_NEUTRON}x = neutronx ]
then
	echo "openstack endpoint create neutron."
else
	openstack endpoint create --region RegionOne network public http://$HOSTNAME:9696 && openstack endpoint create --region RegionOne network internal http://$HOSTNAME:9696 && openstack endpoint create --region RegionOne network admin http://$HOSTNAME:9696
	echo "create neutron endpoint"
fi

yum clean all && yum install openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge ebtables
[ -f /etc/neutron/neutron.conf.bak ] || mv /etc/neutron/neutron.conf /etc/neutron/neutron.bak
cp $PWD/lib/neutron.conf /etc/neutron/neutron.conf
[ -f /etc/neutron/plugins/ml2/ml2_conf.ini.bak ] || mv /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugins/ml2/ml2_conf.ini.bak
cp $PWD/lib/ml2_conf.ini /etc/neutron/plugins/ml2/ml2_conf.ini
[ -f /etc/neutron/plugins/ml2/linuxbridge_agent.ini.bak ] || mv /etc/neutron/plugins/ml2/linuxbridge_agent.ini /etc/neutron/plugins/ml2/linuxbridge_agent.ini.bak
cp $PWD/lib/linuxbridge_agent.ini /etc/neutron/plugins/ml2/linuxbridge_agent.ini
function fn_input_vxlan_address(){
cat << EOF
0)private-net need to set the ip_address,please set the ip_address with eth1 or eth2 ,excepte eth0.Edit the /etc/neutron/plugins/ml2/linuxbridge_agent.ini,[vxlan] local_ip = eth1_ip_address
1)anything is do it ,i want  to next step.
EOF
}
fn_input_vxlan_address
read -p "please input number:" install_number
if [ $? -eq 0 ]
then
	log_info "input is number."
else
	echo "please input one right number[0-3]"
	echo  "input is string."
	fn_input_vxlan_address
fi	
if  [ -z ${install_number}  ]
then 
    echo "please input one right number[0-1]"
    fn_input_vxlan_address
elif [ ${install_number}  -eq 0 ]
then
	echo "let's go to the edit linuxbridge_agent.ini"
	fn_input_vxlan_address
elif [ ${install_number}  -eq 1 ]
then
	echo "ok,let's next step."
	exit
fi

[-f /etc/neutron/l3_agent.ini.bak ] || mv /etc/neutron/l3_agent.ini  /etc/neutron/l3_agent.ini.bak
cp $PWD/lib/l3_agent.ini /etc/neutron/l3_agent.ini
[-f /etc/neutron/dhcp_agent.ini.bak ] || mv /etc/neutron/dhcp_agent.ini /etc/neutron/dhcp_agent.ini.bak
cp $PWD/lib/dhcp_agent.ini /etc/neutron/dhcp_agent.ini
[ -f /etc/neutron/metadata_agent.ini.bak ] || mv /etc/neutron/metadata_agent.ini /etc/neutron/metadata_agent.ini.bak
cp $PWD/lib/metadata_agent.ini /etc/neutron/metadata_agent.ini
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini

ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
function fn_check_service(){
if [ $? -eq 0 ]
then
	echo "anything is ok"
else
	echo "please check the error about network"
fi
}

echo "restart nova-api service wait for minutes..."
systemctl restart openstack-nova-api.service

echo "Start the Networking services and configure them to start when the system boots.For both networking options:" 
systemctl enable neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service neutron-l3-agent.service

echo "start about neutron service"
systemctl start neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service neutron-l3-agent.service

echo "install nova-compute-network_agent neutron package "
yum install openstack-neutron-linuxbridge ebtables ipset
echo "restart neutron service"
systemctl restart openstack-nova-compute.service neutron-linuxbridge-agent.service
fn_check_service

source /root/admin-openrc.sh 
neutron agent-list | grep True 
NEUTRON_STATUS=`neutron agent-list | awk -F "|" '{print $6}' | grep -v "alive" | grep -v "^$" | grep -i xxx`
if [ -z ${NEUTRON_STATUS} ]
then
	echo "neturn network is OK"
else
	echo "check about neutron service have already running"
fi

PUBLIC=`neutron net-list | grep public | awk -F " " '{print$4}'`
if [ ${PUBLIC}x = publicx ]
then
	echo "public-net had created"
else
	neutron net-create --shared --provider:physical_network public --provider:network_type flat public
fi
PUBLIC_SUB=`neutron subnet-list | grep public | awk -F " " '{print$4}'`
if [ ${PUBLIC_SUB}x = publicx ]
then
	echo "public-subnet had created"
else
	neutron subnet-create --name public --allocation-pool start=${PB_START},end=${PB_END} --dns-nameserver ${PB_DNS} --gateway ${PB_GW} public ${PB_NET}
	echo "public-subnet had created"
fi

PRIVATE=`neutron subnet-list | grep private | awk -F " " '{print$4}'`
if [ ${PRIVATE}x = privatex ]
then
	echo "private-net had created"
else
 	neutron net-create private
 	echo "private-net had created"
fi

PRIVATE_SUB=`neutron subnet-list | grep private | awk -F " " '{print$4}'`
if [ ${PRIVATE_SUB}x = privatex]
then
	echo "private-subnet had created"
else
	neutron subnet-create --name private --dns-nameserver ${PA_DNS} --gateway ${PA_GW} private ${PA_NET}
	echo "private-subnet had created"
fi

ROUTE_ID=`neutron router-list | grep router | awk -F " " '{print$4}'`
if [ ${ROUTE_ID}x  = routerx ]
then
	echo  "demo-router had create."
else
    neutron router-create router
    echo "create router router"
fi

source /root/demo-openrc.sh 
ROUTR_PORT=`neutron router-port-list  demo-router |grep  ip_address  |awk -F "\"" '{print$6}' | awk 'NR==1'`
if [  ${ROUTR_PORT}x  = ip_addressx ]
then 
	echo  "subnet had add to router."
else
	#give the private-sub link internet maybe
	neutron router-interface-add router private && neutron router-gateway-set router
	echo "give the private-sub link internet maybe" 
fi

ping -c 4 ${PB_START} > /dev/null
fn_check_service

source /root/demo-openrc.sh
echo "\n" |  ssh-keygen -q -N ""
KEYPAIR=`nova keypair-list | grep  mykey | awk -F " " '{print $2}'`
if [  ${KEYPAIR}x = mykeyx ]
then
	 echo "keypair had added."
else
	openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey
	echo "keypair had added"
fi

openstack security group rule create --proto icmp default
SECRULE=`nova secgroup-list-rules  default | grep 22 | awk -F " " '{print $6}'`
if [ x${SECRULE} = x22 ]
then 
	echo "port 22 and icmp had add to secgroup."
else
	openstack security group rule create --proto tcp --dst-port 22 default
	echo "port 22 and icmp had add to secgroup."
fi
echo -e "\033[32m ################################# \033[0m"
echo -e "\033[32m ##   install neutron sucessed.#### \033[0m"
echo -e "\033[32m ################################# \033[0m"
echo "neutron" >> /var/log/install_log
