#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
from Setconfig import * 
from escpos.printer import Network
import json

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def fly():
            ws = WebsocketConnect(printerName='printerFPOS',printerToken='29a72e71be65404e8799ede72bdeaef3')
            self.sendMessage('<notification><from>' + ws.printerName + '</from><to>' + ws.printerName + '</to><message></message><token>' + ws.printerToken + '</token></notification>')
            #self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            #self.factory.reactor.callLater(1, hello)
        # start sending messages every second ..
        fly()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            #print("Text message received: {0}".format(payload.decode('utf8')))
            dict = eval(payload.decode('utf8'))
            #print dict
            #init push printer character 
            if dict.get('orderType') == 4:  #ordertype 0 push printer ? 4 changetable  and openmoneybox
                try:
                    #cash drawer at 10.02
                    changeTable = dict.get('data')
                    #print changeTable
                    changeTabledict = eval(changeTable) 
                    storeName =  json.dumps(changeTabledict.get('storeName'),encoding='UTF-8',ensure_ascii=False)
                    storeNamefull = storeName.replace("\"","") #店名
                    storeId = changeTabledict.get('storeId')#店铺编号
                    operaterName = changeTabledict.get('operaterName') #收银员名字
                    startTime = changeTabledict.get('startTime')#当前收银员 开始收银时间
                    endTime = changeTabledict.get('endTime') #当前收银员 结束收银时间
                    printerTime = changeTabledict.get('printerTime')#打单时间
                    machineId = changeTabledict.get('machineId')#机号
                    orderNum = changeTabledict.get('orderNum')#总订单量
                    total = changeTabledict.get('total')#合计 总价格
                    mainIncome = changeTabledict.get('mainIncome')#主要业务收入
                    otherIncome = changeTabledict.get('otherIncome')#其他业务收入
                    netIncome = changeTabledict.get('netIncome')#净销售=主要业务=total
                    discount = changeTabledict.get('discount')#折扣
                    p = Network("192.168.1.4")
                    p.set(align='center',font='B',text_type='normal',height=1,width=2,invert=False, smooth=False,flip=False)
                    p.text(u"收银员转桌报告\n".encode('gbk'))
                    p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,
                        flip=False)
                    p.text(u"%s\t%s\n".encode('gbk') % (storeNamefull,storeId))
                    p.text(u"开始时间: %s\n".encode('gbk') % startTime)
                    p.text(u"结束时间: %s\n\n".encode('gbk') % endTime)
                    p.set(align='center',font='a',text_type='normal',height=1,width=2,invert=False, smooth=False,flip=False)
                    p.text(u"收银员: (%s)操作员\n".encode('gbk') % operaterName)
                    p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                    p.text(u"打印时间:%s\n".encode('gbk') % printerTime)
                    p.text(u"机号:[%s]\t %s \t\t\r%s\n".encode('gbk') % (machineId,orderNum,total))
                    p.set(align='left',font='B',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                    p.text(u"\n\t销售数据\n".encode('gbk'))
                    p.set(align='left',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                    p.text(u"+主营业收入\t\t\t\t%s\n".encode('gbk') % mainIncome)
                    p.text(u"+其他业务收入\t\t\t\t%s\n".encode('gbk') % otherIncome)
                    p.text(u"=净销售\t\t\t\t\t%s\n".encode('gbk') % netIncome)
                    p.text(u"+折扣\t\t\t\t\t%s\n".encode('gbk') % discount)
                    p.text(u"+进位差\t\t\t\t\t0\n".encode('gbk') )
                    p.text(u"=应收现金\t\t\t\t%s\n".encode('gbk') % netIncome)
                    p.set(align='left',font='B',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                    p.text(u"\n\t合计部门报表\n".encode('gbk'))
                    allPay = changeTabledict.get('allPay')
                    for allpay in allPay:
                        payName = json.dumps(allpay.get('payName'),encoding='UTF-8',ensure_ascii=False)
                        payNamefull = payName.replace("\"","") 
                        countOrderNum = allpay.get('countOrderNum')
                        totalAmount = allpay.get('totalAmount')
                        p.set(align='left',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                        p.text(u"%s\t\t%s\t\t\t%s\n".encode('gbk') % (payNamefull,countOrderNum,totalAmount))
                    otherStatistics = changeTabledict.get('otherStatistics')
                    p.set(align='left',font='B',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                    p.text(u"\n\t其他统计\n".encode('gbk'))
                    for otherstatistics in otherStatistics: 
                        kindName = json.dumps(otherstatistics.get('kindName'),encoding='UTF-8',ensure_ascii=False)
                        kindNamefull = kindName.replace("\"","")
                        Number = otherstatistics.get('Number')
                        totalAmountO = otherstatistics.get('totalAmount')
                        p.set(align='left',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                        p.text(u"%s\t\t\t\t\r%s\n".encode('gbk') % (kindNamefull,totalAmountO))
                    p.cut()
                except:
                        print "SyntaxError about changetable"

            if dict.get('orderType') == 0:  #ordertype 0 push printer ? 4 changetable  and openmoneybox
                try:
                    #cash drawer at 10.02
                    Big = dict.get('data')
                    Bigstr = str(Big)
                    Bigdict = eval(Bigstr)
                    #print Bigdict #if not data ? print dict.get('data') : true
                    title = json.dumps(Bigdict.get('title'),encoding='UTF-8',ensure_ascii=False)
                    titlefull = title.replace("\"","") 
                    #print titlefull
                    orderId = Bigdict.get('orderId') #取餐号
                    #print orderId
                    machineId = Bigdict.get('machineId') #机号
                    #print type(machineId)
                    cashier = Bigdict.get('cashier') #收银员
                    #print type(cashier)
                    orderTime = Bigdict.get('orderTime') #下单时间
                    #print orderTime
                    kindchagne =  json.dumps(Bigdict.get('kind'),encoding='UTF-8',ensure_ascii=False)
                    #print kindchagne
                    kind = kindchagne.replace("\"","") #堂食/外卖
                    #print kindfull
                    storeAddr = Bigdict.get('storeAddr') 
                    #print storeAddr
                    storeAddrchagne =  json.dumps(Bigdict.get('storeAddr'),encoding='UTF-8',ensure_ascii=False)
                    storeAddrfull = storeAddrchagne.replace("\"","") #餐厅地址
                    payType = Bigdict.get('payType') #支付类型：现金,支付宝,微信,会员卡
                    total = Bigdict.get('total') #需要支付的总金额
                    total2 = total.replace("\"","")
                    #print total2
                    discount = Bigdict.get('discount') #优惠金额
                    #discount2 = discount.replace("\"","")
                    payCashNumber = Bigdict.get('payCashNumber')#支付的现金数量
                    payCashNumber2 = payCashNumber.replace("\"","")
                    #print payCashNumber2
                    card_id = Bigdict.get('card_id') #会员卡卡号
                    card_balance = Bigdict.get('card_balance') # 会员卡余额
                    card_getIntegral = Bigdict.get('card_getIntegral') #本次获得积分
                    card_totalIntegral = Bigdict.get('card_totalIntegral') #可用积分 （即总积分）
                    payTransactionNumber = Bigdict.get('payTransactionNumber') #支付交易号（针对微信，支付宝）
                    storename =  json.dumps(Bigdict.get('storename'),encoding='UTF-8',ensure_ascii=False)
                    storenamefull = storename.replace("\"","") #餐厅名称
                    storeNum = Bigdict.get('storeNum') #餐厅电话
                    footer =  json.dumps(Bigdict.get('footer'),encoding='UTF-8',ensure_ascii=False)
                    footerfull = footer.replace("\"","") #结束语
                    p = Network("192.168.1.4")
                    p.set(align='center',font='B',text_type='normal',height=1,width=2,invert=False, smooth=False,flip=False)
                    p.text(u'%s\n\n'.encode('gbk') % titlefull)
                    p.set(align='left',font='a',text_type='normal',height=1,width=1)
                    p.text(u"地址: [%s]\n".encode('gbk') % storeAddrfull)
                    p.text(u"收银员: [%s]\t\t\t".encode('gbk') % cashier)
                    p.text(u"机号: [%s]\n".encode('gbk') % machineId)
                    p.text(u"打单时间: [%s]\n\n".encode('gbk') % orderTime)
                    p.set(align='center',font='B',text_type='normal',height=2,width=2,invert=False, smooth=False,flip=False)
                    p.text(u"取餐号: [%s]\n\n".encode('gbk') % orderId )
                    p.set(align='center',font='a',text_type='normal',height=1,width=1)
                    p.text(u'%s\n'.encode('gbk') % kind)
                    p.set(align='left',font='a',text_type='normal',height=1,width=1)
                    p.text(u"数量\t产品名称\t\t\t金额\n".encode('gbk'))
                    prodList = Bigdict.get('prodList') #菜品信息
                    #print prodList
                    for prodListdict in prodList:
                            #print prodListdict
                            #print type(prodListdict)
                            foodnum = prodListdict.get('num')
                            foodnamechagne =  json.dumps(prodListdict.get('name'),encoding='UTF-8',ensure_ascii=False)
                            foodname = foodnamechagne.replace("\"","")
                            foodsum = prodListdict.get('sum')
                            #foodsum2 = ("%.2f" % foodsum)
                            #输出数量,产品,金额
                            p.text(u"%s\t\r%s\t\t\t\r%s\n".encode('gbk') % (foodnum,foodname,foodsum))
                    p.text(u"\n总\t价:\t\t\t\t%s\n".encode('gbk') % total2 )
                    p.text(u"优\t惠:\t\t\t\t%s\n".encode('gbk') % discount )
                    p.text(u"应\t收:\t\t\t\t%s\n".encode('gbk') % payCashNumber2)
                    p.text(u"找\t零:\t\t\t\t0.00\n".encode('gbk') )
                    p.set(align='center',font='a',text_type='normal',height=1,width=1)
                    p.text(u'%s\n\n'.encode('gbk') % footerfull)
                    p.text(u'扫描二维码加入真功夫会员，每消费\n一元累计1积分，积分可兑换美食和\n体验，扫描时请保持小票平整！\n'.encode('gbk'))
                    p.image("tx.png")
                    p.cut()
                except:
                    print "SyntaxError about push printer"   

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys
    reload(sys)
    sys.setdefaultencoding('gbk')
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://192.168.1.4:8080/websocketServer")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("192.168.1.4", 8080, factory)
    reactor.run()

