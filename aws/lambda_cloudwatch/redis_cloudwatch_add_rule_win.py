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

# CPUUtilization,3分钟检查3次，平均值大于或等于70%，就告警。
def getCPUUtilizationComm(name, action, instance_id):
    mertic = 'CPUUtilization'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 70 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                        id=instance_id, mertic=mertic)


# EngineCPUUtilization,3分钟检查3次，平均值大于或等于70%，就告警。
def getEngineCPUUtilizationComm(name, action, instance_id):
    mertic = 'EngineCPUUtilization'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 70 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                        id=instance_id, mertic=mertic)


# CurrConnections,3分钟检查3次，平均值大于或等于500，就告警。
def getCurrConnectionsComm(name, action, instance_id):
    mertic = 'CurrConnections'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 500 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                        id=instance_id, mertic=mertic)


#
# FreeableMemory,3分钟检查3次，平均值小于于或等于1g，就告警。
def getFreeableMemoryComm(name, action, instance_id):
    mertic = 'FreeableMemory'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 1000000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator LessThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                        id=instance_id, mertic=mertic)


# NetworkBytesIn,3分钟检查3次，平均值小于于或等于5m，就告警。
def getNetworkBytesInComm(name, action, instance_id):
    mertic = 'NetworkBytesIn'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                        id=instance_id, mertic=mertic)


# NetworkBytesOut,3分钟检查3次，平均值小于于或等于5m，就告警。
def getNetworkBytesOutComm(name, action, instance_id):
    mertic = 'NetworkBytesOut'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                        id=instance_id, mertic=mertic)


# CacheMisses,3分钟检查3次，平均值小于于或等于5000，就告警。
def getCacheMissesComm(name, action, instance_id):
    mertic = 'CacheMisses'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_REDIS_{name}_{id}_{mertic}" \
--alarm-description "aws redis {mertic}" \
--metric-name {mertic} \
--namespace AWS/ElastiCache \
--statistic Average \
--period 60 \
--threshold 5000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=CacheClusterId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
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


# 获取当前可用区内elasticache的基础信息
def getAll():
    comm1 = "%s elasticache describe-cache-clusters" % Contants['AWSCLI']

    all_data = json.loads(execCommand(comm1))

    instance_list = []

    for r in all_data['CacheClusters']:
        if r['Engine'] == 'redis':
            data = {'id': r['CacheClusterId'], 'name': r['ReplicationGroupId']}
            instance_list.append(data)

    return instance_list


# 添加报警
def add_alert(data, action):
    for i in data:
        id = i['id']
        name = i['name']
        execCommand(getCPUUtilizationComm(name, action, id))
        execCommand(getEngineCPUUtilizationComm(name, action, id))
        execCommand(getCurrConnectionsComm(name, action, id))
        execCommand(getFreeableMemoryComm(name, action, id))
        execCommand(getNetworkBytesInComm(name, action, id))
        execCommand(getNetworkBytesOutComm(name, action, id))
        execCommand(getCacheMissesComm(name, action, id))


if __name__ == '__main__':
    sns_arn = "arn:aws-cn:sns:cn-north-1:377051234567:sns-example"
    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        print('[Region] ', i)
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)


