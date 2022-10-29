#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json, sys, re
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.clb.v20180317 import clb_client, models
from threading import Thread
import queue
import time
from logmodule.loger import LogOut
appgroup_list = "ap;fdw;erp;ar;ggzc;glyy;dos;ubuy"
from k8s_cluster_config_dic import *
ThreadNum = 2
class SignCloudKey:
    def __init__(self, area):
        self._arealias = area
        self._id = eval(area_k8s_accesskey_dic[self._arealias])["id"]
        self._key = eval(area_k8s_accesskey_dic[self._arealias])["key"]
        self._sn = credential.Credential(self._id, self._key)
        self._area = area_code_dic[self._arealias]
        self._lbOffsetParamsQ = queue.Queue()
        self._lbList = []
        self._instance = None
        self.logger = LogOut()

    def HttpInstance(self):
        httpProfile = HttpProfile()
        httpProfile.endpoint = "clb.internal.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self._instance = clb_client.ClbClient(self._sn, self._area, clientProfile)
        return self._instance
	
class RequestAgent(SignCloudKey):
    def RequestTotalLoadBlanceOffsetParams(self, offset, limit):
        try:
            endTags = True
            req_instance = self.HttpInstance()
            req = models.DescribeLoadBalancersRequest()
            ##
            params = {
                "Offset": offset,
                "Limit": limit
            }
            req.from_json_string(json.dumps(params))
            resp = req_instance.DescribeLoadBalancers(req)
            ##result
            resp_json = json.loads(resp.to_json_string())
            while endTags:
                if int(offset) + limit < resp_json['TotalCount']:
                    self._lbOffsetParamsQ.put({"Offset": offset, "Limit": limit})
                    offset = int(offset) + limit
                else:
                    self._lbOffsetParamsQ.put({"Offset": offset, "Limit": limit})
                    endTags = False
	            # total dict
	            # print(json.dumps(resp_json))
        except Exception as e:
            self.logger.error("Queue Put Err: '{}'".format(str(e)))
            print(e)
	
    def __call__(self, offset, limit):
        ths = []
        t = Thread(target=self.RequestTotalLoadBlanceOffsetParams, args=(offset, limit))
        t.start()
        ths.append(t)
        for th in ths:
            th.join()
        return self._lbOffsetParamsQ
	
