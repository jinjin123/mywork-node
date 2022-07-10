import boto3
import json

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')
sns_arn = "sns——arn"
region = "cn-north-1"


def add_elb_alarm(instance_arn, instance_name=None):
    print("[Add elb alarm.]")

    elb_client = boto3.client('elbv2')

    instance = elb_client.describe_listeners(LoadBalancerArn=instance_arn)
    arn = instance_arn.split(':loadbalancer/')[1]
    print(instance)
    targetgroup_list = []
    for listener in instance.get('Listeners'):
        for action in listener['DefaultActions']:
            print(action['TargetGroupArn'])

            targetgroup_arn = action['TargetGroupArn']
            targetgroup = targetgroup_arn.split(':')[-1]
            targetgroup_list.append(targetgroup)

    print("[ActiveFlowCount, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 当链接数平均大于或等于 6000 就告警]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_ELB_%s_ActiveFlowCount' % instance_name,
        AlarmDescription='Alarm when ELB ActiveFlowCount exceeds 6000',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='ActiveFlowCount',
        Namespace='AWS/ApplicationELB',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': '%s' % arn
            }
        ],
        Period=60,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=6000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NewFlowCount, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 当链接数平均大于或等于 1000 就告警]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_ELB_%s_NewFlowCount' % instance_name,
        AlarmDescription='Alarm when ELB NewFlowCount exceeds 6000',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NewFlowCount',
        Namespace='AWS/ApplicationELB',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': '%s' % arn
            }
        ],
        Period=60,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=1000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[ProcessedBytes, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 当链接数平均大于或等于 5m 就告警]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_ELB_%s_ProcessedBytes' % instance_name,
        AlarmDescription='Alarm when ELB ProcessedBytes exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='ProcessedBytes',
        Namespace='AWS/ApplicationELB',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': 'app/%s' % arn
            }
        ],
        Period=60,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    for targetgroup in set(targetgroup_list):
        targetgroup_name = targetgroup.split('/')[1]

        print("[HealthyHostCount, 1分钟采集1次, 周期为1分钟, 1分钟有1个数据点超过阈值就告警, 健康主机的最大值小于等于 0 就告警]")
        response = cloudwatch.put_metric_alarm(
            AlarmName='AWS_ELB_%s_%s_HealthyHostCount' % (instance_name, targetgroup_name),
            AlarmDescription='Alarm when ELB HealthyHostCount less than 0',
            ActionsEnabled=True,
            OKActions=[sns_arn],
            AlarmActions=[sns_arn],
            MetricName='HealthyHostCount',
            Namespace='AWS/ApplicationELB',
            Statistic='Maximum',
            Dimensions=[
                {
                    'Name': 'TargetGroup',
                    'Value': '%s' % targetgroup
                },
                {
                    'Name': 'LoadBalancer',
                    'Value': '%s' % arn
                }
            ],
            Period=60,
            Unit='Percent',
            EvaluationPeriods=1,
            DatapointsToAlarm=1,
            Threshold=0,
            ComparisonOperator='LessThanOrEqualToThreshold',
            TreatMissingData='notBreaching'
        )
        print(response)

        print("[UnHealthyHostCount, 1分钟采集1次, 周期为1分钟, 1分钟有1个数据点超过阈值就告警, 当不健康主机数量大于或等于 1 个就告警]")
        response = cloudwatch.put_metric_alarm(
            AlarmName='AWS_ELB_%s_%s_UnHealthyHostCount' % (instance_name, targetgroup_name),
            AlarmDescription='Alarm when ELB UnHealthyHostCount exceeds 5m',
            ActionsEnabled=True,
            OKActions=[sns_arn],
            AlarmActions=[sns_arn],
            MetricName='UnHealthyHostCount',
            Namespace='AWS/ApplicationELB',
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'TargetGroup',
                    'Value': '%s' % targetgroup
                },
                {
                    'Name': 'LoadBalancer',
                    'Value': '%s' % arn
                }
            ],
            Period=60,
            EvaluationPeriods=1,
            DatapointsToAlarm=1,
            Threshold=1,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            TreatMissingData='notBreaching'
        )
        print(response)

