#!/bin/bash
NAMEHOST=$HOSTNAME
line=` wc -l /var/log/install_log | awk '{print$1}'`
if [ $line -eq 4 ]
then
	echo "db had installed."
else
	echo -e "\033[41;37m you should install mariadb first. \033[0m"
	exit
fi
cat /var/log/install_log | grep keystone
if [ $? -eq 0 ]
then
	echo "you had install keystone ."
	exit
fi

yum clean all &&  yum install openstack-keystone httpd mod_wsgi
function fn_create_keystone_database(){
mysql -e "CREATE DATABASE keystone;" && mysql -e "GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'controller' IDENTIFIED BY 'KEYSTONE_DBPASS';" && mysql -e "GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'KEYSTONE_DBPASS';"
echo "create DATABASE"
}
netstat -luntp | grep 3306 > /dev/null
if [ $? -eq 0 ]
then
	exit
else
	echo "check the mysql is running or die?"
	fn_create_keystone_database
fi

[ -f /etc/keystone/keystone.conf ] || cp -a /etc/keystone/keystone.conf /etc/keystone/keystone.conf.bak
echo "[ -f /etc/keystone/keystone.conf ] || cp -a /etc/keystone/keystone.conf /etc/keystone/keystone.conf.bak"
ADMIN_TOKEN=$(openssl rand -hex 10)
openstack-config --set /etc/keystone/keystone.conf DEFAULT admin_token $ADMIN_TOKEN 
echo "openstack-config --set /etc/keystone/keystone.conf DEFAULT admin_token $ADMIN_TOKEN "

openstack-config --set /etc/keystone/keystone.conf database connection mysql+pymysql://keystone:KEYSTONE_DBPASS@$HOSTNAME/keystone
echo "openstack-config --set /etc/keystone/keystone.conf database connection mysql+pymysql://keystone:KEYSTONE_DBPASS@$HOSTNAME/keystone"

openstack-config --set /etc/keystone/keystone.conf token provider fernet
echo "openstack-config --set /etc/keystone/keystone.conf token provider fernet"

su -s /bin/sh -c "keystone-manage db_sync" keystone
echo " su -s /bin/sh -c "keystone-manage db_sync" keystone"

keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
echo " keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone"

[ -f /etc/httpd/conf/httpd.conf_bak  ] || cp -a /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf_bak
echo "[ -f /etc/httpd/conf/httpd.conf_bak  ] || cp -a /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf_bak"

sed  -i  "s/#ServerName www.example.com:80/ServerName ${HOSTNAME}/" /etc/httpd/conf/httpd.conf
echo  "sed  -i  's/#ServerName www.example.com:80/ServerName $HOSTNAME/' /etc/httpd/conf/httpd.conf"

[ -f /etc/httpd/conf.d/wsgi-keystone.conf ] || cp -a /etc/httpd/conf.d/wsgi-keystone.conf /etc/httpd/conf.d/wsgi-keystone.conf.bak
rm -rf /etc/httpd/conf.d/wsgi-keystone.conf && cp -a $PWD/lib/wsgi-keystone.conf /etc/httpd/conf.d/wsgi-keystone.conf
echo "cp -a $PWD/lib/wsgi-keystone.conf  /etc/httpd/conf.d/wsgi-keystone.conf "

chown keystone:keystone /var/log/keystone/keystone.log
echo "chown keystone:keystone /var/log/keystone/keystone.log"

systemctl enable httpd.service && systemctl start httpd.service
echo "systemctl enable httpd.service && systemctl start httpd.service"

export OS_TOKEN=$ADMIN_TOKEN
export OS_URL=http://$HOSTNAME:35357/v3
export OS_IDENTITY_API_VERSION=3

SERVICE_NAME=`openstack service list | grep keystone | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${SERVICE_NAME}x  = keystonex ]
then 
	echo "openstack service have create"
else
	openstack service create --name keystone --description "OpenStack Identity" identity 
	echo "create OpenStack service"
fi

ENDPOINT_LIST=`openstack endpoint list | grep keystone | awk -F "|" '{print$4}' | awk '{if($1=="keystone"){print $1,$2,$3;exit}}'`
if [  ${ENDPOINT_LIST}x  = keystonex  ]
then
	echo "openstack endpoint had created."
else
	 openstack endpoint create --region RegionOne identity public http://$HOSTNAME:5000/v3 && openstack endpoint create --region RegionOne identity internal http://$HOSTNAME:5000/v3 && openstack endpoint create --region RegionOne identity admin http://$HOSTNAME:35357/v3
	echo "OpenStack endpoint create"
fi

PROJECT_ADMIN=`openstack project list | grep admin | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${PROJECT_ADMIN}x = adminx ]
then
	echo  "openstack project admin create."
