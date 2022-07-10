#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import subprocess

# 1. 配置cli路径和region
Contants = {
    "AWSCLI": '"C:\\Program Files\\Amazon\\AWSCLI\\bin\\aws.exe" --output json',
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
def getCPUUtilizationComm(name, action, instance_id):
    mertic = 'CPUUtilization'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_EC2_{name}_{mertic}" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Average \
--period 60 \
--threshold 70 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--unit Percent \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic)


# NetworkIn,3分钟检查3次，平均值大于或等于5m，就告警。
def getNetworkInComm(name, action, instance_id):
    mertic = 'NetworkIn'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_EC2_{name}_{mertic}" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value=%s"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic)


# NetworkOut,3分钟检查3次，平均值大于或等于5m，就告警。
def getNetworkOutComm(name, action, instance_id):
    mertic = 'NetworkOut'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_EC2_{name}_{mertic}" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic)


# 执行命令函数
def execCommand(comm):
    try:
        print(comm)
        (status, stdout) = subprocess.getstatusoutput(comm)
        print(status)
        return stdout
    except Exception as e:
        print(e)


# 获取当前可用区内所有lb2的基础信息
def getAll():
    comm1 = "%s ec2 describe-instances" % Contants['AWSCLI']

    all_data = json.loads(execCommand(comm1))

    instance_list = []

    for r in all_data['Reservations']:
        for i in r['Instances']:
            data = {'id': i['InstanceId']}
            for t in i['Tags']:
                if t['Key'] == 'Name':
                    data['name'] = t['Value']
            if not data['name']:
                data['name'] = i['InstanceId']
            instance_list.append(data)

    return instance_list


# 添加报警
def add_alert(data, action):
    for i in data:
        instance_id = i['id']
        name = i['name']
        execCommand(getCPUUtilizationComm(name, action, instance_id))
        execCommand(getNetworkInComm(name, action, instance_id))
        execCommand(getNetworkOutComm(name, action, instance_id))


if __name__ == '__main__':
    # 2. 配置sns的arn
    sns_arn = "arn:aws-cn:sns:cn-north-1:377051234567:sns-example"

    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        print('[Region] ', i)
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)

