import boto3
from pprint import pprint

client = boto3.client('elbv2')
ec2client = boto3.client('ec2')
acmclient = boto3.client('acm')

vpc_id = ec2client.describe_vpcs()['Vpcs'][0]['VpcId']

load_balancer_name='mi-dev-elb'
target_group_name='mi-dev-http'
target_group_name='mi-dev-http-redirect'
domain_name='dev.mi.spring.co.nz'
cert_idempotency_token='midevrequest'

load_balancer_name='acceleration-stage-elb'
target_group_name='acceleration-stage-http-redirect'
domain_name='stage.acceleration.spring.co.nz'
cert_idempotency_token='stage.acceleration.spring.co.nz'

load_balancer_name='acceleration-dev-elb'
target_group_name='acceleration-dev-http-redirect'
domain_name='dev.acceleration.spring.co.nz'
cert_idempotency_token='dev.acceleration.spring.co.nz'

load_balancer_name='calendar-dev-elb'
target_group_name='calendar-dev-http-redirect'
domain_name='dev.calendar.spring.co.nz'
cert_idempotency_token='calendardevrequest'


loadbalancer_arn = client.describe_load_balancers(Names=[load_balancer_name])['LoadBalancers'][0]['LoadBalancerArn']
listener_arn=client.describe_listeners(LoadBalancerArn=loadbalancer_arn)['Listeners'][0]['ListenerArn']
target_group_arn = client.describe_target_groups(Names=[target_group_name])['TargetGroups'][0]['TargetGroupArn']

tg_create_response = client.create_target_group(
    Name=target_group_name,
    Protocol='HTTP',
    Port=8079,
    VpcId=vpc_id,
    HealthCheckProtocol='HTTP',
    HealthCheckPort='8079',
    HealthCheckPath='/',
    HealthCheckIntervalSeconds=10,
    HealthCheckTimeoutSeconds=5,
    HealthyThresholdCount=3,
    UnhealthyThresholdCount=2,
    Matcher={
        'HttpCode': '301' 
    }
)

target_group_arn = tg_create_response['TargetGroups'][0]['TargetGroupArn']

listener_response = client.create_listener(
    LoadBalancerArn=loadbalancer_arn,
    Protocol='HTTP',
    Port=80,
    Certificates=[],
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group_arn
        },
    ]
)
listener_arn=listener_response['Listeners'][0]['ListenerArn']

ec2_response = ec2client.describe_instances(Filters=[{'Name': 'tag-value', 'Values':[ 'dev-1' ]}])
dev_instance_id = ec2_response['Reservations'][0]['Instances'][0]['InstanceId']

tg_add_response = client.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=[
        {
            'Id': dev_instance_id,
        },
    ],
)

def get_load_balancer_arn(lb_name):
    return client.describe_load_balancers(Names=[lb_name])['LoadBalancers'][0]['LoadBalancerArn']


# Change Log Group Retention

client = boto3.clent('logs')

"""
Set all log groups to 90 day retention
"""
for group in client.describe_log_groups()['logGroups']:
    response = client.put_retention_policy(
        logGroupName = group['logGroupName'],
        retentionInDays=90
    )
    print(response)