def add_elb_http_alarm(instance_group, instance_arn, port=80, instance_name=None):
    print("[Add elb http %s alarm.]" % instance_group)
    print("[HTTPCode_Target_5XX_Count, 1分钟采集1次, 周期为1分钟, 1分钟有1个数据点超过阈值就告警, 当5xx超过 10 个为超过阈值]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_ELB_%s_%s_HTTPCode_Target_5XX_Count' % (instance_name, port),
        AlarmDescription='Alarm when ELB HTTPCode_Target_5XX_Count exceeds 10',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='HTTPCode_Target_5XX_Count',
        Namespace='AWS/ApplicationELB',
        Statistic='Sum',
        Dimensions=[
            {
                'Name': 'TargetGroup',
                'Value': 'targetgroup/%s' % instance_group
            },
            {
                'Name': 'LoadBalancer',
                'Value': 'app/%s' % instance_arn
            }
        ],
        Period=60,
        EvaluationPeriods=1,
        DatapointsToAlarm=1,
        Threshold=10,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[HTTPCode_Target_4XX_Count, 1分钟采集1次, 周期为1分钟, 5分钟有3个数据点超过阈值就告警, 当4xx超过 10% 为超过阈值]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_ELB_%s_%s_HTTPCode_Target_4XX_Count' % (instance_name, port),
        AlarmDescription='Alarm when ELB HTTPCode_Target_4XX_Count exceeds 10',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='HTTPCode_Target_4XX_Count',
        Namespace='AWS/ApplicationELB',
        Statistic='Sum',
        Dimensions=[
            {
                'Name': 'TargetGroup',
                'Value': 'targetgroup/%s' % instance_group
            },
            {
                'Name': 'LoadBalancer',
                'Value': 'app/%s' % instance_arn
            }
        ],
        Period=60,
        EvaluationPeriods=5,
        DatapointsToAlarm=3,
        Threshold=10,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)


def add_ec2_alarm(instance_id, instance_name=None):
    print("Add ec2 %s alarm." % instance_id)
    print("[CPUUtilization, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 80%]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_EC2_%s_CPUUtilization' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when server CPU exceeds 80%',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=80.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NetworkIn, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_EC2_%s_NetworkIn' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when server NetworkIn exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NetworkIn',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NetworkOut, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_EC2_%s_NetworkOut' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when server NetworkOut exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NetworkOut',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[StatusCheckFailed_System, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_EC2_%s_StatusCheckFailed_System' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when server NetworkOut Status Check Failed',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='StatusCheckFailed_System',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=1.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)


def add_ec2_ebs_alarm(instance_id, instance_name=None):
    print("Add ec2 ebs %s alarm." % instance_id)

    ec2d = boto3.resource('ec2')
    instance = ec2d.Instance(instance_id)
    vol_id = instance.volumes.all()
    print(vol_id)
    for v in vol_id:
        print("[Found EBS volume %s on instance %s]" % (v.id, instance_id))
        print("[VolumeIdleTime, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 80%]")
        response = cloudwatch.put_metric_alarm(
            AlarmName='AWS_EC2_%s_EBS_%s_VolumeIdleTime' % (instance_name if instance_name else instance_id, v.id),
            AlarmDescription='Alarm when server CPU exceeds 80%',
            ActionsEnabled=True,
            OKActions=[sns_arn],
            AlarmActions=[sns_arn],
            MetricName='VolumeIdleTime',
            Namespace='AWS/EBS',
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'VolumeId',
                    'Value': '%s' % v.id
                },
            ],
            Period=60,
            EvaluationPeriods=3,
            DatapointsToAlarm=3,
            Threshold=30.0,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            TreatMissingData='notBreaching'
        )
        print(response)


def add_redis_alarm(instance_id, instance_name=None):
    print("[Add redis %s alarm.]" % instance_id)
    print("[CPUUtilization, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 80%]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_CPUUtilization' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis CPU exceeds 80%',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='CPUUtilization',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=80.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[EngineCPUUtilization, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 80%]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_EngineCPUUtilization' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis Engine CPU exceeds 80%',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='EngineCPUUtilization',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=80.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[CurrConnections, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 500]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_CurrConnections' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis connections exceeds 500',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='CurrConnections',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=500,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[FreeableMemory, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值小于于或等于 1G]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_FreeableMemory' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis FreeableMemory Less than 1G',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='FreeableMemory',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=1000000000,
        ComparisonOperator='LessThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NetworkBytesIn, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_NetworkBytesIn' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis NetworkBytesIn exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NetworkBytesIn',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NetworkBytesOut, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_NetworkBytesOut' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis NetworkBytesOut exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NetworkBytesOut',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[CacheMisses, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_REDIS_%s_CacheMisses' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when redis CacheMisses exceeds 5000',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='CacheMisses',
        Namespace='AWS/ElastiCache',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'CacheClusterId',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)