else 
	#create default domain and project admin
    openstack domain create --description "Default Domain" default  && openstack project create --domain default --description "Admin Project" admin
    echo "openstack domain create --description "Default Domain" default  && openstack project create --domain default --description "Admin Project" admin"
fi

USER_LIST=`openstack user list | grep admin | awk -F "|" '{print$3}' | awk -F " " '{print $1}'|grep '^a'`
if [ ${USER_LIST}x = adminx ]
then
	echo "openstack user had  created  admin"
else
	#create user admin  and passwd set admin
    openstack user create admin --password admin --domain default
    echo "openstack user create admin --password admin --domain default" 
fi

ROLE_ADMIN=`openstack role list | grep admin | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${ROLE_ADMIN}x = adminx ]
then 
	echo "openstack role had created admin"
else
	openstack role create admin
    echo "openstack role create admin"
    openstack role add --project admin --user admin admin
    echo "openstack role add --project admin --user admin admin"
fi

PROJECT_SERVICE=`openstack project list |grep service | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [  ${PROJECT_SERVICE}x = servicex ]
then
	echo "openstack project had created service. "
else
	openstack project create --domain default --description "Service Project" service
    echo "openstack project create --domain default --description "Service Project" service"
fi

PROJECT_DEMO=`openstack project list |grep demo | awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [  ${PROJECT_DEMO}x = demox ]
then
	echo "openstack project had created demo "
else
	openstack project create --domain default --description "Demo Project" demo
	echo "openstack project create --domain default --description "Demo Project" demo"
fi

USER_DEMO=` openstack user list |grep demo |awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${USER_DEMO}x  =  demox ]
then
	echo "openstack user had created  demo"
else
	openstack user create demo --password demo --domain default
    echo "openstack user create demo --password demo --domain default"
fi


ROLE_LIST=`openstack role list | grep user  |awk -F "|" '{print$3}' | awk -F " " '{print$1}'`
if [ ${ROLE_LIST}x = userx ]
then
     echo "openstack role had  created user."
else
	openstack role create user
	echo "openstack role create user"
	openstack role add --project demo --user demo user
	echo "openstack role add --project demo --user demo user"
fi

mv /etc/keystone/keystone-paste.ini /etc/keystone/keystone-paste.ini.bak && sed -i '54,64 s/admin_token_auth//' /etc/keystone/keystone-paste.ini
unset OS_TOKEN OS_URL
#uses the password for the admin user.
openstack --os-auth-url http://controller:35357/v3   --os-project-domain-name default --os-user-domain-name default   --os-project-name admin --os-username admin --os-auth-type password token issue --os-password admin
echo "openstack --os-auth-url http://controller:35357/v3   --os-project-domain-name default --os-user-domain-name default   --os-project-name admin --os-username admin --os-auth-type password token issue --os-password admin"

#uses the password for the demo user.
openstack --os-auth-url http://controller:35357/v3   --os-project-domain-name default --os-user-domain-name default   --os-project-name demo --os-username demo --os-auth-type password token issue --os-password demo
echo "openstack --os-auth-url http://controller:35357/v3   --os-project-domain-name default --os-user-domain-name default   --os-project-name demo --os-username demo --os-auth-type password token issue --os-password demo
"

[ -f /root/admin-openrc.sh  ] || cp -a $PWD/lib/admin-openrc.sh  /root/admin-openrc.sh 
echo "[ -f /root/admin-openrc.sh  ] || cp -a $PWD/lib/admin-openrc.sh  /root/admin-openrc.sh "

[ -f /root/demo-openrc.sh  ]  || cp -a $PWD/lib/demo-openrc.sh  /root/demo-openrc.sh 
echo "cp -a $PWD/lib/demo-openrc.sh  /root/demo-openrc.sh "
source /root/admin-openrc.sh
openstack token issue
echo "openstack token issue"

echo -e "\033[32m ################################################ \033[0m"
echo -e "\033[32m ###       install keystone sucessed         #### \033[0m"
echo -e "\033[32m ################################################ \033[0m"
echo "keystone" >> /var/log/install_log
