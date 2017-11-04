#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('gbk')

# Settings of variables
KEY = 2 
PRINTERIP="172.17.233.41"
WEBSOCKETIP="172.17.233.2"
REDISIP="172.17.233.2"

class WebsocketConnect:
    def __init__(self,printerName='printer_kitchen',printerToken='302d9792344e40e3b16d2fc20a900dd7'):
        self.printerName = printerName
        self.printerToken = printerToken
