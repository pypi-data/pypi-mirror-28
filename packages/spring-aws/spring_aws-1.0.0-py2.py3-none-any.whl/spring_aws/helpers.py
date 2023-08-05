import boto3
from pprint import pprint

client = boto3.client('elbv2')
ec2client = boto3.client('ec2')
acmclient = boto3.client('acm')

vpc_id = ec2client.describe_vpcs()['Vpcs'][0]['VpcId']

# load_balancer_name='pub-dev-elb'
# target_group_name='pub-dev-http'
# domain_name='dev.pub.spring.co.nz'
# cert_idempotency_token='pubdevrequest'

load_balancer_name='mi-dev-elb'
target_group_name='mi-dev-http'
domain_name='dev.mi.spring.co.nz'
cert_idempotency_token='midevrequest'

load_balancer_name='acceleration-stage-elb'
target_group_name='acceleration-stage-http'
domain_name='stage.acceleration.spring.co.nz'
cert_idempotency_token='stage.acceleration.spring.co.nz'

load_balancer_name='acceleration-dev-elb'
target_group_name='acceleration-dev-http'
domain_name='dev.acceleration.spring.co.nz'
cert_idempotency_token='dev.acceleration.spring.co.nz'

load_balancer_name='calendar-dev-elb'
target_group_name='calendar-dev-http'
domain_name='dev.calendar.spring.co.nz'
cert_idempotency_token='calendardevrequest'

# Filter list of security group and return id of public web sg
sgs = ec2client.describe_security_groups(Filters = [ { 'Name': 'group-name', 'Values': ['Public Web'] } ])
sg_id = sgs['SecurityGroups'][0]['GroupId']

lb_create_response = client.create_load_balancer(
    Name=load_balancer_name,
    Subnets=[
        'subnet-6794b121',
        'subnet-5da1e62a',
        'subnet-8b247dee'
    ],
    SecurityGroups=[
        sg_id,
    ],
    Scheme='internet-facing'
)

loadbalancer_arn = lb_create_response['LoadBalancers'][0]['LoadBalancerArn']
loadbalancer_dns = lb_create_response['LoadBalancers'][0]['DNSName']

## Use this one if you don't capture it from the response
#loadbalancer_arn = client.describe_load_balancers(Names=['mi-dev-elb'])['LoadBalancers'][0]['LoadBalancerArn']

tg_create_response = client.create_target_group(
    Name=target_group_name,
    Protocol='HTTP',
    Port=8094,
    VpcId=vpc_id,
    HealthCheckProtocol='HTTP',
    HealthCheckPort='8094',
    HealthCheckPath='/',
    HealthCheckIntervalSeconds=10,
    HealthCheckTimeoutSeconds=5,
    HealthyThresholdCount=3,
    UnhealthyThresholdCount=2
)

target_group_arn = tg_create_response['TargetGroups'][0]['TargetGroupArn']

## Use this one if you don't capture the response
#target_group_arn = client.describe_target_groups(Names=['mi-dev-http'])['TargetGroups'][0]['TargetGroupArn']

# Create SSL Request
cert_create_response = acmclient.request_certificate(
    DomainName=domain_name,
    IdempotencyToken=cert_idempotency_token
)
certificate_arn = cert_create_response['CertificateArn']

# Create ELB Listener Object

listener_response = client.create_listener(
    LoadBalancerArn=loadbalancer_arn,
    Protocol='HTTPS',
    Port=443,
    Certificates=[
        {
            'CertificateArn': certificate_arn
        },
    ],
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group_arn
        },
    ]
)
listener_arn=listener_response['Listeners'][0]['ListenerArn']

# Use this one if you don't capture the response
#listener_arn=client.describe_listeners(LoadBalancerArn=loadbalancer_arn)['Listeners'][0]['ListenerArn']

## Add hosts into ELB.

# Get Dev Host Instance Id

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

certificate_arn = 'arn:aws:acm:ap-southeast-2:489528272533:certificate/959d055c-fabe-405e-8abf-3486b5529b61'

# Delete TG's
loadbalancer_arn = client.describe_load_balancers(Names=[load_balancer_name])['LoadBalancers'][0]['LoadBalancerArn']
listener_arn=client.describe_listeners(LoadBalancerArn=loadbalancer_arn)['Listeners'][0]['ListenerArn']
target_group_arn = client.describe_target_groups(Names=[target_group_name])['TargetGroups'][0]['TargetGroupArn']

delete_listener_response = client.delete_listener(
    ListenerArn=listener_arn
)

delete_tg_response = client.delete_target_group(
    TargetGroupArn=target_group_arn
)

def get_certificate_arn(domain_name):
    certs = acmclient.list_certificates()
    for cert in certs['CertificateSummaryList']:
        if cert['DomainName'] == domain_name:
            return cert['CertificateArn']
            break

certificate_arn = get_certificate_arn('dev.calendar.spring.co.nz') 


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
    UnhealthyThresholdCount=2
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