def add_mysql_alarm(instance_id, instance_name=None):
    print("[Add mysql %s alarm.]" % instance_id)
    print("[CPUUtilization, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_MYSQL_%s_CPUUtilization' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when mysql CPUUtilization exceeds 80%',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=80.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[DatabaseConnections, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于或等于 500]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_MYSQL_%s_DatabaseConnections' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when mysql DatabaseConnections exceeds 500',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='DatabaseConnections',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=500,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[FreeableMemory, 1分钟采集1次, 周期为3分钟, 3分钟有3个数据点超过阈值就告警, 平均值小于或等于 1g]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_MYSQL_%s_FreeableMemory' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when mysql FreeableMemory less than 1g',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='FreeableMemory',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=1000000000,
        ComparisonOperator='LessThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[FreeStorageSpace, 5分钟采集1次, 周期为5分钟, 15分钟有3个数据点超过阈值就告警, 平均值小于于或等于 10g]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_MYSQL_%s_FreeStorageSpace' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when mysql FreeStorageSpace less than 10g',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='FreeableMemory',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': '%s' % instance_id
            },
        ],
        Period=300,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=10000000000,
        ComparisonOperator='LessThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NetworkTransmitThroughput, 1分钟采集1次, 周期为1分钟, 3分钟有3个数据点超过阈值就告警, 平均值大于于或等于5m就告警]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_MYSQL_%s_NetworkTransmitThroughput' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when mysql NetworkTransmitThroughput exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NetworkTransmitThroughput',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': '%s' % instance_id
            },
        ],
        Period=60,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

    print("[NetworkReceiveThroughput, 5分钟采集1次, 周期为5分钟, 15分钟有3个数据点超过阈值就告警, 平均值大于或等于 5m]")
    response = cloudwatch.put_metric_alarm(
        AlarmName='AWS_MYSQL_%s_NetworkReceiveThroughput' % (instance_name if instance_name else instance_id),
        AlarmDescription='Alarm when mysql NetworkReceiveThroughput exceeds 5m',
        ActionsEnabled=True,
        OKActions=[sns_arn],
        AlarmActions=[sns_arn],
        MetricName='NetworkReceiveThroughput',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': '%s' % instance_id
            },
        ],
        Period=300,
        Unit='Percent',
        EvaluationPeriods=3,
        DatapointsToAlarm=3,
        Threshold=5000000,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        TreatMissingData='notBreaching'
    )
    print(response)

def add_ec2_dashboard(instance_id, instance_name=None):
    print("[add ec2 %s dashboard]" % (instance_name if instance_name else instance_id))

    body = {"widgets": [
        {
            "type": "metric",
            "x": 6,
            "y": 0,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": False,
                "metrics": [
                    ["AWS/EC2", "NetworkIn", "InstanceId", instance_id],
                    [".", "NetworkOut", ".", "."]
                ],
                "region": region,
                "title": "Network"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 0,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": False,
                "metrics": [
                    ["AWS/EC2", "CPUUtilization", "InstanceId", instance_id],
                ],
                "region": region,
                "title": "CPUUtilization"
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 0,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": False,
                "metrics": [
                    ["AWS/EC2", "EBSWriteOps", "InstanceId", instance_id],
                    [".", "EBSReadOps", ".", "."]
                ],
                "region": region,
                "title": "EBSOps"
            }
        },
        {
            "type": "metric",
            "x": 18,
            "y": 0,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": False,
                "metrics": [
                    ["AWS/EC2", "EBSIOBalance%", "InstanceId", instance_id],
                    [".", "EBSByteBalance%", ".", "."]
                ],
                "region": region,
                "title": "EBSBalance"
            }
        }
    ]
    }
    response = cloudwatch.put_dashboard(
        DashboardName='AWS_EC2_%s' % (instance_name if instance_name else instance_id),
        DashboardBody=json.dumps(body)
    )
    print(response)


def add_mysql_dashboard(instance_id, instance_name=None):
    print("[add mysql %s dashboard]" % (instance_name if instance_name else instance_id))

    body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": [
                        ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", instance_id]
                    ],
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": [
                        ["AWS/RDS", "DatabaseConnections", "DBInstanceIdentifier", instance_id]
                    ],
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": [
                        ["AWS/RDS", "ReadLatency", "DBInstanceIdentifier", instance_id],
                        [".", "WriteLatency", ".", "."]
                    ],
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 18,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": [
                        ["AWS/RDS", "WriteIOPS", "DBInstanceIdentifier", instance_id],
                        [".", "ReadIOPS", ".", "."]
                    ],
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 6,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": [
                        ["AWS/RDS", "NetworkTransmitThroughput", "DBInstanceIdentifier", instance_id],
                        [".", "NetworkReceiveThroughput", ".", "."]
                    ],
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": [
                        ["AWS/RDS", "FreeStorageSpace", "DBInstanceIdentifier", instance_id],
                        [".", "BinLogDiskUsage", ".", "."]
                    ],
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 6,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": [
                        ["AWS/RDS", "FreeableMemory", "DBInstanceIdentifier", instance_id]
                    ],
                    "region": region
                }
            }
        ]
    }
    response = cloudwatch.put_dashboard(
        DashboardName='AWS_MYSQL_%s' % (instance_name if instance_name else instance_id),
        DashboardBody=json.dumps(body)
    )
    print(response)