class RequestLoadBlanceObj(SignCloudKey):
    def Lb_Obj(self, _lbOffsetParamsQ):
        test_dev_uat = ""
        while _lbOffsetParamsQ.empty() == False:
            params = _lbOffsetParamsQ.get()
            try:
                req_instance = self.HttpInstance()
                req = models.DescribeLoadBalancersRequest()
                req.from_json_string(json.dumps(params))
                resp = req_instance.DescribeLoadBalancers(req)
                resp_json = json.loads(resp.to_json_string())
                if resp_json.get("LoadBalancerSet", None):
                    if len(resp_json["LoadBalancerSet"]) > 0:
                        data_json = resp_json["LoadBalancerSet"]
                        for obj in data_json:
                            # self._lbList.append(obj)
                            clb_id = obj['LoadBalancerId']
                            clb_name = obj['LoadBalancerName']
                            appgroup_name = ""
                            if "s2-" + self._area in clb_name and "_" in clb_name:
                                temp = clb_name.split('_')[1]
                                temp = temp.replace("-test", "").replace("test-", "")
                                appgroup_name = "{}_group".format(temp.split('-')[-1])
                            else:
                                for m in appgroup_list.split(';'):
                                    if m in re.split("[-_]", (json.dumps(clb_name))):
                                        appgroup_name = "{}_group".format(m)
                                        break
                            if appgroup_name == "":
                                appgroup_name = "yw_group"
	                        clb_name_lower = clb_name.lower()
                            if "-test" in clb_name_lower or "_test" in clb_name_lower or "test-" in clb_name_lower or "test_" in clb_name_lower or "-dev" in clb_name_lower or "_dev" in clb_name_lower or "dev-" in clb_name_lower or "dev_" in clb_name_lower or "-uat" in clb_name_lower or "_uat" in clb_name_lower or "uat-" in clb_name_lower or "uat_" in clb_name_lower:
                                test_dev_uat += "{}||{}\n".format(clb_name, clb_id)
                                continue
	                    # print(clb_id)
                            self._lbList.extend(self.get_listener(clb_id, appgroup_name, clb_name))
                            self.logger.info("LBList:'{}'".format(self._lbList))
                            # print(json.dumps(result))
                            # print(len(result))
                            # time.sleep(4)
                            # self._lbList.append({"id":obj["LoadBalancerId"],"name":obj["LoadBalancerName"]})
	
	                # print("Get: {}".format(params))
            except Exception as e:
                self.logger.error("Get LB_obj error:'{}', params:'{}'".format(str(e),str(params)))
                print("Get LB_obj error:{}, params:{}".format(e, params))
                _lbOffsetParamsQ.put(params)
                #time.sleep(3)
            finally:
                _lbOffsetParamsQ.task_done()
	
     def get_listener(self, clb_id, appgroup_name, clb_name):
        Total = []
        try:
            # data_content = ""
            req_instance = self.HttpInstance()
            self.logger.info("Get Listener instance:'{}'".format(req_instance))
            params = {
                "LoadBalancerIds": [clb_id]
            }
            req = models.DescribeTargetHealthRequest()
            req.from_json_string(json.dumps(params))
            resp = req_instance.DescribeTargetHealth(req)
            result_json = json.loads(resp.to_json_string())
            if result_json.get("LoadBalancers"):
                if len(result_json["LoadBalancers"]) > 0:
                    # print(json.dumps(result_json))
                    data_json = result_json['LoadBalancers']
                    for obj in data_json:
                        data_content = {}
                        if obj.get("Listeners", None):
                            listeners = obj["Listeners"]
                            for line in listeners:
                                listen_id = line['ListenerId']
                                listen_name = line['ListenerName']
                                if 'Rules' not in line:
                                    data_content = {
                                        "APPGROUP": appgroup_name,
                                        "LOADBALANCERNAME": clb_name,
                                        "LOADBALANCEID": clb_id,
                                        "LISTENERID": listen_id,
                                        "LISTENNAME": listen_name,
                                        "Domain": listen_name,
                                        "Url": "/",
                                        "HealthStatus": "NULL",
                                        "LocationId": "NULL",
                                        "IP": "NULL",
                                        "Port": "NULL",
                                        "TargetId": "NULL",
                                        "HealthStatusDetial": "NULL",
                                        "Weight": "NULL",
                                        "Instance": "NULL"
                                    }
                                    Total.append(data_content)
                                    # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
                                    #     appgroup_name, clb_name, clb_id, listen_id,listen_name, "NULL", "NULL", "NULL", "NULL",
                                    #     "NULL",
                                    #     "NULL", "NULL", "NULL")
                                    break
                                listen_rules = line['Rules']
                                if not listen_rules and listen_rules is None:
                                    data_content = {
                                        "APPGROUP": appgroup_name,
                                        "LOADBALANCERNAME": clb_name,
                                        "LOADBALANCEID": clb_id,
                                        "LISTENERID": listen_id,
                                        "LISTENNAME": listen_name,
                                        "Domain": listen_name,
                                        "Url": "/",
                                        "LocationId": "NULL",
                                        "HealthStatus": "NULL",
                                        "IP": "NULL",
                                        "Port": "NULL",
                                        "TargetId": "NULL",
                                        "HealthStatusDetial": "NULL",
                                        "Weight": "NULL",
                                        "Instance": "NULL"
                                    }
                                    Total.append(data_content)
                                    # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
                                    #     appgroup_name, clb_name, clb_id, listen_id,listen_name, "NULL", "NULL", "NULL", "NULL",
                                    #     "NULL",
                                    #     "NULL", "NULL", "NULL")
                                    break
                                for i in listen_rules:
                                    if ('Url' not in i) and ('Domain' not in i):
                                        # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
                                        #     appgroup_name, clb_name, clb_id, listen_id,listen_name, "NULL", "NULL", "NULL", "NULL",
                                        #     "NULL", "NULL", "NULL", "NULL")
                                        data_content = {
                                            "APPGROUP": appgroup_name,
                                            "LOADBALANCERNAME": clb_name,
                                            "LOADBALANCEID": clb_id,
                                            "LISTENERID": listen_id,
                                            "LISTENRNAME": listen_name,
                                            "Domain": listen_name,
                                            "Url": '/',
                                            "LocationId": "NULL",
                                            "HealthStatus": "NULL",
                                            "IP": "NULL",
                                            "Port": "NULL",
                                            "TargetId": "NULL",
                                            "HealthStatusDetial": "NULL",
                                            "Weight": "NULL",
                                            "Instance": "NULL"
                                        }
                                        Total.append(data_content)
                                        break
                                    url = i['Url']
                                    domain = i['Domain']
                                    LocationId = i['LocationId']
                                    if 'Targets' not in i:
                                        data_content = {
                                            "APPGROUP": appgroup_name,
                                            "LOADBALANCERNAME": clb_name,
                                            "LOADBALANCEID": clb_id,
                                            "LISTENERID": listen_id,
                                            "LISTENRNAME": listen_name,
                                            "Domain": domain if domain else listen_name,
                                            "Url": url if url else '/',
                                            "LocationId": LocationId,
                                            "HealthStatus": "NULL",
                                            "IP": "NULL",
                                            "Port": "NULL",
                                            "TargetId": "NULL",
                                            "HealthStatusDetial": "NULL",
                                            "Weight": "NULL",
                                            "Instance": "NULL"
                                        }
                                        Total.append(data_content)
                                        # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
                                        #     appgroup_name, clb_name, clb_id, listen_id,listen_name, domain, url, "NULL", "NULL",
                                        #     "NULL", "NULL", "NULL", "NULL")
                                        break
                                    targets = i["Targets"]
                                    # print (targets)
                                    if not targets and targets is None:
                                        data_content = {
                                            "APPGROUP": appgroup_name,
                                            "LOADBALANCERNAME": clb_name,
                                            "LOADBALANCEID": clb_id,
                                            "LISTENERID": listen_id,
                                            "LISTENNAME": listen_name,
                                            "Domain": domain if domain else listen_name,
                                            "Url": url if url else '/',
                                            "LocationId": LocationId,
                                            "HealthStatus": "NULL",
                                            "IP": "NULL",
                                            "Port": "NULL",
                                            "TargetId": "NULL",
                                            "HealthStatusDetial": "NULL",
                                            "Weight": "NULL",
                                            "Instance": "NULL"
                                        }
                                        Total.append(data_content)
                                        # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
                                        #     appgroup_name, clb_name, clb_id, listen_id,listen_name, domain, url, "NULL", "NULL","NULL","NULL", "NULL", "NULL")
                                        break
                                    for i in targets:
                                        if ('HealthStatus' not in i) and ('IP' not in i) and ('TargetId' not in i) and (
                                                'Port' not in i) and ('HealthStatusDetial' not in i):
                                            data_content = {
                                                "APPGROUP": appgroup_name,
                                                "LOADBALANCERNAME": clb_name,
                                                "LOADBALANCEID": clb_id,
                                                "LISTENERID": listen_id,
                                                "LISTENNAME": listen_name,
                                                "Domain": domain if domain else listen_name,
                                                "Url": url if url else '/',
                                                "LocationId": LocationId,
                                                "HealthStatus": "NULL",
                                                "IP": "NULL",
                                                "Port": "NULL",
                                                "TargetId": "NULL",
                                                "HealthStatusDetial": "NULL",
                                                "Weight": "NULL",
                                                "Instance": "NULL"
                                            }
                                            Total.append(data_content)
                                            # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
                                            #     appgroup_name, clb_name, clb_id, listen_id,listen_name, domain, url, "NULL", "NULL","NULL", "NULL", "NULL", "NULL")
                                            break
                                        healthStatus = i["HealthStatus"]
                                        ip = i["IP"]
                                        # print (ip)
                                        targetId = i["TargetId"]
                                        client = self.HttpInstance()
                                        req = models.DescribeTargetsRequest()
                                        params = {
                                            "LoadBalancerId": clb_id,
                                            "ListenerIds": [listen_id]
                                        }
                                        req.from_json_string(json.dumps(params))
                                        resp = client.DescribeTargets(req)
                                        # print(json.dumps(result_json))
                                        port = i["Port"]
                                        healthStatusDetial = i["HealthStatusDetial"]
                                        result_json = json.loads(resp.to_json_string())
                                        Weight = ""
                                        # print(json.dumps(result_json))
                                        for line in result_json["Listeners"]:
                                            if line["ListenerId"] == listen_id:
                                                for line in line["Rules"]:
                                                    if line["LocationId"] == LocationId:
                                                        for line in line["Targets"]:
                                                            if line["InstanceId"] == targetId:
                                                                Weight = line["Weight"]
	                                        # data_content += """APPGROUP:{}||LOADBALANCERNAME:{}||LOADBALANCEID:{}||LISTENERID:{}||LISTENNAME:{}||Domain:{}||Url:{}||HealthStatus:{}||IP:{}||LOCATIONID:{}||TargetId:{}||Port:{}||HealthStatusDetial:{}||Weight:{}\n""".format(
	                                        # appgroup_name, clb_name, clb_id, listen_id,listen_name ,domain, url, healthStatus, ip,LocationId,targetId, port, healthStatusDetial, Weight)
                                        data_content = {
                                            "APPGROUP": appgroup_name,
                                            "LOADBALANCERNAME": clb_name,
                                            "LOADBALANCEID": clb_id,
                                            "LISTENERID": listen_id,
                                            "LISTENNAME": listen_name,
                                            "Domain": domain if domain else listen_name,
                                            "Url": url if url else '/',
                                            "LocationId": LocationId,
                                            "HealthStatus": healthStatus,
                                            "IP": ip,
                                            "Port": port,
                                            "TargetId": targetId,
                                            "HealthStatusDetial": healthStatusDetial,
                                            "Weight": str(Weight),
                                            "Instance": str(ip) + ":" + str(port) + "-" + str(Weight) + "-(" + str(
                                                healthStatusDetial) + ")" if Weight else str(ip) + ":" + str(
                                                port) + "-" + str(Weight) + "NULL" + "-(" + str(
                                                healthStatusDetial) + ")"
	                                     }
                                         Total.append(data_content)
                                        # print(data_content)
	                    # print(Total)
	                    # print(len(Total))
        except TencentCloudSDKException as e:
            self.logger.error("SDK Listener Err:'{}'".format(str(e)))
            print("Err: %s" % e)
        except Exception as e:
            self.logger.error("Listener Err:'{}'".format(str(e)))
            print("Err: %s" % e)
        return Total

    def SwitchInstanceWeight(self, LoadBalancerId, ListenerId, LocationId, InstanceId, Port, Weight):
        fail_list = ""
        try:
            req_instance = self.HttpInstance()
            req = models.ModifyTargetWeightRequest()
            params = {
                "LoadBalancerId": LoadBalancerId, "ListenerId": ListenerId, "LocationId": LocationId,
                "Targets": [{"InstanceId": InstanceId, "Port": int(Port), "Weight": int(Weight)}]
            }
            req.from_json_string(json.dumps(params))
            resp = req_instance.ModifyTargetWeight(req)
            result_json = json.loads(resp.to_json_string())
            self.logger.info("switch instance params:'{}'".format(json.dumps(result_json)))
            print(json.dumps(result_json))
            return self.SwitchStatus(result_json["RequestId"],LoadBalancerId, ListenerId, LocationId, InstanceId, Port)

        except TencentCloudSDKException as err:
            self.logger.error("Switch SDK  Err:'{}'".format(str(err)))
            print(err)
            if "Auth failed" in err or "permission" in err:
                fail_list += "{} {} {} {} {} {}\n".format(self._area, LoadBalancerId,
                                                      ListenerId, LocationId, InstanceId, Port)
            if fail_list != "":
                with open("fail_switch_istance_weight_file.txt", "w+") as f:
                    f.write(fail_list)
        except Exception as e:
            self.logger.error("Switch instance  Err:'{}'".format(str(e)))
            print("Uknown Err: %s" % e)
	
    def SwitchStatus(self, TaskId, LoadBalancerId, ListenerId, LocationId, InstanceId, Port):
        """
        taskId  是每一个请求的得到的返回Requestid
        :param TaskId:
        :param LoadBalancerId:
        :param ListenerId:
        :param LocationId:
        :param InstanceId:
        :param Port:
        :return:
        """
        fail_list = ""
        try:
            req_instance = self.HttpInstance()
            req = models.DescribeTaskStatusRequest()
            params = {
                "TaskId": TaskId
            }
            req.from_json_string(json.dumps(params))
            resp = req_instance.DescribeTaskStatus(req)
            result_json = json.loads(resp.to_json_string())
            print(resp.to_json_string())
            self.logger.info("Switch status :'{}'".format(resp.to_json_string()))
            return json.dumps(result_json)

        except TencentCloudSDKException as err:
            self.logger.error("Switch status SDK Err:'{}'".format(str(err)))
            print(err)
            if "Auth failed" in err or "permission" in err:
                fail_list += "{} {} {} {} {} {}\n".format(self._area, LoadBalancerId,
                                                          ListenerId, LocationId, InstanceId, Port)
            if fail_list != "":
                with open("fail_switch_istance_weight_file.txt", "w+") as f:
                    f.write(fail_list)

        except Exception as e:
            self.logger.error("Switch status  Err:'{}'".format(str(e)))
            print("Uknown Err: %s" % e)
	
    def __call__(self, _lbOffsetParamsQ):
        for th in range(ThreadNum):
            t = Thread(target=self.Lb_Obj, args=(_lbOffsetParamsQ,))
            t.setDaemon(True)
            t.start()
        _lbOffsetParamsQ.join()
        return self._lbList
	
