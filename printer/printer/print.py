#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('gbk')
import websocket
from threading import Timer
from escpos.printer import Network
from config import *
import json
import datetime
import redis

def start():
            global REDISIP
            global KEY
            global PRINTERIP

	    cache = redis.StrictRedis(REDISIP,6379)
            key = KEY
            message = cache.get(key)
            dict = eval(message)
            print dict
            #init push printer character 
            if dict.get('orderType') == 1: 
                    Big = dict.get('data')
                    Bigstr = str(Big)
                    Bigdict = eval(Bigstr)
                    title = json.dumps(Bigdict.get('storeName'),encoding='UTF-8',ensure_ascii=False)
                    titlefull = title.replace("\"","")
                    orderId = Bigdict.get('orderId')
                    machineId = Bigdict.get('machineId')
                    cashier = Bigdict.get('cashier')
                    orderTime = Bigdict.get('orderTime')
                    takefoodNum = Bigdict.get('takefoodNum') #取餐号
                    kindchagne =  json.dumps(Bigdict.get('kind'),encoding='UTF-8',ensure_ascii=False)
                    kind = kindchagne.replace("\"","")  #堂食 / 外带
                    try:
	                    print "init printer"
	                    p = Network(PRINTERIP,timeout=10000)
	                    p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
	                    p.text(u"欢迎光临真功夫[%s]\n\n".encode('gbk') % titlefull)
	                    p.set(align='center',font='B',text_type='B',height=2,width=2,invert=False, smooth=False,flip=False)
	                    p.text(u"取货单\n\n".encode('gbk'))
	                    p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
	                    p.text(u"单号：[%s]\t 机号: [%s]\n 收银员: [%s]\n ".encode('gbk') % (orderId,machineId,cashier))
	                    p.text(u"打单时间: [%s]\n\n".encode('gbk') % orderTime)
	                    p.set(align='center',font='B',text_type='B',height=2,width=2,invert=False, smooth=False,flip=False)
	                    p.text(u"取餐号: %s\n\n".encode('gbk') % (takefoodNum))
	                    p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
	                    p.text(u"[%s]合计 Total\n".encode('gbk') % (kind))
	                    p.set(align='left',font='a',text_type='normal',height=1,width=1,density=8,invert=False, smooth=False,flip=False)
	                    p.text(u"数量\t\t产品名称\r\n".encode('gbk'))
	                    prodList = Bigdict.get('prodList')
	                    for prodListdict in prodList:
	                            foodnum = prodListdict.get('num')
	                            #print foodnum
	                            foodnamechagne =  json.dumps(prodListdict.get('name'),encoding='UTF-8',ensure_ascii=False)
	                            foodname = foodnamechagne.replace("\"","")
	                            #print foodname
	                            p.text(u"%s\t%s\n".encode('gbk') % (foodnum,foodname))
	                    p.cut()

                    except Exception as e:
	                    print ("connect printer %s") % (e)  
	                    print ("please look at the bus about printer_kitchen alive")


start()