def add_redis_dashboard(clusters, group_id):
    print("[add redis %s dashboard]" % group_id)

    EngineCPUUtilization_metrcis = []
    CurrConnections_metrcis = []
    FreeableMemory_metrcis = []
    NetworkBytes_metrcis = []
    CacheHits_metrcis = []
    CacheMisses_metrcis = []
    CPUUtilization_metrcis = []
    IsMaster_metrcis = []
    NewConnections_metrcis = []
    StringBasedCmds_metrcis = []
    BytesUsedForCache_metrcis = []
    ReplicationBytes_metrcis = []

    for c in clusters:
        EngineCPUUtilization_metrcis.append(["AWS/ElastiCache", "EngineCPUUtilization", "CacheClusterId", "%s" % c])
        CurrConnections_metrcis.append(["AWS/ElastiCache", "CurrConnections", "CacheClusterId", "%s" % c])
        FreeableMemory_metrcis.append(["AWS/ElastiCache", "FreeableMemory", "CacheClusterId", "%s" % c])
        NetworkBytes_metrcis.append(["AWS/ElastiCache", "NetworkBytesIn", "CacheClusterId", "%s" % c])
        NetworkBytes_metrcis.append(["AWS/ElastiCache", "NetworkBytesOut", "CacheClusterId", "%s" % c])
        CacheHits_metrcis.append(["AWS/ElastiCache", "CacheHits", "CacheClusterId", "%s" % c])
        CacheMisses_metrcis.append(["AWS/ElastiCache", "CacheMisses", "CacheClusterId", "%s" % c])
        CPUUtilization_metrcis.append(["AWS/ElastiCache", "CPUUtilization", "CacheClusterId", "%s" % c])
        IsMaster_metrcis.append(["AWS/ElastiCache", "IsMaster", "CacheClusterId", "%s" % c])
        NewConnections_metrcis.append(["AWS/ElastiCache", "NewConnections", "CacheClusterId", "%s" % c])
        StringBasedCmds_metrcis.append(["AWS/ElastiCache", "StringBasedCmds", "CacheClusterId", "%s" % c])
        BytesUsedForCache_metrcis.append(["AWS/ElastiCache", "BytesUsedForCache", "CacheClusterId", "%s" % c])
        ReplicationBytes_metrcis.append(["AWS/ElastiCache", "BytesUsedForCache", "CacheClusterId", "%s" % c])

    body = {
        "widgets": [
            {
                "type": "metric",
                "x": 6,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "metrics": EngineCPUUtilization_metrcis,
                    "view": "timeSeries",
                    "stacked": True,
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "metrics": CurrConnections_metrcis,
                    "view": "timeSeries",
                    "stacked": True,
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": FreeableMemory_metrcis,
                    "region": region
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": True,
                    "metrics": NetworkBytes_metrcis,
                    "region": region,
                    "title": "NetworkBytes"
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 12,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": CacheHits_metrcis,
                    "region": region,
                    "title": " CacheHits"
                }
            },
            {
                "type": "metric",
                "x": 6,
                "y": 12,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": CacheMisses_metrcis,
                    "region": region,
                    "title": " CacheMisses"
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": CPUUtilization_metrcis,
                    "region": region,
                    "title": "CPUUtilization"
                }
            },
            {
                "type": "metric",
                "x": 18,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": IsMaster_metrcis,
                    "region": region,
                    "title": "IsMaster",
                    "period": 300
                }
            },
            {
                "type": "metric",
                "x": 6,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": NewConnections_metrcis,
                    "region": region,
                    "title": "NewConnections"
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 12,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": StringBasedCmds_metrcis,
                    "region": region,
                    "title": "StringBasedCmds"
                }
            },
            {
                "type": "metric",
                "x": 18,
                "y": 6,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": BytesUsedForCache_metrcis,
                    "region": region,
                    "title": "BytesUsedForCache"
                }
            },
            {
                "type": "metric",
                "x": 18,
                "y": 12,
                "width": 6,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": ReplicationBytes_metrcis,
                    "region": region,
                    "title": "ReplicationBytes"
                }
            }
        ]
    }

    response = cloudwatch.put_dashboard(
        DashboardName='AWS_REDIS_%s' % group_id,
        DashboardBody=json.dumps(body)
    )
    print(response)

