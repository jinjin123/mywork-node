#!/usr/local/bin/python4
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from myoa_approval_api import *
import json
import copy
from mysql_exec_sql_api import *
import traceback
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from Weixin import *
from itertools import chain
# import datetime
import time
from operator import itemgetter
sys.path.append('/data/scripts/devops/selfdos/config')
from api_config import myoa_api_url, myoa_api_appid, myoa_api_apptoken, myoa_callback_url, myoa_category_code, \
	    landun_api_url_app_pub_retry, landun_api_token, landun_rebuild_url, wechatid
if __name__ == "__main__":
    Log = LogOut()
    if len(sys.argv) > 1:
        timeout = 30
        global s
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[403, 429, 500, 502, 503, 504],
                                                         method_whitelist=frozenset(['GET', 'POST']))))
        timestr = str(int(time.time()))
        # sn = MyOaSign("demo", "myoatoken").SignToken()
        sn = MyOaSign(myoa_api_appid, myoa_api_apptoken).SignToken()
        print("auth: %s" % str(sn))
        Log.info("auth sign: '{}'".format(sn))
        global kwargs
	        kwargs = {
            "headers": {"signature": sn, "timestamp": timestr, "Content-Type": "application/json"},
            "work_items": []
        }
      Log.info("input params argv 1: '{}'".format(str(sys.argv[1])))
      # print(json.loads((sys.argv[1]).replace('\\', '\\\\'), strict=False))
      global data
      data = json.loads((sys.argv[1]).replace('\\', '\\\\'), strict=False)
      tmp = {
          "category": "C23D7091B98844659D128773209BBF85",
          "handler": data["handler"],
          "title": data["title"],
          "process_name": data["process_name"],
          "process_inst_id": data["process_inst_id"],
          "activity": "Default",
          "applicant": data["applicant"],
          "callback_url": myoa_callback_url,
          "detail_view": data["detail_view"],
          "data": data["data"],
          "approval_history": [],
          "actions": [
              {
                  "display_name": "同意",
                  "value": "1"
              },
              {
	                    "display_name": "驳回",
	                    "value": "2"
              },
              {
                  "display_name": "待定",
                  "value": "3"
              }
          ]

         }

      sql = "select status,leader_approval_status,test_approval_status,db_approval_status,operate_approval_status" \
            " from sys_app_publish_log where id ={};".format(data["process_inst_id"])
      Log.info("create order of status: '{}'".format(sql))
      res = exec_mysql().select(sql)
      resd = list(chain.from_iterable(res))
      print(resd)
      Log.info(
          "approval status code [status,leader_approval_status,test_approval_status,db_approval_status,operate_approval_status]: '{}'".format(
              resd))
      for x in data["data"]:
          if x["value"][0] == "leader":
              if resd[0] == 1 and (resd[1] == 0 or resd[1] is None):
                  Log.info("#####Create leader order #######")
              else:
                  Log.info("#####leader approval pass #######")
                  sys.exit(0)
          elif x["value"][0] == "test":
              if resd[0] == 1 and (resd[2] == 0 or resd[2] is None):
                  Log.info("#####Create test order #######")
              else:
                  Log.info("#####test approval pass #######")
                  sys.exit(0)
          elif x["value"][0] == "db":
              if resd[0] == 1 and (resd[3] == 0 or resd[3] is None):
                  Log.info("#####Create db order #######")

              else:
                  Log.info("#####db approval pass #######")
                  sys.exit(0)
          elif x["value"][0] == "ops":
              if resd[0] == 1 and (resd[4] == 0 or resd[4] is None):
                  Log.info("#####Create ops order #######")

              else:
                  Log.info("#####ops approval pass #######")
                  sys.exit(0)
          else:
              Log.info("unkown user approval pass")
              sys.exit(1)

      h_sql = "select test_approval_user,test_approval_result,test_approval_status,test_approval_time," \
              "operate_approval_user,ops_approval_result,operate_approval_status,operate_approval_time," \
              "db_approval_user,db_approval_result,db_approval_status,db_approval_time," \
              "leader_approval_user,leader_approval_result,leader_approval_status,leader_approval_time from sys_app_publish_log where id ={};".format(
          data["process_inst_id"])
      keys = ["test_approval_user", "test_approval_result", "test_approval_status", "test_update_time",
              "operate_approval_user", "ops_approval_result", "operate_approval_status", "op_update_time",
              "db_approval_user",
              "db_approval_result", "db_approval_status", "db_update_time", "leader_approval_user",
              "leader_approval_result", "leader_approval_status", "ld_update_time"]
      r = exec_mysql().select(h_sql)
      resd = list(chain.from_iterable(r))
      tmpColumnArr = []
      tmpValueArr = []
      for b in range(0, len(keys), 4):
          tmpColumnArr.append(keys[b:b + 4])
      for i in range(0, len(resd), 4):
          tmpValueArr.append(resd[i:i + 4])

      mapping = map(list, zip(tmpColumnArr, tmpValueArr))
      newData = {}
      newTmpArr = []
      for x in mapping:
          tmpdata = dict(zip(*x))
          if tmpdata.get("test_approval_result", None):
              newData["approver"] = tmpdata["test_approval_user"]
              newData["opinion"] = tmpdata["test_approval_result"]
              newData["step"] = "测试审批"
              newData["action"] = "驳回" if tmpdata["test_approval_status"] == 1 else "通过"
              newData["approval_time"] = (tmpdata["test_update_time"].strftime('%Y-%m-%dT%H:%M:%S.%f'))[:-5]
              newTmpArr.append(copy.deepcopy(newData))
          elif tmpdata.get("operate_approval_result", None):
              newData["step"] = "运维审批"
              newData["approver"] = tmpdata["operate_approval_user"]
              newData["opinion"] = tmpdata["ops_approval_result"]
              newData["action"] = "驳回" if tmpdata["operate_approval_status"] == 1 else "通过"
              newData["approval_time"] = (tmpdata["op_update_time"].strftime('%Y-%m-%dT%H:%M:%S.%f'))[:-5]
              newTmpArr.append(copy.deepcopy(newData))
          elif tmpdata.get("db_approval_result", None):
              newData["step"] = "DB审批"
              newData["approver"] = tmpdata["db_approval_user"]
              newData["opinion"] = tmpdata["db_approval_result"]
              newData["action"] = "驳回" if tmpdata["db_approval_status"] == 1 else "通过"
              newData["approval_time"] = (tmpdata["db_update_time"].strftime('%Y-%m-%dT%H:%M:%S.%f'))[:-5]
              newTmpArr.append(copy.deepcopy(newData))
          elif tmpdata.get("leader_approval_result", None):
              newData["step"] = "Leader审批"
              newData["approver"] = tmpdata["leader_approval_user"]
              newData["opinion"] = tmpdata["leader_approval_result"]
              newData["action"] = "驳回" if tmpdata["leader_approval_status"] == 1 else "通过"
              newData["approval_time"] = (tmpdata["ld_update_time"].strftime('%Y-%m-%dT%H:%M:%S.%f'))[:-5]
              newTmpArr.append(copy.deepcopy(newData))
          else:

              pass

      Log.info("approval hisotry: '{}'".format(newTmpArr))
      try:
          if data["handler"].find(";") != -1:
              outhsernum = len(data["handler"].split(";"))
              outhserlist = data["handler"].split(";")
              for x in range(outhsernum):
                  # tmp = {}
                  tmp["applicant"] = data["applicant"]
                  tmp["handler"] = outhserlist[x]
                  tmp["title"] = data["title"]
                  tmp["process_name"] = data["process_name"]
                  tmp["process_inst_id"] = data["process_inst_id"]
                  tmp["detail_view"] = data["detail_view"]
                  tmp["approval_history"] = sorted(newTmpArr, key=itemgetter('approval_time'))
                  tmp["data"] = data["data"]
                  kwargs["work_items"].append(copy.deepcopy(tmp))

              # Log.info("create order params: '{}'".format(json.dumps(kwargs)))
              Log.info("resolve params ok, if error check myoa api")
              testlog = RESTfulApiRequestAgent().create(**kwargs)
              Log.info("create order back Resphonse: '{}'".format(testlog))
              if "200" not in testlog:
                  sql = "select task_id from sys_app_publish_log where id ={} limit 1;".format(
                      data["process_inst_id"])
                  Log.info("get pipline build sql '{}'".format(sql))
                  res = exec_mysql().select(sql)
                  resd = list(chain.from_iterable(res))
                  Log.info("get pipline build sql result '{}'".format(resd))
                  Log.info("### REBUILD PIPLINE######")
                  retry_bk_url = landun_api_url_app_pub_retry.format(resd[0], landun_api_token)
                  # msg = "流水线推送Myoa审批单异常,开始rebuild-id-{},URL为:\n[{}]({})\n<@v_peijwu><@v_minmmlin>".format(data["process_inst_id"],landun_rebuild_url.format("b-37ad4af998614ae1aa9b1506289be54b"),landun_rebuild_url.format("b-37ad4af998614ae1aa9b1506289be54b"))
                  msg = "流水线推送Myoa审批单异常,开始rebuild-id-{},URL为:\n[{}]({})\n<@v_peijwu><@v_minmmlin>".format(
                      data["process_inst_id"], landun_rebuild_url.format(resd[0]), landun_rebuild_url.format(resd[0]))
                  a = Weixin(msgType="markdown", cid=wechatid, tbody=msg).PushMarkMsg()
                  Log.info("Wechat send rebuld msg'{}'".format(a))
                  # retry_bk_url = landun_api_url_app_pub_retry.format("b-37ad4af998614ae1aa9b1506289be54b", landun_api_token)
                  Log.info("rebuild url '{}'".format(retry_bk_url))
                  try:
                      res = s.post(url=retry_bk_url, timeout=timeout).json()
                      Log.info("rebuild back '{}'".format(res["status"]))
                      Log.info("### REBUILD PIPLINE done######")
                  except Exception as e:
                      Log.info("REBUILD ERROR '{}'".format(e))

          else:
              # tmp = {}
              tmp["applicant"] = data["applicant"]
              tmp["handler"] = data["handler"]
              tmp["title"] = data["title"]
              tmp["process_name"] = data["process_name"]
              tmp["process_inst_id"] = data["process_inst_id"]
              tmp["detail_view"] = data["detail_view"]
              tmp["data"] = data["data"]
              tmp["approval_history"] = sorted(newTmpArr, key=itemgetter('approval_time'))
              kwargs["work_items"].append(copy.deepcopy(tmp))
              # Log.info("create order params: '{}'".format(json.dumps(kwargs)))
              Log.info("resolve params ok, if error check myoa api")
              # print(json.dumps(kwargs))
              testlog = RESTfulApiRequestAgent().create(**kwargs)
              Log.info("create order back Resphonse: '{}'".format(testlog))
              if "200" not in testlog:
                  sql = "select task_id from sys_app_publish_log where id ={} limit 1;".format(
                      data["process_inst_id"])
                  Log.info("get pipline build sql '{}'".format(sql))
                  res = exec_mysql().select(sql)
                  resd = list(chain.from_iterable(res))
                  Log.info("get pipline build sql result '{}'".format(resd))
                  Log.info("### REBUILD PIPLINE######")
                  retry_bk_url = landun_api_url_app_pub_retry.format(resd[0], landun_api_token)
	                    # msg = "流水线推送Myoa审批单异常,开始rebuild-id-{},URL为:\n[{}]({})".format(data["process_inst_id"],landun_rebuild_url.format("b-37ad4af998614ae1aa9b1506289be54b"),landun_rebuild_url.format("b-37ad4af998614ae1aa9b1506289be54b"))
	                    msg = "流水线推送Myoa审批单异常,开始rebuild-id-{},URL为:\n[{}]({})\n<@v_peijwu><@v_minmmlin>".format(
                        data["process_inst_id"], landun_rebuild_url.format(resd[0]), landun_rebuild_url.format(resd[0]))
	                    a = Weixin(msgType="markdown", cid=wechatid, tbody=msg).PushMarkMsg()
	                    Log.info("Wechat send rebuld msg'{}'".format(a))
	                    # retry_bk_url = landun_api_url_app_pub_retry.format("b-37ad4af998614ae1aa9b1506289be54b", landun_api_token)
                 Log.info("rebuild url '{}'".format(retry_bk_url))
                 try:
                     res = s.post(url=retry_bk_url, timeout=timeout).json()
                     Log.info("rebuild back '{}'".format(res["status"]))
                     Log.info("### REBUILD PIPLINE done######")
                 except Exception as e:
                     Log.info("REBUILD ERROR '{}'".format(e))
      except Exception as e:
             Log.error("Request Unknown Error wait 15s to retry: '{}'".format(e))
             sql = "select task_id from sys_app_publish_log where id ={} limit 1;".format(data["process_inst_id"])
             Log.info("get pipline build sql '{}'".format(sql))
             res = exec_mysql().select(sql)
             resd = list(chain.from_iterable(res))
             Log.info("get pipline build sql result '{}'".format(resd))
             Log.info("### REBUILD PIPLINE 283######")
             retry_bk_url = landun_api_url_app_pub_retry.format(resd[0], landun_api_token)
             msg = "流水线推送Myoa审批单异常,开始rebuild-id-{},URL为:\n[{}]({})\n<@v_peijwu><@v_minmmlin>".format(
                 data["process_inst_id"], landun_rebuild_url.format(resd[0]), landun_rebuild_url.format(resd[0]))
             # msg = "流水线推送Myoa审批单异常,开始rebuild-id-{},URL为:\n[{}]({})".format(data["process_inst_id"],landun_rebuild_url.format("b-37ad4af998614ae1aa9b1506289be54b"),landun_rebuild_url.format("b-37ad4af998614ae1aa9b1506289be54b"))
             a = Weixin(msgType="markdown", cid=wechatid, tbody=msg).PushMarkMsg()
             Log.info("Wechat send rebuld msg'{}'".format(a))
             Log.info("rebuild url '{}'".format(retry_bk_url))
             try:
                 res = s.post(url=retry_bk_url, timeout=timeout).json()
                 Log.info("rebuild back '{}'".format(res["status"]))
                 Log.info("### REBUILD PIPLINE done 293######")
             except Exception as e:
                 Log.info("######REBUILD ERROR###### '{}'".format(e))

             sys.exit(1)
 else:
     print("miss arguments")
     print("finalstate:ERROR")
     sys.exit(1)

 


