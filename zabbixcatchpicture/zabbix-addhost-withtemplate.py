# -*- coding: UTF-8 -*-
import urllib2,json,cookielib,urllib
from urllib2 import Request, urlopen, URLError, HTTPError
global auth_code,zabbix_url,zabbix_header
#zabbix接口地址、登录地址、图片地址
zabbix_url="http://10.16.2.4/zabbix/api_jsonrpc.php"

zabbix_header = {"Content-Type":"application/json"}
zabbix_user   = "admin"
zabbix_pass   = "password"
auth_code     = ""
auth_data = json.dumps({
    "jsonrpc":"2.0",
    "method":"user.login",
    "params":
            {
            "user":zabbix_user,
            "password":zabbix_pass
            },
    "id":0
    })


request = urllib2.Request(zabbix_url,auth_data)
for key in zabbix_header:
    request.add_header(key,zabbix_header[key])
try:
    result = urllib2.urlopen(request)
except HTTPError, e:
    print 'The server couldn\'t fulfill the request, Error code: ', e.code
except URLError, e:
    print 'We failed to reach a server.Reason: ', e.reason
else:
    response=json.loads(result.read())
    #print response
    result.close()

#判断SESSIONID是否在返回的数据中
if  'result'  in  response:
    auth_code=response['result']
else:
    print  response['error']['data']

def Http_access(data):
    request = urllib2.Request(zabbix_url,data)
    for key in zabbix_header:
        request.add_header(key,zabbix_header[key])
    result = urllib2.urlopen(request)
    
    response = json.loads(result.read())
    # print result.read()
    # print response
    result.close()  
    if len(response['result']) > 0:
        return response['result']

def Http_access(data):
    request = urllib2.Request(zabbix_url,data)
    for key in zabbix_header:
        request.add_header(key,zabbix_header[key])
    result = urllib2.urlopen(request)
    
    response = json.loads(result.read())
    # print result.read()
    #print response
    result.close()  
    if len(response['result']) > 0:
        return response['result']

#定义模板名称
def get_template():
    template_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "extend",
            "filter": {
                "host": [
                    "template-windows-basic" #定义模板名称
                ]
            }
        },
        "auth": auth_code,
        "id": 1
    })
    return template_data


#过滤所有模板
def get_template():
    template_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "extend"
        },
        "auth": auth_code,
        "id": 1
    })
    return template_data



#配置需要添加的host信息（Host Name，IP，groupID，templateID）
def add_hostdata():
    if len(auth_code) <> 0:
        host_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": "Mail CAS_1.41", #Host Name
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": "10.16.3.4", #Host IP
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": "30" #group-live-uxdata-windows
                }
            ],
            "templates": [
                {
                    "templateid": "10132" #template ID
                }
            ]
        },
        "auth": auth_code,
        "id": 1
    })
    return host_data 
    
    ----------------------------------------------
    
hostdata =add_hostdata()
print Http_access(hostdata) #添加主机的


templatedata = get_template()
print Http_access(templatedata)[0]['templateid']  #d得到指定模版ID

templatedata = get_template()
for template in Http_access(templatedata):
    print template['templateid'],template['host'] #获取所有模版ID
[root@localhost a]# python 4.py 
10001 Template OS Linux
10047 Template App Zabbix Server
10048 Template App Zabbix Proxy
10050 Template App Zabbix Agent
10060 Template SNMP Interfaces
10065 Template SNMP Generic
10066 Template SNMP Device
10067 Template SNMP OS Windows
10068 Template SNMP Disks
10069 Template SNMP OS Linux
10070 Template SNMP Processors
10071 Template IPMI Intel SR1530
10072 Template IPMI Intel SR1630
10073 Template App MySQL
10074 Template OS OpenBSD
10075 Template OS FreeBSD
10076 Template OS AIX
10077 Template OS HP-UX
10078 Template OS Solaris

