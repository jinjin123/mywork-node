mkdir  /app/mysql


####
zabbix-agent
|-- conf
|   -- zabbix-agentd.conf
 -- docker-compose.yml
conf/zabbix-agentd.conf 的内容如下：

LogFile=/tmp/zabbix_agentd.log
EnableRemoteCommands=1
Server=192.168.1.100
ListenPort=10050
ServerActive=192.168.1.100
