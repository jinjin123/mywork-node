#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys, subprocess, re, json

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
# HealthyHostCount,一分钟检查一次，当健康主机数量等于0，就告警。健康主机的最大值小于等于0就告警
def getHealthyHostCountComm(elb_name, port, tag_group, elb_arn, sns_arn):
    mertic = 'HealthyHostCount'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name \"AWS_ELB_{name}_{port}_{mertic}\" \
--alarm-description \"aws elb {mertic}\" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Maximum \
--period 60 \
--threshold 0 \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator LessThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=TargetGroup,Value=targetgroup/{tag_group}" "Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, port=port, action=sns_arn, tag_group=tag_group, elb_arn=elb_arn, mertic=mertic)


# ActiveFlowCount,3分钟检查3次，当链接数平均大于或等于6000，就告警。
def getActiveFlowCountComm(elb_name, port, tag_group, elb_arn, sns_arn):
    mertic = 'ActiveFlowCount'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_ELB_{name}_{port}_{mertic}" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Average \
--period 300 \
--threshold 6000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=TargetGroup,Value=targetgroup/{tag_group}" "Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, port=port, action=sns_arn, tag_group=tag_group, elb_arn=elb_arn, mertic=mertic)


# ProcessedBytes,3分钟检查3次，当链接数平均大于或等于5M，就告警。
def getProcessedBytesComm(elb_name, port, tag_group, elb_arn, sns_arn):
    mertic = 'ProcessedBytes'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_ELB_{name}_{port}_{mertic}" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Average \
--period 60 \
--threshold 5000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=TargetGroup,Value=targetgroup/{tag_group}" "Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, port=port, action=sns_arn, tag_group=tag_group, elb_arn=elb_arn, mertic=mertic)


# UnHealthyHostCount 五分钟检查一次，当不健康主机数量大于或等于1个，就告警.  不健康主机数量的最小值大于等于1就告警
def getUnHealthyHostCountComm(elb_name, port, tag_group, elb_arn, sns_arn):
    mertic = 'UnHealthyHostCount'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_ELB_{name}_{port}_{mertic}" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Minimum \
--period 300 \
--threshold 1 \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=TargetGroup,Value=targetgroup/{tag_group}" "Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, port=port, action=sns_arn, tag_group=tag_group, elb_arn=elb_arn, mertic=mertic)


# HTTPCode_Target_5XX_Count 一分钟采集一次，周期为1分钟，1个数据点中有1次超过阈值就告警，当5xx超过10个为超过阈值
def getHTTPCode_Target_5XX_CountComm(elb_name, port, tag_group, elb_arn, sns_arn):
    mertic = 'HTTPCode_Target_5XX_Count'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_ELB_{name}_{port}_{mertic}" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Sum \
--period 60 \
--threshold 10 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=TargetGroup,Value=targetgroup/{tag_group}" "Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, port=port, action=sns_arn, tag_group=tag_group, elb_arn=elb_arn, mertic=mertic)


# HTTP_4XX 一分钟采集一次，周期为5分钟，5个数据点中有三次超过阈值就告警，当4xx超过10%为超过阈值
def getHTTPCode_Target_4XX_CountComm(elb_name, port, tag_group, elb_arn, sns_arn):
    mertic = 'HTTPCode_Target_4XX_Count'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "AWS_ELB_{name}_{port}_{mertic}" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Sum \
--period 60 \
--threshold 10 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 5 \
--datapoints-to-alarm 3 \
--unit Percent \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=TargetGroup,Value=targetgroup/{tag_group}\" "Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, port=port, action=sns_arn, tag_group=tag_group, elb_arn=elb_arn, mertic=mertic)


# 执行命令函数
def execCommand(comm):
    try:
        print(comm)
        (status, stdout) = subprocess.getstatusoutput(comm)
        # print(comm)
        print(status)
        return stdout
    except Exception as e:
        print(e)


# 获取当前可用区内所有elb2的信息
def getAll():
    comm1 = "%s elbv2 describe-load-balancers" % Contants['AWSCLI']
    AllLb2Details = json.loads(execCommand(comm1))['LoadBalancers']
    arndict = CreateDict()
    for i in range(0, len(AllLb2Details)):
        lbarn = AllLb2Details[i]["LoadBalancerArn"]
        lbname = AllLb2Details[i]["LoadBalancerName"]
        arndict[lbname]["type"] = AllLb2Details[i]["Type"]
        arndict[lbname]["lbarn"] = lbarn
        if arndict[lbname]["type"] == "network":
            comm2 = "%s elbv2 describe-target-groups --load-balancer-arn %s" % (
                Contants['AWSCLI'], lbarn)
            lb_target = json.loads(execCommand(comm2))
            arndict[lbname]["lbgroup"]['TCP'] = lb_target['TargetGroups'][0]['TargetGroupArn']
        else:
            comm2 = "%s elbv2 describe-listeners --load-balancer-arn %s" % (Contants['AWSCLI'], lbarn)
            alllisten = json.loads(execCommand(comm2))['Listeners']
            for j in range(0, len(alllisten)):
                taggroup = alllisten[j]['DefaultActions'][0]['TargetGroupArn']
                port = alllisten[j]['Port']
                arndict[lbname]["lbgroup"][port] = taggroup
    return arndict


# 添加报警
def add_alert(arn_data, sns_arn):
    for elb_name, elb_value in arn_data.items():
        elb_arn = re.split(r'loadbalancer/app/', elb_value['lbarn'])[-1]
        for port, taggroup in elb_value['lbgroup'].items():
            print("######################################################")
            taggroup = re.split(r':targetgroup/', taggroup)[-1]

            execCommand(getHealthyHostCountComm(elb_name, port, taggroup, elb_arn, sns_arn))
            execCommand(getUnHealthyHostCountComm(elb_name, port, taggroup, elb_arn, sns_arn))
            execCommand(getActiveFlowCountComm(elb_name, port, taggroup, elb_arn, sns_arn))
            execCommand(getProcessedBytesComm(elb_name, port, taggroup, elb_arn, sns_arn))

            if elb_value['type'] != 'network':
              execCommand(getHTTPCode_Target_5XX_CountComm(elb_name, port, taggroup, elb_arn, sns_arn))
              execCommand(getHTTPCode_Target_4XX_CountComm(elb_name, port, taggroup, elb_arn, sns_arn))

if __name__ == '__main__':
    sns_arn = "arn:aws-cn:sns:cn-north-1:377051234567:sns-example"

    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        print('[Region] ', i)
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)


