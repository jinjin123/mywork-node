#-*- coding:utf8 -*-
# filename = taskname
# dag_id = taskname
# task_id = action_name + deal_sequence + taskname
import sys, os
import time
import json, logging
from 
#< from py tookit import logger first> 
class DealData(object):
        def __init__(self, json_paramsdata_file, json_scriptdata_file, dag_template_tile):
            self.Log = LogOut()
            self.json_paramsdata_file = json_paramsdata_file
            self.json_scriptdata_file = json_scriptdata_file
            self.dag_template_tile = dag_template_tile
            # self.Log.info("json body: %s" %  self.json_paramsdata_file)
        def result_json_paramsdata(self):
            json_paramsdata = json.loads(self.json_paramsdata_file)
            return json_paramsdata

        def action_script_file(self, actionname):
            json_scriptdata = ""
            script_file = ""
            try:
                with open(self.json_scriptdata_file, 'r') as scriptfileconfig:
                    read_scriptdata = scriptfileconfig.readlines()

            except Exception as err:
                self.Log.error(err)

            try:
                for line1 in read_scriptdata:
                    if line1 == '\n':
                        line1 = line1.strip()

                    json_scriptdata += line1

                json_scriptdata = json.loads(json_scriptdata.strip())
                for line2 in json_scriptdata['wsserver_config']:
                    action_name = line2['action_name']
                    if action_name == actionname:
                        script_file = line2['action_file']

            except Exception as err:
                self.Log.error(err)
            return script_file

        def dag_name(self):
            data = self.result_json_paramsdata()
            # data = json.loads(self.result_json_paramsdata())
            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # print (data)
            # logpath = "/data/APP_DIR/airflow/logs/"
            # taskname = data["task_name"]
            # all_status_n = logpath + taskname + "-status.log"
            # all_status_tn = logpath + taskname + "-status-tmp.log"
            # with open(all_status_n, "w+")as f:
            #     print >> f, len(data["action_list"])
            # with open(all_status_tn, "w+")as tf:
            #     print >> tf, len(data["action_list"])
            taskname = data["task_name"]
            # dag_filename = taskname
            # dags_id = taskname
            # print("\n%s"%taskname)
            return taskname


        def dag_BashOperator(self):
            # """ actionname, dealsequence, params
            ##bash_command='/data/srv/salt/ittool/2_app_deploy/7.copy_upload_local.sh {{ params.v1 }} {{ params.v2 }} {{ params.v3 }} {{ params.v4 }} {{ params.v5 }} {{ params.v6 }}',
            ##params={ 'v1': u'ip', 'v2': u'taskname', 'v3': u'deploy_path','v4': u'type' },"""
            data = self.result_json_paramsdata()
            bashoperator = ""
            try:
                actionlists = data['action_list']
                for each_actionlist in actionlists:
                    actionunit = each_actionlist['action_unit']
                    actionname = actionunit['action_name']
                    actionpars = actionunit['action_pars']
                    dealsequence = actionpars['deal_sequence']
                    targetobjects = actionunit['target_objects']
                    for param in targetobjects:
                        params1 = param["object_name"]
                        params2 = param["config1"]
                        params3 = param["config2"]
                        params4 = param["config3"]
                        params5 = param["config4"]
                        params6 = param["config5"]
                        params = """{{'v1': u'{}', 'v2': u'{}', 'v3': u'{}', 'v4': u'{}', 'v5': u'{}', 'v6': u'{}'}}""".format(
                                params1, params2, params3, params4, params5, params6)

                        # taskid = "{}-{}-{}".format(actionname, dealsequence, self.dag_name())
                        taskid = "{}-{}-{}".format(dealsequence, actionname, self.dag_name())
                        bashoperator += """t{} = BashOperator(
                                task_id='{}',
                                bash_command='{} "{{{{ params.v1 }}}}" "{{{{ params.v2 }}}}" "{{{{ params.v3 }}}}" "{{{{ params.v4 }}}}" "{{{{ params.v5 }}}}" "{{{{ params.v6 }}}}"',
                                params={},
                                trigger_rule='all_success',
                                dag=dag)
                         """.format(dealsequence, taskid, self.action_script_file(actionname), params)
            except Exception as err:
                self.Log.error(err)
                # print(bashoperator)
            return bashoperator.strip()

        def dag_actionstream(self):
            data = self.result_json_paramsdata()
            rulesList = data["flow_rules"]
            ruleInfoList = []
            for ruledd in rulesList:
                ruleInfoList = ruledd["task_info"]["task_list"]

        def dag_queue(self):
            AREA_LIST = "OAVPC;YUNTI;TCLOUD;AP;EU;NA;YUNTINA;YUNTIAP;YUNTIEU"
            TEST_LIST = "TESTOPS;FUNCTEST;SEPCTEST;SPECTEST"
            task_name = self.dag_name()
            temp = task_name.split('-')[1:-2]
            root = '-'.join(temp)
            area = ""
            if "TEST" in task_name and task_name.split('-')[1] in TEST_LIST.split(';'):
                # TESTOPS, FUNCTEST,SPECTEST
                area = task_name.split('-')[1]

            elif 'DOCKERIMAGE' in root.upper():
                area = "ODC"
            elif temp[1] in AREA_LIST.split(';') and 'DOCKER' in root.upper():
                area = str(temp[1]).upper()
            else:
                area = "OA"
            return area

        def dag_file(self, ou_type):
            dag_path = "F:\python\demo\dags\\"
            owner_name = ou_type
            if owner_name and (owner_name.upper() == "QA" or owner_name.upper() == "TEST"):
                owner_name = "qa"
            elif owner_name and (owner_name.upper() == "OPS"):
                owner_name = "ops"
            else:
                owner_name = "airflow"

            dag_file_name = '{}/{}.py'.format(dag_path, self.dag_name())

            # dag_file_name = '{}.py'.format(self.dag_name())

            with open(self.dag_template_tile, 'r') as dagtemplatetile:
                read_content = dagtemplatetile.readlines()

            template_content = ""

            try:
                for line in read_content:
                    template_content += line

            except Exception as err:
                self.Log.error(err)
            dags_name = self.dag_name()
            pool_queue = self.dag_queue()
            self.Log.info("dags name: %s" % dags_name)
            self.Log.info("pool queue: %s" % pool_queue)
            dag_content = template_content.replace('{{TENCENT_DAGID}}', dags_name)
            dag_content = dag_content.replace('{{TENCENT_OWNER}}', owner_name)
            dag_content = dag_content.replace('{{TENCENT_QUEUE}}', pool_queue)
            dag_content = dag_content.replace('{{TENCENT_POOL}}', pool_queue)
            dag_content = dag_content.replace('{{TENCENT_BASHOPERATOR}}', self.dag_BashOperator())
            dag_content = dag_content.replace("{{TENCENT_ACTIONSTREAM}}", self.dag_actionstream())
            # print(dag_content)

            with open(dag_file_name, "w+") as dagfile:
                for conten_line in dag_content:
                    dagfile.write(conten_line)
                    # print >> dagfile, conten_line

def main():
    Log = LogOut()
    Log.info("Begin...")

    if len(sys.argv) > 1:
        params_filename = sys.argv[1]
        # ou_type = sys.argv[2]
        ou_type = ""

    else:
        print("aaa")
        # params_filename = "/data/APP_DIR/airflow/airflow_tool/config/example.json"
        # ou_type = ""
    # Log.info(params_filename.decode('utf-8'))
    #script_filename = "/data/APP_DIR/airflow/airflow_tool/config/wsserver_config.json"
    script_filename = "F:\python\demo\wsserver_config.json"
    #dag_template = "/data/APP_DIR/airflow/airflow_tool/config/DEPLOY_TEMPLATE.py"
    dag_template = "F:\python\demo\DEPLOY_TEMPLATE.py"
    Deal_Data = DealData(params_filename, script_filename, dag_template)
    Deal_Data.dag_file(ou_type)
    # Deal_Data.dag_name()
    # for actionlist in data['action_list']:
    #     actionunit = actionlist['action_unit']
    #     print(actionunit['action_name'], actionunit['target_objects'])





if __name__ == '__main__':
    main() 


