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
import os

class Saber:
	def __init__(self):
            pass

	def on_open(self,ws):
            now = datetime.datetime.now()
            print "## %s connect bus true##" % (now.strftime('%c'))
            def fly():
	        wss = WebsocketConnect()
                ws.send('<notification><from>' + wss.printerName + '</from><to>' + wss.printerName + '</to><message></message><token>' + wss.printerToken + '</token></notification>')
                t = Timer(4,fly)
                t.start()
            fly()

	def on_message(self,ws, message):
                global REDISIP
                global KEY
		cache = redis.StrictRedis(REDISIP,6379)
                key = KEY
                cache.set(key,message)
                os.system('python /usr/local/proxy/printer/print.py')

        def on_error(self,ws, error):
		pass
                #now = datetime.datetime.now()
                #print error + "%s" %(now.strftime('%c'))

        def on_close(self,ws):
		pass
                #now = datetime.datetime.now()
                #print "## %s connect bus faild##" % (now.strftime('%c'))

if __name__ == '__main__':
    saber = Saber()
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://" + WEBSOCKETIP + ":8080/websocketServer",
                              on_message = saber.on_message,
                              on_error = saber.on_error,
                              on_close = saber.on_close)

    ws.on_open = saber.on_open
    while True:
    	try:
    		ws.run_forever()
    	except:
    		ws.run_forever()
