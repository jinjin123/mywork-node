#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
from threading import Timer
from escpos.printer import Usb
import json

class WebsocketConnect:
    def __init__(self,printerName='printerFPOS',printerToken='d947750a358f4bc197364380cd1a9e7b'):
        self.printerName = printerName
        self.printerToken = printerToken

class MyClientProtocol(WebSocketClientProtocol):
    storeNamefull = ''  #店名
    storeId = ''  #店铺编号
    operaterName = ''   #收银员名字 
    startTime = ''#当前收银员 开始收银时间
    endTime = ''#当前收银员 结束收银时间
    printerTime = ''#打单时间
    machineId = ''#机号
    machineId = ''#总订单量
    orderNum = '' #合计 总价格 
    total = ''#主要业务收入
    mainIncome = '' #主要业务收入
    otherIncome = ''#其他业务收入
    netIncome = ''#净销售=主要业务=total
    discount = ''#折扣
    allpay = ''  #  所有支付方式
    otherStatistics = '' 
    titlefull = '' 
    orderId = ''
    machineId = '' 
    cashier  = ''
    orderTime = ''
    kind = ''
    storeAddrfull = ''
    payType = ''
    total2 = ''
    discount = ''
    payCashNumber2 = ''
    card_id = ''#会员卡卡号
    card_balance = '' # 会员卡余额
    card_getIntegral = '' #本次获得积分
    card_totalIntegral = '' #可用积分 （即总积分）
    payTransactionNumber = '' #支付交易号（针对微信，支付宝）
    storenamefull = ''#餐厅名称
    storeNum = ''#餐厅电话
    footer =  ''
    footerfull = '' #结束语


    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def fly():
            ws = WebsocketConnect()
            self.sendMessage('<notification><from>' + ws.printerName + '</from><to>' + ws.printerName + '</to><message></message><token>' + ws.printerToken + '</token></notification>')
            t = Timer(4,fly)
            t.start()
        fly()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            #print("Text message received: {0}".format(payload.decode('utf8')))
            dict = eval(payload.decode('utf8'))
            print dict
            #init push printer character 
            if dict.get('orderType') == 4:  #ordertype 0 push printer ? 4 changetable  and openmoneybox
                    changeTable = dict.get('data')
                    changeTabledict = eval(changeTable) 
                    storeName =  json.dumps(changeTabledict.get('storeName'),encoding='UTF-8',ensure_ascii=False)
                    MyClientProtocol.storeNamefull = storeName.replace("\"","") #店名
                    MyClientProtocol.storeId = changeTabledict.get('storeId')#店铺编号
                    MyClientProtocol.operaterName = changeTabledict.get('operaterName') #收银员名字
                    MyClientProtocol.startTime = changeTabledict.get('startTime')#当前收银员 开始收银时间
                    MyClientProtocol.endTime = changeTabledict.get('endTime') #当前收银员 结束收银时间
                    MyClientProtocol.printerTime = changeTabledict.get('printerTime')#打单时间
                    MyClientProtocol.machineId = changeTabledict.get('machineId')#机号
                    MyClientProtocol.orderNum = changeTabledict.get('orderNum')#总订单量
                    MyClientProtocol.total = changeTabledict.get('total')#合计 总价格
                    MyClientProtocol.mainIncome = changeTabledict.get('mainIncome')#主要业务收入
                    MyClientProtocol.otherIncome = changeTabledict.get('otherIncome')#其他业务收入
                    MyClientProtocol.netIncome = changeTabledict.get('netIncome')#净销售=主要业务=total
                    MyClientProtocol.discount = changeTabledict.get('discount')#折扣
                    def shield():
                        try:
                            p = Usb(0x04b8,0x0e0f)
                            p.set(align='center',font='B',text_type='normal',height=1,width=2,invert=False, smooth=False,flip=False)
                            p.text(u"收银员转桌报告\n".encode('gbk'))
                            p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,
                                flip=False)
                            p.text(u"%s\t%s\n".encode('gbk') % (MyClientProtocol.storeNamefull,MyClientProtocol.storeId))
                            p.text(u"开始时间: %s\n".encode('gbk') % MyClientProtocol.startTime)
                            p.text(u"结束时间: %s\n\n".encode('gbk') % MyClientProtocol.endTime)
                            p.set(align='center',font='B',text_type='B',height=2,width=2,invert=False, smooth=False,flip=False)
                            p.text(u"收银员: (%s)操作员\n".encode('gbk') % MyClientProtocol.operaterName)
                            p.set(align='center',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                            p.text(u"\n打印时间:%s\n".encode('gbk') % MyClientProtocol.printerTime)
                            p.text(u"机号:[%s]\t %s \t\t\r%s\n".encode('gbk') % (MyClientProtocol.machineId,MyClientProtocol.orderNum,MyClientProtocol.total))
                            p.text("----------------------------------------------")
                            p.set(align='center',font='B',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                            p.text(u"\n\t销售数据\n".encode('gbk'))
                            p.set(align='left',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                            p.text(u"+主营业收入\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.mainIncome)
                            p.text(u"+其他业务收入\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.otherIncome)
                            p.text(u"=净销售\t\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.netIncome)
                            p.text(u"+折扣\t\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.discount)
                            p.text(u"+进位差\t\t\t\t\t0\n".encode('gbk') )
                            p.text(u"=应收现金\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.netIncome)
                            p.text("----------------------------------------------")
                            p.set(align='center',font='B',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                            p.text(u"\n\t合计部门报表\n".encode('gbk'))
                            MyClientProtocol.allPay = changeTabledict.get('allPay')
                            for allpay in MyClientProtocol.allPay:
                                payName = json.dumps(allpay.get('payName'),encoding='UTF-8',ensure_ascii=False)
                                payNamefull = payName.replace("\"","") 
                                countOrderNum = allpay.get('countOrderNum')
                                totalAmount = allpay.get('totalAmount')
                                p.set(align='left',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                                p.text(u"%s\t\t%s\t\t\t%s\n".encode('gbk') % (payNamefull,countOrderNum,totalAmount))
                            MyClientProtocol.otherStatistics = changeTabledict.get('otherStatistics')
                            p.text("----------------------------------------------")
                            p.set(align='center',font='B',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                            p.text(u"\n\t其他统计\n".encode('gbk'))
                            for otherstatistics in MyClientProtocol.otherStatistics: 
                                kindName = json.dumps(otherstatistics.get('kindName'),encoding='UTF-8',ensure_ascii=False)
                                kindNamefull = kindName.replace("\"","")
                                Number = otherstatistics.get('Number')
                                totalAmountO = otherstatistics.get('totalAmount')
                                p.set(align='left',font='a',text_type='normal',height=1,width=1,invert=False, smooth=False,flip=False)
                                p.text(u"%s\t\t\t\t\r%s\n".encode('gbk') % (kindNamefull,totalAmountO))
                            p.cut()
                            #p.cashdraw(2)  #get the message = 0 ? openmoneybox
                        except Exception as e:
                                print (e)
                    shield()

            if dict.get('orderType') == 0:  #ordertype 0 push printer ? 4 changetable  and openmoneybox
                try:
                    #cash drawer
                    Big = dict.get('data')
                    if Big == '':
                        p = Usb(0x04b8,0x0e0f)
                        p.cashdraw(2)
                    else:
                            Bigstr = str(Big)
                            #print Bigstr
                            Bigdict = eval(Bigstr)
                            #print Bigdict
                            #print Bigdict #if not data ? print dict.get('data') : true
                            title = json.dumps(Bigdict.get('title'),encoding='UTF-8',ensure_ascii=False)
                            MyClientProtocol.titlefull = title.replace("\"","") 
                            #print titlefull
                            MyClientProtocol.orderId = Bigdict.get('orderId') #取餐号
                            #print orderId
                            MyClientProtocol.machineId = Bigdict.get('machineId') #机号
                            #print type(machineId)
                            MyClientProtocol.cashier = Bigdict.get('cashier') #收银员
                            #print type(cashier)
                            MyClientProtocol.orderTime = Bigdict.get('orderTime') #下单时间
                            #print orderTime
                            kindchagne =  json.dumps(Bigdict.get('kind'),encoding='UTF-8',ensure_ascii=False)
                            #print kindchagne
                            MyClientProtocol.kind = kindchagne.replace("\"","") #堂食/外卖
                            #print kindfull
                            storeAddr = Bigdict.get('storeAddr') 
                            #print storeAddr
                            storeAddrchagne =  json.dumps(Bigdict.get('storeAddr'),encoding='UTF-8',ensure_ascii=False)
                            MyClientProtocol.storeAddrfull = storeAddrchagne.replace("\"","") #餐厅地址
                            MyClientProtocol.payType = Bigdict.get('payType') #支付类型：现金,支付宝,微信,会员卡
                            total = Bigdict.get('total') #需要支付的总金额
                            MyClientProtocol.total2 = total.replace("\"","")
                            #print total2
                            MyClientProtocol.discount = Bigdict.get('discount') #优惠金额
                            #discount2 = discount.replace("\"","")
                            payCashNumber = Bigdict.get('payCashNumber')#支付的现金数量
                            MyClientProtocol.payCashNumber2 = payCashNumber.replace("\"","")
                            #print payCashNumber2
                            MyClientProtocol.card_id = Bigdict.get('card_id') #会员卡卡号
                            MyClientProtocol.card_balance = Bigdict.get('card_balance') # 会员卡余额
                            MyClientProtocol.card_getIntegral = Bigdict.get('card_getIntegral') #本次获得积分
                            MyClientProtocol.card_totalIntegral = Bigdict.get('card_totalIntegral') #可用积分 （即总积分）
                            payTransactionNumber = Bigdict.get('payTransactionNumber') #支付交易号（针对微信，支付宝）
                            storename =  json.dumps(Bigdict.get('storename'),encoding='UTF-8',ensure_ascii=False)
                            MyClientProtocol.storenamefull = storename.replace("\"","") #餐厅名称
                            MyClientProtocol.storeNum = Bigdict.get('storeNum') #餐厅电话
                            footer =  json.dumps(Bigdict.get('footer'),encoding='UTF-8',ensure_ascii=False)
                            MyClientProtocol.footerfull = footer.replace("\"","") #结束语

                            def spear():
                                    p = Usb(0x04b8,0x0e0f)
                                    #p.cashdraw(2)
                                    p.set(align='center',font='B',text_type='normal',height=1,width=2,invert=False, smooth=False,flip=False)
                                    p.text(u'%s\n\n'.encode('gbk') % MyClientProtocol.titlefull)
                                    p.set(align='left',font='a',text_type='normal',height=1,width=1)
                                    p.text(u"地址: [%s]\n".encode('gbk') % MyClientProtocol.storeAddrfull)
                                    p.text(u"收银员: [%s]\t\t\t".encode('gbk') % MyClientProtocol.cashier)
                                    p.text(u"机号: [%s]\n".encode('gbk') % MyClientProtocol.machineId)
                                    p.text(u"打单时间: [%s]\n\n".encode('gbk') % MyClientProtocol.orderTime)
                                    p.set(align='center',font='B',text_type='B',height=2,width=2,invert=False, smooth=False,flip=False)
                                    p.text(u"取餐号: [%s]\n\n".encode('gbk') % MyClientProtocol.orderId )
                                    p.set(align='center',font='a',text_type='normal',height=1,width=1)
                                    p.text(u'%s\n'.encode('gbk') % MyClientProtocol.kind)
                                    p.set(align='left',font='a',text_type='normal',height=1,width=1)
                                    p.text(u"数量\t产品名称\t\t\t金额\n".encode('gbk'))
                                    MyClientProtocol.prodList = Bigdict.get('prodList') #菜品信息
                                    #print prodList
                                    for prodListdict in MyClientProtocol.prodList:
                                            #print prodListdict
                                            #print type(prodListdict)
                                            foodnum = prodListdict.get('num')
                                            foodnamechagne =  json.dumps(prodListdict.get('name'),encoding='UTF-8',ensure_ascii=False)
                                            foodname = foodnamechagne.replace("\"","")
                                            foodsum = prodListdict.get('sum')
                                            #foodsum2 = ("%.2f" % foodsum)
                                            #输出数量,产品,金额
                                            p.text(u"%s\t\r%s\t\t\t\r%s\n".encode('gbk') % (foodnum,foodname,foodsum))
                                    p.text(u"\n总\t价:\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.total2 )
                                    p.text(u"优\t惠:\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.discount )
                                    p.text(u"应\t收:\t\t\t\t%s\n".encode('gbk') % MyClientProtocol.payCashNumber2)
                                    p.text(u"找\t零:\t\t\t\t0.00\n".encode('gbk') )
                                    p.set(align='center',font='a',text_type='normal',height=1,width=2)
                                    p.text(u'%s\n\n'.encode('gbk') % MyClientProtocol.footerfull)
                                    p.text(u'扫描二维码加入真功夫会员，每消费\n一元累计1积分，积分可兑换美食和\n体验，扫描时请保持小票平整！\n'.encode('gbk') )
                                    p.image("/usr/local/proxy/printer/tx.png")
                                    p.cut()
                            spear()

                except Exception as e:
                    print ("connect printerFPOS %s") % (e)  
                    print ("please look at the bus about printerFPOS alive")
                      

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('gbk')
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)
    factory = WebSocketClientFactory(u"ws://172.17.8.2:8080/websocketServer")
    factory.protocol = MyClientProtocol
    reactor.connectTCP("172.17.8.2", 8080, factory)
    reactor.run()

