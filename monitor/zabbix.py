# -*- coding: UTF-8 -*-
import json,urllib2,sys
from urllib2 import URLError

class ZabbixAPI:
	def __init__(self,address,username,password): 
		self.address = address 
		self.username = username 
		self.password = password 
		self.url = '%s/api_jsonrpc.php' % self.address 
		self.header = {"Content-Type":"application/json"} 

	def user_login(self): 
		data = json.dumps({ 
		"jsonrpc": "2.0", 
		"method": "user.login", 
		"params": { 
		"user": self.username, 
		"password": self.password 
		}, 
		"id": 0
		}) 
		request = urllib2.Request(self.url, data) 
		for key in self.header: 
			request.add_header(key, self.header[key]) 
		try: 
			result = urllib2.urlopen(request) 
		except URLError as e: 
			print "Auth Failed, please Check your name and password:", e.code 
		else: 
			response = json.loads(result.read()) 
			result.close() 
			self.authID = response['result'] 
			return self.authID 

	def trigger_get(self): 
		res = []
		data = json.dumps({ 
		"jsonrpc":"2.0", 
		"method":"trigger.get", 
		"params": { 
		"output": [ 
		"triggerid", 
		"description", 
		"priority"
		], 
		"filter": { 
		"value": 1
		}, 
		"expandData":"hostname", 
		"sortfield": "priority", 
		"sortorder": "DESC"
		}, 
		"auth": self.user_login(), 
		"id":1 
		})
		request = urllib2.Request(self.url, data) 
		for key in self.header: 
			request.add_header(key, self.header[key]) 
		try: 
			result = urllib2.urlopen(request) 
		except URLError as e: 
			print "Error as ", e 
		else: 
			response = json.loads(result.read()) 
			result.close() 
			issues = response['result'] 
			content = ''
			total = 0
			if issues: 
				for line in issues: 
					fdata = {'host':line['host'].encode("utf-8"),
					'description':line['description'].encode("utf-8")}
					res.append(fdata)
				total = len(res)
			content = json.dumps({"total":total,"rows":res})
			return content

if __name__ == "__main__": 
	address='http://118.194.44.45/zabbix'
	username='admin'
	password='JIANKEcomcn'
	zabbixapi = ZabbixAPI(address=address, username=username, password=password) 
	content = zabbixapi.trigger_get()
	print content