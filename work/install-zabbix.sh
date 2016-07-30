#!/bin/sh
#install the zabbix-agent

clear
echo "========================================================================="
echo "Now begin to install zabbix-agent"
echo "========================================================================="

#get serverip
echo -n "Please enter server ip:"
read serverip

if [ "$(whoami)" != 'root' ]; then
        echo "install need root user"
        exit 1
fi

file1="./zabbix-2.4.4.tar.gz"
if [ ! -f "$file1" ]; then
        echo "Need zabbix-2.4.4.tar.gz"
        exit 1
fi

file2="./zabbix_agentd"
if [ ! -f "$file2" ]; then
        echo "Need zabbix_agentd"
        exit 1
fi

file3="./zabbix_agent.conf"
if [ ! -f "$file3" ]; then
        echo "Need zabbix_agent.conf"
        exit 1
fi

file4="./zabbix_agentd.conf"
if [ ! -f "$file4" ]; then
        echo "Need zabbix_agentd.conf"
        exit 1
fi

echo "Install Depend Package..."
yum makecache
resoult=$?
while((1))
do
        if [ $resoult == 0 ]
        then
                break
        else
                yum clean all
                yum makecache
                resoult=$?
                continue
        fi
done
yum -y install gcc gcc-c++
resoult=$?
while((1))
do
        if [ $resoult == 0 ]
        then
                break
        else
                yum clean packages
                yum -y install gcc gcc-c++
                resoult=$?
                continue
        fi
done

echo "Create user..."
groupadd zabbix
useradd zabbix -g zabbix
echo "tar zabbix-2.4.4.tar.gz"
tar -zxvf ./zabbix-2.4.4.tar.gz

echo "configure..."
cd zabbix-2.4.4
./configure --prefix=/opt/zabbix_agent --enable-agent

echo "make install..."
make install
cd ..

echo "Install service..."
cat >>/etc/services<<EOF
zabbix-agent 10050/tcp Zabbix Agent
zabbix-agent 10050/udp Zabbix Agent
zabbix-trapper 10051/tcp Zabbix Trapper
zabbix-trapper 10051/udp Zabbix Trapper
EOF

echo "copy conf to /opt/zabbix_agent/etc/"
cp -rpf ./zabbix_agent.conf /opt/zabbix_agent/etc/zabbix_agent.conf
cp -rpf ./zabbix_agentd.conf /opt/zabbix_agent/etc/zabbix_agentd.conf

echo "Create service..."
cp ./zabbix-2.4.4/misc/init.d/fedora/core/zabbix_agentd /etc/init.d/
chmod a+x /etc/init.d/zabbix_*

echo "copy zabbix_agentd..."
cp -rpf ./zabbix_agentd /etc/init.d/zabbix_agentd

echo "link to bin and sbin..."
ln -s /opt/zabbix_agent/sbin/* /usr/local/sbin/
ln -s /opt/zabbix_agent/bin/* /usr/local/bin/

#set serverip
sed -i 's/zbxserver/'$serverip'/g' /opt/zabbix_agent/etc/zabbix_agent.conf
sed -i 's/zbxserver/'$serverip'/g' /opt/zabbix_agent/etc/zabbix_agentd.conf

echo "Start service..."
chkconfig zabbix_agentd on
service zabbix_agentd start
sleep 2
ps -aux|grep zabbix_agentd

echo "========================================================================="
echo "Install finish!!!"
echo "========================================================================="