def add_elb_dashboard(instance_arn, instance_name):
    print("[add elb %s dashboard]" % instance_name)
    elb_client = boto3.client('elbv2')

    instance = elb_client.describe_listeners(LoadBalancerArn=instance_arn)
    arn = instance_arn.split(':loadbalancer/')[1]

    targetgroup_list = []
    for listener in instance.get('Listeners'):
        for action in listener['DefaultActions']:
            print(action['TargetGroupArn'])

            targetgroup_arn = action['TargetGroupArn']
            targetgroup = targetgroup_arn.split(':')[-1]
            targetgroup_list.append(targetgroup)

    HealthyHost_metrcis = []

    for targetgroup in set(targetgroup_list):
        HealthyHost_metrcis.append(["AWS/NetworkELB", "UnHealthyHostCount", "TargetGroup",
                                    targetgroup, "LoadBalancer", arn])
        HealthyHost_metrcis.append(["AWS/NetworkELB", "HealthyHostCount", "TargetGroup",
                                    targetgroup, "LoadBalancer", arn])

    body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": [
                        ["AWS/NetworkELB", "ProcessedBytes", "LoadBalancer", "%s" % arn]
                    ],
                    "region": region,
                    "title": "ProcessedBytes"
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/NetworkELB", "ActiveFlowCount", "LoadBalancer", "%s" % arn],
                        [".", "NewFlowCount", ".", "."],
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": region,
                    "title": "FlowCount"
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 12,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": [
                        ["AWS/NetworkELB", "TCP_Client_Reset_Count", "LoadBalancer", "%s" % arn],
                        [".", "TCP_ELB_Reset_Count", ".", "."],
                        [".", "TCP_Target_Reset_Count", ".", "."]
                    ],
                    "region": region,
                    "title": "TCP_Reset"
                }
            },
            {
                "type": "metric",
                "x": 12,
                "y": 6,
                "width": 12,
                "height": 6,
                "properties": {
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": HealthyHost_metrcis,
                    "region": region,
                    "title": "HealthyHost"
                }
            }
        ]
    }

    response = cloudwatch.put_dashboard(
        DashboardName='AWS_ELB_%s' % instance_name,
        DashboardBody=json.dumps(body)
    )
    print(response)

def lambda_handler(event, context):
    # TODO implement

    print(event)
    detail = event.get('detail', {})
    event_source = detail.get('eventSource')
    event_name = detail.get('eventName')
    event_response = detail.get('responseElements', {})

    if event_source == 'ec2.amazonaws.com':
        if event_name == 'RunInstances':
            instances = event_response.get('instancesSet', {})
            for item in instances.get('items', []):
                print(item)
                instance_id = item.get('instanceId')
                if instance_id:
                    add_ec2_alarm(instance_id)
                    add_ec2_ebs_alarm(instance_id)
                    add_ec2_dashboard(instance_id)

    elif event_source == 'rds.amazonaws.com':
        if event_name == 'CreateDBInstance':
            dBInstanceArn = event_response.get('dBInstanceArn')
            dBInstanceIdentifier = event_response.get('dBInstanceIdentifier')
            engine = event_response.get('engine')
            if engine == 'mysql':
                print(dBInstanceArn, dBInstanceIdentifier)
                add_mysql_alarm(dBInstanceIdentifier)
                add_mysql_dashboard(dBInstanceIdentifier)
    elif event_source == 'elasticache.amazonaws.com':
        if event_name == 'CreateReplicationGroup':
            group_id = event_response.get('replicationGroupId')
            clusters = event_response.get('memberClusters')
            for c in clusters:
                add_redis_alarm(c)

            add_redis_dashboard(clusters, group_id)
    elif event_source == 'elasticloadbalancing.amazonaws.com':
        if event_name == 'CreateLoadBalancer':
            loadBalancers = event_response.get('loadBalancers')
            for loadbalancer in loadBalancers:
                instance_name = loadbalancer.get('loadBalancerName')
                instance_type = loadbalancer.get('type')
                instance_arn = loadbalancer.get('loadBalancerArn')
    
                if instance_type == 'network':
                    add_elb_alarm(instance_arn, instance_name)
                    add_elb_dashboard(instance_arn, instance_name)

    return {
        'statusCode': 200,
        'body': json.dumps('add success.')
    }
