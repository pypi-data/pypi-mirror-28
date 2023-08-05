import boto3
import time
import json
import sys
import re
from tabulate import tabulate

"""
Python AWS utilities that are used across different
applications and scripts
"""

## AWS Service Clients
elbclient = boto3.client('elbv2')
ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')
acmclient = boto3.client('acm')
r52client = boto3.client('route53')
# Regiion is set to us-east-1 because that's where route53 creates it's health checks by default. 
cw_client = boto3.client('cloudwatch', region_name='us-east-1')
cw_resource = boto3.resource('cloudwatch', region_name='us-east-1')

##-- Cloudwatch helpers --##

def get_alarms(env):
    alarms = cw_client.describe_alarms()
    alarm_list = []
    for alarm in alarms['MetricAlarms']:
        if re.match(r".*{}.*".format(env),alarm['AlarmName']):
            print(alarm['AlarmName'])
            alarm_list.append(alarm['AlarmName'])
    return alarm_list


def modify_alerts(alarm_list,action):
    for alarm_name in alarm_list:
        alert = cw_resource.Alarm(alarm_name)
        if action == "enable":
            print("Enabling actions for - {}".format(alarm_name))
            alert.enable_actions()
        elif action == "disable":
            print("Disabling actions for - {}".format(alarm_name))
            alert.disable_actions()


##-- EC2 Related Helpers --##

def get_host_ip(instance_id):
    return ec2client.Instance(instance_id).public_ip_address


def get_instance_id(instance_name):
   instances = ec2client.describe_instances(Filters=[{'Name': 'tag-value', 'Values':[ instance_name ]}]) 
   return instances['Reservations'][0]['Instances'][0]['InstanceId']


# Retrieve a list of instance id's from an ec2 reservation list
def get_instance_id_from_manifest( instance_json ):
    instances = []

    for reservation in instance_json['Reservations']:
        for instance in reservation['Instances']:
            instances = instances + [ instance['InstanceId'] ]

    return instances


def get_instance_tags(instance_id):
    return ec2client.Instance(instance_id).tags


def get_tag_value( key_name, tag_array ):
    for tag in tag_array:
        if isinstance( tag, dict ):
            if tag['Key'] == key_name:
                return tag['Value']
    return ""


def list_host_names(instance_list):
    instance_ids=[]
    for instance in instance_list['Reservations']:
        for host in instance['Instances']:
            print(get_tag_value('Name',get_instance_tags(host['InstanceId'])) + " - " + get_tag_value('description',get_instance_tags(host['InstanceId'])))
            instance_ids.append(host['InstanceId'])
    return instance_ids


# Specify list of tags and get matched hosts (i.e. get_filtered_instances({'env': 'prod', 'type': 'docker'}))
def get_filtered_instances( tag_dict ):
    filters=[]
    for key,value in tag_dict.items():
        filters.append({'Name': 'tag:'+key, 'Values':[value]})
    return ec2client.describe_instances(Filters=filters)


def get_instance_state(instance_id):
    instance = ec2resource.Instance(instance_id)
    return instance.state


def get_vpc_id(cidr_block=None):
    vpcs = ec2client.describe_vpcs()['Vpcs']
    if cidr_block:
        for vpc in vpcs:
            if vpc['CidrBlock'] == cidr_block:
                return vpc['VpcId']
                break
    else:
        return vpcs[0]['VpcId']


def get_subnet_list():
    subnet_list = []
    subnets = ec2client.describe_subnets()['Subnets']
    for subnet in subnets:
        subnet_list.append(subnet['SubnetId'])
    return subnet_list


def get_security_group_id(security_group_name):
    security_groups = ec2client.describe_security_groups(
        Filters = [
            {
                'Name': 'group-name',
                'Values': [ security_group_name ]
            }
        ])
    for security_group in security_groups['SecurityGroups']:
        if security_group_name == security_group['GroupName']:
            return security_group['GroupId']


def attach_multiple_tags(instance_id_list,tag_name,tag_value):
    for id in instance_id_list:
        ec2client.Instance(id).create_tags(
            DryRun=False,
            Tags=[
                {
                    'Key': tag_name,
                    'Value': tag_value
                },
            ]
        )


##-- ELB Related Helpers -- ##

def create_load_balancer(load_balancer_name,subnet_list,security_group_list,scheme='internet-facing'):
    response = elbclient.create_load_balancer(
        Name=load_balancer_name,
        Subnets=subnet_list,
        SecurityGroups=security_group_list,
        Scheme=scheme
    )
    return response['LoadBalancers'][0]['LoadBalancerArn']


def get_load_balancer_arn(load_balancer_name):
    response = elbclient.describe_load_balancers(
            Names=[load_balancer_name]
            )
    return response['LoadBalancers'][0]['LoadBalancerArn']


def get_load_balancer_dns(load_balancer_arn):
    response = elbclient.describe_load_balancers(
            LoadBalancerArns=[
                load_balancer_arn
            ]
        )
    return response['LoadBalancers'][0]['DNSName']


def get_load_balancer_target_group_arns(load_balancer_arn):
    response = elbclient.describe_target_groups(LoadBalancerArn=load_balancer_arn)
    target_groups = response['TargetGroups']
    tg_arns = []
    for tg in target_groups:
        tg_arns.append(tg['TargetGroupArn'])
    return tg_arns 


