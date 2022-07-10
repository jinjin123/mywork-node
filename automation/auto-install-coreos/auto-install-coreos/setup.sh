#!/bin/bash
Home='/home/core'
RT='/root'
CodeFe='/home/core/code'
ScriptFe='/home/core/scripts'
SystemFe='/etc/systemd'
KeyFe='/home/core/keys'
DockerFe='/home/core/docker'
CommandFe='/opt/bin'
MysqlFebk='/home/core/mysql/backup'
MysqlFebklink='/var/lib/mysql'
IMG='/home/core/IMG'
Dockerconfurl='http://192.168.1.4/dockerconf/dockerconf.tar'
Nginxurl='http://192.168.1.4/img/nginx.tar.gz'
Kcurl='http://192.168.1.4/img/kc.tar.gz'
Mysqlurl='http://192.168.1.4/img/mysql.tar.gz'
Busurl='http://192.168.1.4/img/bus.tar.gz'
SSHurl='http://192.168.1.4/scripts/scripts.tar'
Keyurl='http://192.168.1.4/keys/keys.tar'
Commandurl='http://192.168.1.4/command/command.tar'
RTscript='http://192.168.1.4/root/scripts.tar'
Systemurl='http://192.168.1.4/system/system.tar'
Buscodeurl='http://192.168.1.4/code/buscode.tar.gz'    
Kccodeurl='http://192.168.1.4/code/kcconf.tar'    
Kpcodeurl='http://192.168.1.4/code/kpconf.tar'    
Pythonurl='http://192.168.1.4/python/python.tar.gz'
Python='/opt'
networkPath='/etc/systemd/system'
network2Path='/etc/systemd/network'
Dburl='http://192.168.1.4/dbframework/data.tar'
DbFe='/home/core/mysql'
IP=`ifconfig | grep -A1 'enp' | awk 'NR==2 {print $0}'| awk '{print $2}'`
#IP=`ifconfig | grep -A1 'ens' | awk 'NR==2 {print $0}'| awk '{print $2}'`

#mkdir dir
#[ -e ${CodeFe} ]  || mkdir -p ${CodeFe}  && echo "mkdir codefe ok" >> /tmp/${IP}.log
#[ -e ${CommandFe} ]  || mkdir -p ${CommandFe}  && echo "mkdir CommandFe ok" >> /tmp/${IP}.log
#[ -e ${DockerFe} ]  || mkdir -p ${DockerFe} && echo "mkdir DockerFe ok" >> /tmp/${IP}.log
#[ -e ${ScriptFe} ]  || mkdir -p ${ScriptFe} && echo "mkdir ScriptFe ok" >> /tmp/${IP}.log
[ -e ${sqlframeworkFe} ]  || mkdir -p ${sqlframeworkFe} && echo "mkdir sqlframeworkFe ok" >> /tmp/${IP}.log
[ -e ${MysqlFebk} ]  || mkdir -p ${MysqlFebk} && echo "mkdir MysqlFebk ok" >> /tmp/${IP}.log || sudo echo "mkdir MysqlFebk faild" >> /tmp/${IP}.log 
[ -e ${MysqlFebklink} ]  || mkdir -p ${MysqlFebklink} && sudo chmod 777 ${MysqlFebklink} && sudo  echo "mkdir MysqlFebklink ok" >> /tmp/${IP}.log ||sudo  echo "mkdir MysqlFebk faild" >> /tmp/${IP}.log

