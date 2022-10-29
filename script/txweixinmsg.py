#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import requests
import sys
import json
from requests_toolbelt import MultipartEncoder
sys.path.append('/xxxx/conf')
from k8s_cluster_config_dic import *
from loger import LogOut
import datetime
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
class Weixin:
    timeout = 30
    global s
    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[400,403, 429, 500, 502, 503, 504],method_whitelist=frozenset(['GET', 'POST']))))
    MsgTypeMap = {
        "markdown": {
            "chatid":"",
            "msgtype": "markdown",
            "markdown": {
                "content": "xx"
            },
        },
        "text": {
            "chatid":"",
            "msgtype": "text",
            "text": {
                "content": "hello world",
                "mentioned_list": ["wangqing", "@all"],
            }
        },
        "image": {
            "chatid":"",
            "msgtype": "image",
            "image": {
                "base64": "DATA",
                "md5": "MD5"
            }
        },
        "news": {
            "chatid":"",
            "msgtype": "news",
            "articles": [
                {
                    "title": "中秋节礼品领取",
                    "description": "今年中秋节公司有豪礼相送",
                    "url": "www.qq.com",
                    "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                }
            ]
        },
        "file": {
            "chatid":"",
            "msgtype": "file",
            "file": {
                "media_id": "3a8asd892asd8asd"
            }
        }
    }
    PProxy = {"https": "https://1.1.1.1:8088"}
    def __init__(self, fpath=None, msgType=None,cid=None,tbody=None,exinfo=None,newsBody=None,ImgBody=None,UserBody=None):
        self.Url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/"
        self.fileUrl = fpath
        self.logger = LogOut()
        self.logger.logfile = "/data/logs/ittool/28_clb_manager/wechatpush.log"
        self.msg_type = msgType
        self.chat_id = cid
        self.content = tbody
        self.extra = exinfo
        self.newsParams = newsBody
        self.imgData = ImgBody
        self.toUser = UserBody ## list of str

	
    def uploadFileMediaId(self):
        data = MultipartEncoder({
            "filename": (self.fileUrl, open(self.fileUrl, 'rb'), 'application/octet-stream'),
        })
        try:
            #res = requests.post(url=self.Url+"upload_media?key=a52abe90-e93e-4a18-93b0-e33a78872f06&type=file", data=data, headers={'Content-Type': data.content_type},proxies=self.PProxy)
            res = s.post(url=self.Url+"upload_media?key=a52abe90-e93e-4a18-93b0-e33a78872f06&type=file", data=data, headers={'Content-Type': data.content_type},proxies=self.PProxy)
            if (res.json()).get("media_id"):
                return (res.json())["media_id"]

        except Exception as e:
               self.logger.error("Upload WX File Err: '{}'".format(str(e)))

    def PushMediaMsg(self):
        mid = self.uploadFileMediaId()
        data = self.MsgTypeMap[self.msg_type]
        data["chatid"] = self.chat_id
        data["file"]["media_id"] = mid
        if self.msg_type == "file" and self.content is not None:
            self.msg_type = "markdown"
            #self.PushTextMsg()
            self.PushMarkMsg()
        try:
            #res = requests.post(url=self.Url+"send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),headers={'Content-Type': 'application/json'},proxies=self.PProxy)
            res = s.post(url=self.Url+"send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),headers={'Content-Type': 'application/json'},proxies=self.PProxy)
            # print(res.json())
            return res.json()
        except Exception as e:
            self.logger.error("Send WX msg Err: '{}'".format(str(e)))
	
    def PushTextMsg(self):
        data = self.MsgTypeMap[self.msg_type]
        data["chatid"] = self.chat_id
        data["msgtype"] = self.msg_type
        data["text"]["content"] = self.content
        data["text"]["mentioned_list"] = self.toUser
        try:
            #res = requests.post(url=self.Url + "send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),
            res = s.post(url=self.Url + "send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),
                            headers={'Content-Type': 'application/json'},proxies=self.PProxy)
            return res.json()
        except Exception as e:
            self.logger.error("Send WX msg Err: '{}'".format(str(e)))

    def PushMarkMsg(self):
        data = self.MsgTypeMap[self.msg_type]
        data["chatid"] = self.chat_id
        data["msgtype"] = self.msg_type
        data["markdown"]["content"] =  self.content
        try:
            #res = requests.post(url=self.Url + "send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),
            res = s.post(url=self.Url + "send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),
                            headers={'Content-Type': 'application/json'},proxies=self.PProxy)
            return res.json()
        except Exception as e:
            self.logger.error("Send WX msg Err: '{}'".format(str(e)))
	
    def PushNewsMsg(self):
        newsParmas = self.newsParams
        tmp=[]
        tmp.append(newsParmas)
        data = self.MsgTypeMap[self.msg_type]
        data["chatid"] = self.chat_id
        data["msgtype"] = self.msg_type
        data["markdown"]["articles"] = tmp
        try:
            res = requests.post(url=self.Url + "send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),
                            headers={'Content-Type': 'application/json'})
            return res.json()
        except Exception as e:
            self.logger.error("Send WX msg Err: '{}'".format(str(e)))

    def PushImagMsg(self):
        data = self.MsgTypeMap[self.msg_type]
        data["chatid"] = self.chat_id
        data["msgtype"] = self.msg_type
        data["image"] = self.imgData
        try:
            res = requests.post(url=self.Url + "send?key=a52abe90-e93e-4a18-93b0-e33a78872f06", data=json.dumps(data),
                           headers={'Content-Type': 'application/json'})
            return res.json()
        except Exception as e:
            self.logger.error("Send WX msg Err: '{}'".format(str(e)))
