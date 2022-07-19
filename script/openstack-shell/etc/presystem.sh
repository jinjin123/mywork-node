#!/bin/bash
function  fn_log(){
OS_VERSION=` cat /etc/centos-release | awk -F " " '{print $4}' | awk -F "." '{print $1}'`
if [ ${OS_VERSION} -ne 7 ]
then
    echo -e "\033[41;37m you should install OS system by CentOS-7.2.1511-x86_64-DVD.iso. \033[0m"
	exit 1
fi
}

FIRST_ETH=`ip addr | grep ^2: |awk -F ":" '{print$2}'`
FIRST_ETH_IP=`ifconfig ${FIRST_ETH}  | grep netmask | awk -F " " '{print$2}'`

if [ ${FIRST_ETH} != "eth0" ]
then 
	echo -e "\033[41;37m you should rename network_name. \033[0m "
elif [ -z ${FIRST_ETH_IP} ]
then 
	echo -e "\033[41;37m you should config the first network by the manager ip. \033[0m"
else 
	exit 1
fi

read -p "pelease hostname for system [default:controller]:" install_number
if [ -z ${install_number} ]
then
 	echo "controller" > $PWD/lib/hostname
else
	echo "${install_number}" > $PWD/lib/hostname
fi	

NAMEHOST=`cat $PWD/lib/hostname`
FIRST_ETH_IP=`ifconfig ${FIRST_ETH}  | grep netmask | awk -F " " '{print$2}'`

#set hostname
function fn_set_hostname(){
hostnamectl set-hostname ${NAMEHOST}
echo "${FIRST_ETH_IP} ${NAMEHOST}" >> /etc/hosts
echo "modify hosts"
}

HOSTS_STATUS=`cat /etc/hosts | grep $FIRST_ETH_IP`
if [ -z "${HOSTS_STATUS}" ]
then
	fn_set_hostname
else
	echo "hostname had set"
fi

#stop firewall
systemctl stop	firewalld.service
echo "stop firewalld"
systemctl disable firewalld.service
echo "systemctl disable firewalld.service"

#disabled selinux
SELINUX_STATUS=`cat /etc/sysconfig/selinux | grep -v "#" | grep disabled | cut -c 9-`
if [ ${SELINUX_STATUS} = "enforcing" ]
then
   sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux 
   echo "selinux is disable "
else
	exit 
fi

ping -c 4 ${NAMEHOST}
echo "ping -c 4 ${NAMEHOST}"

#install ntp
yum clean all && yum install chrony
echo "yum clean all && yum install chrony"
#modify /etc/chrony.conf
cp -a /etc/chrony.conf /etc/chrony.conf.bak
sed -i '3,5 d' /etc/chrony.conf && sed -i 's/3.centos.pool.ntp.org/controller/g' /etc/chrony.conf && sed -i 's/#allow 192.168\/16/allow 192.168.1.0\/24/g'  /etc/chrony.conf
echo "allow 192.168.1.0/24 in chrony.conf"
systemctl enable chronyd.service &&  systemctl start chronyd.service && chronyc sources

function fn_yum_openstack(){
cd /etc/yum.repos.d && mv CentOS-Base.repo CentOS-Base.repo.bk && wget http://mirrors.163.com/.help/CentOS7-Base-163.repo 
echo "|cd /etc/yum.repos.d && mv CentOS-Base.repo CentOS-Base.repo.bk && wget http://mirrors.163.com/.help/CentOS7-Base-163.repo |"
echo "clean all && yum install centos-release-openstack-mitaka && yum upgrade && yum install python-openstackclient"
yum clean all && yum install centos-release-openstack-mitaka && yum upgrade  && yum install python-openstackclient
} 
echo -e "\033[32m ################################# \033[0m"
echo -e "\033[32m ## basic envionment sucessed.#### \033[0m"
echo -e "\033[32m ################################# \033[0m"
echo -e "\033[41;37m begin to reboot system to enforce kernel \033[0m"

sleep 2

reboot