#get resource
[ -e ${IMG} ]  || mkdir -p ${IMG} && cd ${IMG} && wget ${Nginxurl};unzip ${IMG}/nginx.tar.gz &&sudo  echo "mkdir img&get the Nginx.tar resource &unzip the resource ok" >> /tmp/${IP}.log ||sudo  echo "mkdir img&get the Nginx.tar resource &unzip the resource faild" >> /tmp/${IP}.log 
[ -e ${IMG} ]  || mkdir -p ${IMG} && cd ${IMG} && wget ${Kcurl};unzip ${IMG}/kc.tar.gz && sudo echo "mkdir img&get the Kc.tar resource &unzip the resource ok" >> /tmp/${IP}.log || sudo echo "mkdir img&get the Kc.tar resource &unzip the resource faild" >> /tmp/${IP}.log
[ -e ${IMG} ]  || mkdir -p ${IMG} && cd ${IMG} && wget ${Mysqlurl};unzip ${IMG}/mysql.tar.gz && sudo  echo "mkdir img&get the Mysql.tar resource &unzip the resource ok" >> /tmp/${IP}.log ||sudo  echo "mkdir img&get the Mysql.tar resource &unzip the resource faild" >> /tmp/${IP}.log
[ -e ${IMG} ]  || mkdir -p ${IMG} && cd ${IMG} && wget ${Busurl};unzip ${IMG}/bus.tar.gz &&sudo echo "mkdir img&get the Bus.tar resource &unzip the resource ok" >> /tmp/${IP}.log ||sudo  echo "mkdir img&get the Bus.tar resource &unzip the resource faild" >> /tmp/${IP}.log
[ -e ${DockerFe} ]  || cd ${Home}; wget ${Dockerconfurl}; tar -xf dockerconf.tar &&sudo echo "get the dockerconf  resource &unzip the resource ok" >> /tmp/${IP}.log || sudo echo "get the dockerconf  resource &unzip the resource faild" >> /tmp/${IP}.log

#get kc data
[ -e ${DbFe} ]  || cd ${DbFe}; wget -P ${DbFe} ${Dburl};tar -xf ${DbFe}/data.tar  -C ${DbFe} &&sudo echo "get the  kcdata resource &unzip the resource ok" >> /tmp/${IP}.log || sudo echo "get the kcdata  resource &unzip the resource faild" >> /tmp/${IP}.log

#get code
[ -e ${CodeFe} ]  || mkdir -p ${CodeFe} && cd ${CodeFe} &&  wget ${Buscodeurl};unzip ${CodeFe}/buscode.tar.gz;tar -xf ${CodeFe}/buscode.tar -C ${CodeFe};echo "get the buscodeconf ok" >> /tmp/${IP}.log || echo "get the buscodeconf faild" >> /tmp/${IP}.log 
[ -e ${CodeFe} ]  || mkdir -p ${CodeFe} && cd ${CodeFe} &&  wget ${Kccodeurl};tar -xf ${CodeFe}/kcconf.tar -C ${CodeFe}; echo "get the kccodeconf ok" >> /tmp/${IP}.log || echo "get the kccodeconf faild" >> /tmp/${IP}.log 
#[ -e ${CodeFe} ]  || mkdir -p ${CodeFe} && cd ${CodeFe} &&  wget ${Kpcodeurl};tar -xf ${CodeFe}/kpconf.tar -C ${CodeFe}; echo "get the kpcodeconf ok" >> /tmp/${IP}.log || echo "get the kpcodeconf faild" >> /tmp/${IP}.log 

#SSH script; remote key ;scp key
[ -e ${ScriptFe} ]  || cd ${Home};wget -P ${Home} ${SSHurl}; tar -xf ${Home}/scripts.tar && sudo echo "get the sshscript resource &unzip the resource ok" >> /tmp/${IP}.log ||sudo echo "get the sshscript resource &unzip the resource faild" >> /tmp/${IP}.log
#[ -e ${KeyFe} ]  || cd ${Home};wget -P ${Home} ${keyurl}; tar -xf ${Home}/keys.tar -C ${Home} && sudo echo "get the key resource &unzip the resource ok" >> /tmp/${IP}.log || sudo echo "get the key resource &unzip the resource faild" >> /tmp/${IP}.log && sudo chown -R core:core ${Home}
cd ${Home};wget -P /home/core http://192.168.1.4/keys/keys.tar; tar -xf ${Home}/keys.tar -C ${Home}
cd ${Home};wget -P /home/core/keys http://192.168.1.4/keys/id_rsa;sudo chown core.core -R /home/core