def run():
    if len(sys.argv) > 2:
        if sys.argv[1] == "init":
            try:
                time_start = time.time()
                lbparmasQ = RequestAgent(sys.argv[2])(0, 20)
                # print(lbparmasQ)
                lbListobj = RequestLoadBlanceObj(sys.argv[2])(lbparmasQ)
                RequestLoadBlanceObj(sys.argv[2]).SwitchInstanceWeight()
                data = {}
                data["total"] =len(lbListobj)
                data["data"] = lbListobj
                # print(data)
                file = sys.argv[2] + "_cloud_clb_listener_specific_list.txt"
                with open(file, "w+") as f:
                    f.write(json.dumps(data))
                time_end = time.time()
                print("finalstate:FINISH")
                print('totally cost', time_end - time_start)
                sys.exit(1)
            except Exception as e:
                print("finalstate:ERROR")
                sys.exit(0)

        elif sys.argv[1] == "filter":
            try:
                file = sys.argv[2] + "_cloud_clb_listener_specific_list.txt"
                with open(file, "r") as f:
                    r = f.read()
                print("finalstate:FINISH")
                return list(filter(
                    lambda data: data["LISTENNAME"] == sys.argv[3],
                    json.loads(r)["data"]
                ))
                # params = json.loads(sys.argv[2])
                # if params.get("area",None) and params.get("LISTENNAME",None):
                #     file = sys.argv[2] + "_cloud_clb_listener_specific_list.txt"
                #     with open(file, "r") as f:
                #         r = f.read()
                #     print("finalstate:FINISH")
                #     return list(filter(
                #         lambda data: data["LISTENNAME"] == sys.argv[3],
                #         json.loads(r)["data"]
                #     ))
           except Exception as e:
                print("finalstate:ERROR")
                sys.exit(0)
        else:
            pass

if __name__ == "__main__":
     run()
