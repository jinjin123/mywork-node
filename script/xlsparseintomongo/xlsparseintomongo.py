#coding=utf-8
import xlrd
import sys
import json
import pymongo
from pymongo import MongoClient

#连接数据库
client=MongoClient('localhost',27017)
db=client.local
account=db.weibo

data=xlrd.open_workbook('sid-ip2222.xlsx')
table=data.sheets()[0]
#读取excel第一行数据作为存入mongodb的字段名
rowstag=table.row_values(0)
nrows=table.nrows
#ncols=table.ncols
#print rows
returnData={}
for i in range(1,nrows):
    #将字段名和excel数据存储为字典形式，并转换为json格式
    returnData[i]=json.dumps(dict(zip(rowstag,table.row_values(i))))
    #通过编解码还原数据
    returnData[i]=json.loads(returnData[i])
    #print returnData[i]
    account.insert(returnData[i])
