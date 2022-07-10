#!/usr/bin/python
import os
import pymysql
import requests
import boto3
import time

db= pymysql.connect(host='10.0.0.30',port=3306,user='root', passwd='root', db='spiderflowbak',charset='utf8')
cursor = db.cursor()

cursor.execute("select cateimg2 from watch2 where cateimg is  null and  detailimg != '' and detailimg !='[]' and id > 30000 and  cateimg2 not like '%base64%'")
data = [i[0] for i in cursor.fetchall()]

s3 = boto3.resource('s3')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER'}
for ul in data:
  res=requests.get(ul,headers=headers)
  imgname = ul.split("uhren/")[1]
  #s3 url save to db
  url="https://wristcheck.s3.ap-east-1.amazonaws.com/detailImg/"+ imgname
  s3.Bucket('wristcheck').put_object(Key="detailImg/"+imgname, Body=res.content)

  l="""update watch2 set cateimg = ("%s") where cateimg2 = ("%s")""" % (url,ul)
  b="""insert into log  (detailUrl) values ("%s") """ % (ul)
  try:
    cursor.execute(l)
    cursor.execute(b)
    db.commit()
  except:
    pass
  time.sleep(1.5)