# compose mysqldump
[ -e ${CommandFe} ]  || sudo mkdir -p ${CommandFe} && sudo wget -P ${CommandFe} ${Commandurl}; sudo tar -xf ${CommandFe}/command.tar -C ${CommandFe} &&  sudo mv  ${CommandFe}/command/* ${CommandFe}/  && sudo  echo "mkdir CommandFe&get the command ok" >> /tmp/${IP}.log || sudo echo "mkdir CommandFe&get the command faild" >> /tmp/${IP}.log

#load img
[ -f ${IMG}/kc.tar ] && /usr/bin/docker load < ${IMG}/kc.tar; sudo echo "load kc.tar ok" >> /tmp/${IP}.log ||sudo echo "load kc.tar faild" >> /tmp/${IP}.log
[ -f ${IMG}/bus.tar ] && /usr/bin/docker load < ${IMG}/bus.tar;sudo echo "load bus.tar ok" >> /tmp/${IP}.log ||sudo  echo "load bus.tar faild" >> /tmp/${IP}.log
[ -f ${IMG}/nginx.tar ] && /usr/bin/docker load < ${IMG}/nginx.tar;sudo echo "load nginx.tar ok" >> /tmp/${IP}.log ||sudo echo "load nginx.tar faild" >> /tmp/${IP}.log
[ -f ${IMG}/mysql.tar ] && /usr/bin/docker load < ${IMG}/mysql.tar;sudo echo "load mysql.tar ok" >> /tmp/${IP}.log ||sudo echo "load mysql.tar faild" >> /tmp/${IP}.log

#RT  script
sudo wget -P ${RT} ${RTscript};sudo tar -xf ${RT}/scripts.tar -C ${RT}; sudo mv ${RT}/scripts/*  ${RT} && sudo rm -rf *.tar && sudo chmod +x ${RT}/*

#install python
sudo wget -P  ${Python} ${Pythonurl} && sudo tar -xf ${Python}/python.tar.gz -C ${Python} && sudo mv ${Python}/ActivePython-2.7.8.10-linux-x86_64 ${Python}/apy 
sudo /bin/sh ${Python}/apy/install.sh -I /opt/python/
sudo ln -s /opt/python/bin/easy_install /opt/bin/easy_install
sudo ln -s /opt/python/bin/pip /opt/bin/pip
sudo ln -s /opt/python/bin/python /opt/bin/python
sudo ln -s /opt/python/bin/virtualenv /opt/bin/virtualenv

#init network
sudo mv ${networkPath}/static.network.bak ${network2Path}/static.network && sudo echo  'init network ok' >> /tmp/${IP}.log || sudo echo 'init network faild' >> /tmp/${IP}.log

#get system service
sudo rm -rf ${SystemFe}/system && sudo wget -P ${SystemFe} ${Systemurl} && sudo tar -xf ${SystemFe}/system.tar -C  ${SystemFe} && sudo echo "get the systemdir  instead of source ok" >> /tmp/${IP}.log || sudo  echo "mkdir systemdir&get the systemreourse faild" >> /tmp/${IP}.log 

#enable service
#sudo cd ${SystemFe}/system && sudo ls -l | awk '/.service$/{print $9}' | xargs sudo systemctl enable {} && sudo echo "enable service ok " >> /tmp/${IP}.log ||sudo echo "enable service  faild" >> /tmp/${IP}.log
sudo cd ${SystemFe}/system &&  sudo systemctl enable *.service && sudo echo "enable service ok " >> /tmp/${IP}.log ||sudo echo "enable service  faild" >> /tmp/${IP}.log
#sudo cd ${SystemFe}/system && sudo ls -l | awk '/.timer$/{print $9}' | xargs sudo systemctl enable {} && sudo echo "enable service ok " >> /tmp/${IP}.log || sudo echo "enable service faild" >> /tmp/${IP}.log
sudo cd ${SystemFe}/system &&  sudo systemctl enable *.timer && sudo echo "enable timer ok " >> /tmp/${IP}.log || sudo echo "enable timer faild" >> /tmp/${IP}.log

#synchronism time
sudo rm -rf /etc/localtime && sudo  ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && date | awk '{if($6=="CST"){print "ok"}}' | xargs sudo echo "synchronism time " >> /tmp/${IP}.log 

#result use key to scp
sudo systemctl start storecore
scp -i /home/core/keys/id_rsa /tmp/${IP}.log jin@192.168.1.4:/home/jin/result
#/opt/bin/mysql -uroot -proot -e "use kc;source /home/core/dbframework/kc.sql;"
#sudo reboot



#系统日志要限制大小 ,key 下载 ,数据库的创建，配置文件的修改 定时器有三个脚本 备份删除数据 重启storecore  啦代码的key  还有登陆的key 还有python  还有远程链接的key
#所有代码配置要统一
