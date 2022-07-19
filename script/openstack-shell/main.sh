#!/bin/bash
function fn_install_openstack(){
cat <<EOF
0)config Basic environment.
1)install mariadb,nosql,redis,memcache
2)install keystone.
3)install glance.
4)install nova.
5)install cinder.
6)install neutron.
7)install graph with VM.
8)install dashboard.
9)quit
EOF

read -p "please input one number :" install_number
expr ${install_number}+0 >/dev/null
if[ $? -eq 0 ]
then
	echo "input is number."
else
	echo "please input one number [0-3]"
	echo "input is string."
	fn_install_openstack
fi	
if [ -z ${install_number} ]
then
	echo "please input one right number[0-3]"
	fn_install_openstack
elif [ ${install_number} -eq 0 ]
then
	yum clean all && yum install net-tools
	/bin/bash $PWD/etc/presystem.sh
	echo "/bin/bash $PWD/etc/presystem.sh."
	fn_install_openstack
elif [ ${install_number} -eq 1]
then
	/bin/bash $PWD/etc/install_db.sh
	echo "/bin/bash $PWD/etc/install_db.sh."
	fn_install_openstack
elif [ ${install_number} -eq 2]
then
     /bin/bash $PWD/etc/config-keystone.sh
     echo "/bin/bash $PWD/etc/config-keystone.sh."
     fn_install_openstack
elif [ ${install_number} -eq 3]
then
	/bin/bash $PWD/etc/install_glance.sh
	echo "/bin/bash $PWD/etc/install_glance.sh."
	fn_install_openstack
elif [ ${install_number} -eq 4]
then
	/bin/bash $PWD/etc/install_nova.sh
	echo "/bin/bash $PWD/etc/install_nova.sh"
	fn_install_openstack
elif [ ${install_number} -eq 5] 
then
	/bin/bash $PWD/etc/install_cinder.sh
	echo "/bin/bash $PWD/etc/install_cinder.sh"
	fn_install_openstack
elif [ ${install_number} -eq 6] 
then
	fn_install_neutron
	fn_install_openstack
elif [ ${install_number} -eq 7 ]
then
	/bin/bash $PWD/etc/install_graph.sh
	echo "/bin/bash $PWD/etc/install_graph.sh"
	fn_install_openstack
elif [ ${install_number} -eq 8 ]
then
	/bin/bash $PWD/etc/install_dashboard.sh
	echo "/bin/bash $PWD/etc/install_dashboard.sh"
	fn_install_openstack
elif [ ${install_number} -eq 9 ]
then
	echo "exit install."
    exit
else
	echo "please input one right number[0-3]"
	fn_install_openstack
fi
} 

function fn_install_neutron(){
cat << EOF
1) install neutron for one net
2) install neutron for two net
0) quit
EOF
read -p "please input one number for install :" install_number
expr ${install_number}+0 >/dev/null
if [ $? -eq 0 ]
then
	log_info "input is number."
else
	echo "please input one right number[0-3]"
	echo  "input is string."
	fn_install_neutron
fi	
if  [ -z ${install_number}  ]
then 
    echo "please input one right number[0-3]"
	fn_install_neutron
elif [ ${install_number}  -eq 1 ]
then
	/bin/bash $PWD/etc/install_neutron_one.sh
	echo "/bin/bash $PWD/etc/install_neutron_one.sh"
	fn_install_neutron
elif [ ${install_number}  -eq 2 ]
then
	/bin/bash $PWD/etc/install_neutron_two.sh
	echo "/bin/bash $PWD/etc/install_neutron_two.sh"
	fn_install_neutron
elif  [ ${install_number}  -eq 0 ]
then 
	echo "exit intall."
	fn_install_openstack
else 
     echo "please input one right number[0-3]"
	 fn_install_neutron
fi
}
