import boto3
import json

cloudwatch = boto3.client('cloudwatch')


def del_alarm(type, name_prefix):
    print("[delete %s alarm.]" % type)

    rep = cloudwatch.describe_alarms(AlarmNamePrefix=name_prefix, )

    alarm_names = []
    for m in rep.get('MetricAlarms'):
        alarm_names.append(m.get('AlarmName'))

    response = cloudwatch.delete_alarms(
        AlarmNames=alarm_names
    )
    print('alarm_names', alarm_names)
    print('response', response)


def del_dashboards(type, name_prefix):

    print("[delete %s dashboards.]" % type)

    rep = cloudwatch.list_dashboards(DashboardNamePrefix=name_prefix)

    dashboard_names = []
    for m in rep.get('DashboardEntries'):
        dashboard_names.append(m.get('DashboardName'))

    response = cloudwatch.delete_dashboards(
        DashboardNames=dashboard_names
    )
    print('dashboard_names', dashboard_names)
    print('response', response)


def lambda_handler(event, context):
    # TODO implement

    print(event)
    detail = event.get('detail', {})
    event_source = detail.get('eventSource')
    event_name = detail.get('eventName')
    event_response = detail.get('responseElements', {})

    if event_source == 'ec2.amazonaws.com':
        if event_name == 'TerminateInstances':
            instances = event_response.get('instancesSet', {})
            for item in instances.get('items', []):
                instance_id = item.get('instanceId')
                if instance_id:
                    del_alarm('ec2', 'AWS_EC2_%s' % instance_id)
                    del_dashboards('ec2', 'AWS_EC2_%s' % instance_id)

    elif event_source == 'rds.amazonaws.com':
        if event_name == 'DeleteDBInstance':
            dBInstanceIdentifier = event_response.get('dBInstanceIdentifier')
            engine = event_response.get('engine')
            if engine == 'mysql':
                del_alarm('mysql', 'AWS_MYSQL_%s' % dBInstanceIdentifier)
                del_dashboards('mysql', 'AWS_MYSQL_%s' % dBInstanceIdentifier)

    elif event_source == 'elasticache.amazonaws.com':
        if event_name == 'DeleteReplicationGroup':
            group_id = event_response.get('replicationGroupId')
            del_alarm('redis', 'AWS_REDIS_%s' % group_id)
            del_dashboards('redis', 'AWS_REDIS_%s' % group_id)

    elif event_source == 'elasticloadbalancing.amazonaws.com':
        if event_name == 'DeleteLoadBalancer':
            requestParameters = detail.get('requestParameters', {})
            loadBalancerArn = requestParameters.get('loadBalancerArn')
            instance_name = loadBalancerArn.split(':loadbalancer/')[1].split('/')[1]
            del_alarm('elb', 'AWS_ELB_%s' % instance_name)
            del_dashboards('elb', 'AWS_ELB_%s' % instance_name)

    return {
        'statusCode': 200,
        'body': json.dumps('add success.')
    }