def create_target_group(target_group_name,protocol,port,vpc_id,http_code):
    response = elbclient.create_target_group(
        Name=target_group_name,
        Protocol=protocol,
        Port=port,
        VpcId=vpc_id,
        HealthCheckProtocol=protocol,
        HealthCheckPort=str(port),
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=10,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=3,
        UnhealthyThresholdCount=2,
        Matcher={
            'HttpCode': http_code
        }
    )
    return response['TargetGroups'][0]['TargetGroupArn']


def create_listener(loadbalancer_arn,protocol,port,certificate_arn,target_group_arn):

    if protocol == 'HTTPS' and certificate_arn:
        certificate_list = [ { 'CertificateArn': certificate_arn} ]
    elif protocol == 'HTTPS' and not certificate_arn:
        print("If setting up an HTTPS listener, there must be an associated SSL Certificate")
        sys.exit(1)
    else:
        certificate_list = []

    response = elbclient.create_listener(
        LoadBalancerArn=loadbalancer_arn,
        Protocol=protocol,
        Port=port,
        Certificates=certificate_list,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            },
        ]
    )
    return response['Listeners'][0]['ListenerArn']


def add_instance_to_target_group(instance_id,target_group_arn):
    response = elbclient.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id,
            },
        ],
    )
    return response


def remove_instance_from_target_group(instance_id,target_group_arn):
    response = elbclient.deregister_targets(
        TargetGroupArn=target_group_arn,
        Targets=[
            {
                'Id': instance_id,
            },
        ],
    )
    return response


def add_instance_to_lb(load_balancer_name,instance_name):

    instance_id = get_instance_id(instance_name)
    load_balancer_arn = get_load_balancer_arn(load_balancer_name)
    target_groups = get_load_balancer_target_group_arns(load_balancer_arn)

    for tg_arn in target_groups:
        add_instance_to_target_group(instance_id,tg_arn)


def remove_instance_from_lb(load_balancer_name,instance_name):

    instance_id = get_instance_id(instance_name)
    load_balancer_arn = get_load_balancer_arn(load_balancer_name)
    target_groups = get_load_balancer_target_group_arns(load_balancer_arn)

    for tg_arn in target_groups:
        remove_instance_from_target_group(instance_id,tg_arn)


##-- Certificate Related Helpers --##


def check_for_certificate(domain_name):
    response = acmclient.list_certificates()
    for cert in response['CertificateSummaryList']:
        if cert['DomainName'] == domain_name:
            return cert['CertificateArn']


def request_certificate(domain_name,idempotency_token=None):
    if not idempotency_token: idempotency_token = "".join(domain_name.split('.'))
    response = acmclient.request_certificate(
        DomainName=domain_name,
        IdempotencyToken=idempotency_token
    )
    return response['CertificateArn']


def wait_for_certificate_approval(certificate_arn,max_tries=20,delay_time=15):
    certificate_state='unset'
    tries = 0

    while (certificate_state != 'ISSUED') and (tries < max_tries):
        tries += 1
        print("Validating Certificate, attempt {} of {}".format(tries,max_tries))
        certificate_state = acmclient.describe_certificate(CertificateArn=certificate_arn)['Certificate']['Status']
        time.sleep(delay_time)
        if certificate_state == 'ISSUED': print("Certificate Successfully Validated")

        if tries >= max_tries:
            print("Max attemps reached. Script exiting. Rerun script when certificate has been approved.")


## Route53 Related Helpers

def get_hosted_zone(domain_name):
    for zone in r52client.list_hosted_zones()['HostedZones']:
        if (domain_name == zone['Name']) or (domain_name + "." == zone['Name']):
            return zone['Id'].split('/').pop()
            break


def create_dns_cname(hosted_zone_id,domain_name,target):
    response = r52client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'CNAME',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': target
                            },
                        ]
                    }
                },
            ]
        }
    )
    return response


def update_dns_a_record(hosted_zone_id,domain_name,target):
    response = r52client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': target
                            },
                        ]
                    }
                },
            ]
        }
    )
    return response


def update_dns_alias_record(hosted_zone_id,domain_name,target):
    response = r52client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': 'Z1GM3OXH4ZPM65',
                            'DNSName': target,
                            'EvaluateTargetHealth': False
                        }
                    }
                },
            ]
        }
    )
    return response


## Misc - General Helpers

def show_all_instances():
    all_hosts = ec2_client.describe_instances()
    table = []
    header = ['Instance ID','Name','State','ASG','Public IP','Private IP','AZ']

    for result in all_hosts['Reservations']:
        for host in result['Instances']:
            instance = ec2client.Instance(host['InstanceId'])
            host_list = [
                instance.instance_id,
                get_tag_value('Name',instance.tags),
                instance.state['Name'],
                get_tag_value( 'aws:autoscaling:groupName', instance.tags ),
                instance.public_ip_address,
                instance.private_ip_address,
                instance.placement["AvailabilityZone"],
            ]
            table.append(host_list)
    print (tabulate(sorted(table, key=lambda ins: ins[1]),header,tablefmt='orgtbl'))