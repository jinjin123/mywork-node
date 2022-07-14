#_*_coding:utf-8_*_
import json,urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
#url and url header
#zabbix的api 地址，用户名，密码，这里修改为自己实际的参数
zabbix_url="http://172.16.240.250/zabbix/api_jsonrpc.php"
zabbix_header = {"Content-Type":"application/json"}
zabbix_user   = "admin"
zabbix_pass   = "1991jianke"
auth_code     = ""

#auth user and password
#用户认证信息的部分，最终的目的是得到一个SESSIONID
#这里是生成一个json格式的数据，用户名和密码
auth_data = json.dumps(
        {
            "jsonrpc":"2.0",
            "method":"user.login",
            "params":
                    {
                        "user":'admin',
                        "password":'1991jianke'
                    },
            "id":0
        })

# create request object
request = urllib2.Request(zabbix_url,auth_data)

for key in zabbix_header:
    request.add_header(key,zabbix_header[key])

try:
    result = urllib2.urlopen(request)
#对于出错新的处理
except HTTPError, e:
    print 'The server couldn\'t fulfill the request, Error code: ', e.code
except URLError, e:
    print 'We failed to reach a server.Reason: ', e.reason
else:
    response=json.loads(result.read())
    print response
    result.close()

#判断SESSIONID是否在返回的数据中
if  'result'  in  response:
    auth_code=response['result']
else:
    print  response['error']['data']
                                                                                                                                                                                    
# request json
#用得到的SESSIONID去通过验证，获取主机的信息（用http.get方法）
if len(auth_code) <> 0:
    host_list=[]
    get_host_data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"host.get",
        "params":{
                "output": "extend",
        },
        "auth":auth_code,
        "id":1,
    })

    # create request object
    request = urllib2.Request(zabbix_url,get_host_data)
    for key in zabbix_header:
        request.add_header(key,zabbix_header[key])

    # get host list
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        response = json.loads(result.read())
        result.close()                                                                                                                                                                        
        #将所有的主机信息显示出来
        for r in response['result']:
          #  print r['hostid'],r['host'] 打印所有主机
            host_list.append(r['hostid'])
        #显示主机的个数
        print "Number Of Hosts: ", len(host_list)

	get_item_data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": "10309",
                "search":{
                "name": "CPU Idle"
                        },
            "sortfield": "name"
                    },
            "auth": auth_code,
            "id": 1
        })
    request = urllib2.Request(zabbix_url,get_item_data)
    for key in zabbix_header:
           request.add_header(key,zabbix_header[key])
           result = urllib2.urlopen(request)

    try:
        result = urllib2.urlopen(request)    
        response = json.loads(result.read())
        for r in response['result']:
            print r['itemid'],r['hostid']
        result.close()    
    except:
        pass

    #通过hostid获取相应的graphid
    get_graph_data = json.dumps({
        "jsonrpc": "2.0",
        "method": "graphitem.get",
        "params": {
            "output": "extend",
            "expandData": 1,
            "itemids": "36725"
        },
        "auth": auth_code,
        "id": 1
    })
    request = urllib2.Request(zabbix_url,get_graph_data)
    for key in zabbix_header:
        request.add_header(key,zabbix_header[key])
    result = urllib2.urlopen(request)

    try:
        result = urllib2.urlopen(request)    
        response = json.loads(result.read())
        for r in response['result']:
            print r['itemid'],r['graphid']
        result.close()    
    except:
        pass
--------------------------------------------------------------
[root@localhost ~]# python 4.py 
{u'jsonrpc': u'2.0', u'result': u'd7004ea08c10f11ab25b9214822c3086', u'id': 0}
10285 172.16.108.105
10286 172.16.200.6
10287 172.16.200.10
10288 172.16.200.30
10289 172.16.200.31
10290 172.16.200.98
10292 172.16.240.4
10293 172.16.240.5
10294 172.16.240.11
10299 192.168.20.20
10300 172.16.240.16
10305 h3c-7503E-S
10309 172.16.201.110
10312 172.16.240.166
10315 172.16.240.233
10341 zabbix
10355 172.16.240.99-KVM
10356 172.16.240.212
10361 192.168.20.51
10363 192.168.20.52
10364 192.168.20.50
10365 172.16.12.2
10367 192.168.20.54
10368 221.4.131.12
10371 192.168.80.1
10372 118.194.44.37
10373 122.13.166.119
10374 172.16.11.2
10377 192.168.20.253
10381 12.2
10383 172.16.108.91
10384 172.16.108.92
10387 192.168.20.101
Number Of Hosts:  33
36725 10309
36725 3157
