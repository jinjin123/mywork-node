#_*_coding:utf-8_*_
import sys
import datetime
import cookielib,urllib2,urllib
login_url = 'http://192.168.1.31/zabbix/index.php'
login_data = urllib.urlencode({
                        "name": 'Admin',
                        "password": 'zabbix',
                        "autologin": 1,
                        "enter": "Sign in"})

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
opener.open(login_url,login_data).read()
#sql_hostid = select hostid from hosts where host='192.168.1.101'; #通过host查询hostid
#sql_itemid = select itemid,`name`,key_ from items where hostid='10251' #通过hostid查询itemid，通过key_过滤性
能监视器
#sql_graphid = select graphid from graphs_items where itemid='33712' #通过itemid查询对应的graphid

graph_args = urllib.urlencode({
                        "graphid":'561',
                        "width":'400',
                        "height":'156',
                        "stime":'20160728213200', #图形开始时间
                        "period":'86400'})


graph_url = 'http://192.168.1.31/zabbix/chart2.php'
print graph_args  #返回格式：width=400&screenid=28&graphid=4769&period=86400&height=156

data = opener.open(graph_url,graph_args).read()
# print data
file=open('/root/a/2.png','wb')
file.write(data)
file.flush()
file.close()
