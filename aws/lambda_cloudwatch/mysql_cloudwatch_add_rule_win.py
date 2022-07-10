#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import subprocess

Contants = {
    "AWSCLI": '"C:\\Program Files\\Amazon\\AWSCLI\\bin\\aws.exe"  --output json',
    "AWSREGION": ['cn-north-1']  # 北京
}


# 构造字典
class CreateDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


#########################################################################################################
# 配置告警

# CPUUtilization,3分钟检查3次，平均值大于或等于80%，就告警。
def getCPUUtilizationComm(action, instance_id):
    mertic = 'CPUUtilization'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_MYSQL_{id}_{mertic}" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 60 \
--threshold 70 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# DatabaseConnections,3分钟检查3次，平均值大于或等于500，就告警。
def getDatabaseConnectionsComm(action, instance_id):
    mertic = 'DatabaseConnections'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_MYSQL_{id}_{mertic}" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 60 \
--threshold 500 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# FreeableMemory,3分钟检查3次，平均值小于于或等于1g，就告警。
def getFreeableMemoryComm(action, instance_id):
    mertic = 'FreeableMemory'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_MYSQL_{id}_{mertic}" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 60 \
--threshold 1000000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator LessThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# FreeStorageSpace,15分钟检查3次，平均值小于于或等于20g，就告警。
def FreeStorageSpace(action, instance_id):
    mertic = 'FreeStorageSpace'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_MYSQL_{id}_{mertic}" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 300 \
--threshold 20000000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator LessThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# NetworkTransmitThroughput,3分钟检查3次，平均值小于于或等于5m，就告警。
def getNetworkTransmitThroughputComm(action, instance_id):
    mertic = 'NetworkTransmitThroughput'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_MYSQL_{id}_{mertic}" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# NetworkBytesOut,3分钟检查3次，平均值小于于或等于5m，就告警。
def getNetworkReceiveThroughputComm(action, instance_id):
    mertic = 'NetworkReceiveThroughput'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_MYSQL_{id}_{mertic}" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# 执行命令函数
def execCommand(comm):
    try:
        print(comm)
        (status, stdout) = subprocess.getstatusoutput(comm)
        print(status)
        return stdout
    except Exception as e:
        print(e)


# 获取当前可用区内RDS的基础信息
def getAll():
    comm1 = "%s rds describe-db-instances" % Contants['AWSCLI']

    all_data = json.loads(execCommand(comm1))

    instance_list = []

    for r in all_data['DBInstances']:
        if r['Engine'] == 'mysql':
            data = {'id': r['DBInstanceIdentifier']}
            instance_list.append(data)

    return instance_list


# 添加报警
def add_alert(data, action):
    for i in data:
        id = i['id']
        execCommand(getCPUUtilizationComm(action, id))
        execCommand(getDatabaseConnectionsComm(action, id))
        execCommand(getFreeableMemoryComm(action, id))
        execCommand(getNetworkReceiveThroughputComm(action, id))
        execCommand(getNetworkTransmitThroughputComm(action, id))
        execCommand(FreeStorageSpace(action, id))


if __name__ == '__main__':
    sns_arn = "arn:aws-cn:sns:cn-north-1:377051234567:sns-example"
    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        print('[Region] ', i)
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)

