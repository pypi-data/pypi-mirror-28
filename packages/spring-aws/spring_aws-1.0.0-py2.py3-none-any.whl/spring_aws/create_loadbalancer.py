import sys
import time
import boto3
import argparse
import utils

client = boto3.client('elbv2')
ec2client = boto3.client('ec2')
acmclient = boto3.client('acm')
r52client = boto3.client('route53')

## If a CIDR block is specified, then return the matching VPC, otherwise return the first VPC in the array - typically the default.
#def get_vpc_id(cidr_block=None):
#    vpcs = ec2client.describe_vpcs()['Vpcs']
#    if cidr_block:
#        for vpc in vpcs:
#            if vpc['CidrBlock'] == cidr_block:
#                return vpc['VpcId']
#                break
#    else:
#        return vpcs[0]['VpcId']
#    
#def get_subnet_list():
#    subnet_list = []
#    subnets = ec2client.describe_subnets()['Subnets']
#    for subnet in subnets:
#        subnet_list.append(subnet['SubnetId'])
#    return subnet_list
#
#def get_security_group_id(security_group_name):
#    security_groups = ec2client.describe_security_groups(
#        Filters = [
#            {
#                'Name': 'group-name',
#                'Values': [ security_group_name ]
#            }
#        ])
#    for security_group in security_groups['SecurityGroups']:
#        if security_group_name == security_group['GroupName']:
#            return security_group['GroupId']
#
#def create_load_balancer(load_balancer_name,subnet_list,security_group_list,scheme='internet-facing'):
#    response = client.create_load_balancer(
#        Name=load_balancer_name,
#        Subnets=subnet_list,
#        SecurityGroups=security_group_list,
#        Scheme=scheme
#    )
#    return response['LoadBalancers'][0]['LoadBalancerArn']
#
#def get_load_balancer_dns(loadbalancer_arn):
#    response = client.describe_load_balancers(
#            LoadBalancerArns=[
#                loadbalancer_arn
#            ]
#        )
#    return response['LoadBalancers'][0]['DNSName']
#
#def create_target_group(target_group_name,protocol,port,vpc_id,http_code):
#    response = client.create_target_group(
#        Name=target_group_name,
#        Protocol=protocol,
#        Port=port,
#        VpcId=vpc_id,
#        HealthCheckProtocol=protocol,
#        HealthCheckPort=str(port),
#        HealthCheckPath='/',
#        HealthCheckIntervalSeconds=10,
#        HealthCheckTimeoutSeconds=5,
#        HealthyThresholdCount=3,
#        UnhealthyThresholdCount=2,
#        Matcher={
#            'HttpCode': http_code
#        }
#    )
#    return response['TargetGroups'][0]['TargetGroupArn']
#
#def check_for_certificate(domain_name):
#    response = acmclient.list_certificates()
#    for cert in response['CertificateSummaryList']:
#        if cert['DomainName'] == domain_name:
#            return cert['CertificateArn']
#
#
#def request_certificate(domain_name,idempotency_token=None):
#    if not idempotency_token: idempotency_token = "".join(domain_name.split('.'))
#    response = acmclient.request_certificate(
#        DomainName=domain_name,
#        IdempotencyToken=idempotency_token
#    )
#    return response['CertificateArn']
#
#def wait_for_certificate_approval(certificate_arn,max_tries=20,delay_time=15):
#    certificate_state='unset'
#    tries = 0
#
#    while (certificate_state != 'ISSUED') and (tries < max_tries):
#        tries += 1
#        print("Validating Certificate, attempt {} of {}".format(tries,max_tries))
#        certificate_state = acmclient.describe_certificate(CertificateArn=certificate_arn)['Certificate']['Status']
#        time.sleep(delay_time)
#        if certificate_state == 'ISSUED': print("Certificate Successfully Validated")
#
#        if tries >= max_tries:
#            print("Max attemps reached. Script exiting. Rerun script when certificate has been approved.")
#
#def create_listener(loadbalancer_arn,protocol,port,certificate_arn,target_group_arn):
#
#    if protocol == 'HTTPS' and certificate_arn:
#        certificate_list = [ { 'CertificateArn': certificate_arn} ]
#    elif protocol == 'HTTPS' and not certificate_arn:
#        print("If setting up an HTTPS listener, there must be an associated SSL Certificate")
#        sys.exit(1)
#    else:
#        certificate_list = []
#
#    response = client.create_listener(
#        LoadBalancerArn=loadbalancer_arn,
#        Protocol=protocol,
#        Port=port,
#        Certificates=certificate_list,
#        DefaultActions=[
#            {
#                'Type': 'forward',
#                'TargetGroupArn': target_group_arn
#            },
#        ]
#    )
#    return response['Listeners'][0]['ListenerArn']
#
#def get_instance_id(instance_name):
#   instances = ec2client.describe_instances(Filters=[{'Name': 'tag-value', 'Values':[ instance_name ]}]) 
#   return instances['Reservations'][0]['Instances'][0]['InstanceId'] 
#
#def add_instance_to_target_group(instance_id,target_group_arn):
#    response = client.register_targets(
#        TargetGroupArn=target_group_arn,
#        Targets=[
#            {
#                'Id': instance_id,
#            },
#        ],
#    )
#    return response
#
#def get_hosted_zone(domain_name):
#    for zone in r52client.list_hosted_zones()['HostedZones']:
#        if (domain_name == zone['Name']) or (domain_name + "." == zone['Name']):
#            return zone['Id'].split('/').pop()
#            break
#
#def create_dns_cname(hosted_zone_id,domain_name,target):
#    response = r52client.change_resource_record_sets(
#        HostedZoneId=hosted_zone_id,
#        ChangeBatch={
#            'Changes': [
#                {
#                    'Action': 'UPSERT',
#                    'ResourceRecordSet': {
#                        'Name': domain_name,
#                        'Type': 'CNAME',
#                        'TTL': 300,
#                        'ResourceRecords': [
#                            {
#                                'Value': target
#                            },
#                        ]
#                    }
#                },
#            ]
#        }
#    )
#    return response

def parse_args():
  parser = argparse.ArgumentParser(description='Deploy a load balancer') 
  parser.add_argument('-n','--lb-name',required=True,help='The name of the load balancer to be created')
  parser.add_argument('-t','--target-group',required=True,help='The name of the target group to be created')
  parser.add_argument('-d','--domain',required=True,help='The domain name for the certificate')
  parser.add_argument('-c','--certname',required=True,help='Certificate to use for the loadbalancer')
  parser.add_argument('-p','--port',type=int,required=True,help='The listening port for the associated listener')
  parser.add_argument('-r','--redirect-port',type=int,required=True,help='The listening port for the associated http redirect listener')
  parser.add_argument('-i','--instances',nargs='+',required=True,help='A list of instances to add to the load balancer')
  return parser.parse_args()

def main():
    vpc_id = utils.get_vpc_id()
    print("VPC ID = {}".format(vpc_id))
    subnet_list = utils.get_subnet_list()
    load_balancer_security_group=utils.get_security_group_id('Public Web')

    # Create Resources
    print("Creating LoadBalaner")
    lb_arn = utils.create_load_balancer(args.lb_name,subnet_list,[load_balancer_security_group])
    print("Load Balancer Created with dns of {}".format(utils.get_load_balancer_dns(lb_arn)))
    print("Creating Target Groups")
    tg_arn = utils.create_target_group(args.target_group,'HTTP',args.port,vpc_id,'200')
    redirect_tg_arn   = utils.create_target_group(args.target_group+"-redirect",'HTTP',args.redirect_port,vpc_id,'301')

    print("Retrieving or creating certificate request for {}".format(args.domain))
    if args.certname:
      cert_arn = utils.check_for_certificate(args.certname)
    else:
      cert_arn = utils.check_for_certificate(args.domain)
    if not cert_arn: 
        cert_arn = utils.request_certificate(args.domain)
        utils.wait_for_certificate_approval(cert_arn)

    listener_arn = utils.create_listener(lb_arn,'HTTPS',443,cert_arn,tg_arn)
    redirect_listener_arn = utils.create_listener(lb_arn,'HTTP',80,'',redirect_tg_arn)
    for instance in args.instances:
        instance_id = utils.get_instance_id(instance)
        print("Adding '{}' instance to target groups".format(instance))
        utils.add_instance_to_target_group(instance_id,tg_arn)
        utils.add_instance_to_target_group(instance_id,redirect_tg_arn)

    # Create DNS
    print("Creating DNS record for {}".format(args.domain))
    hosted_zone = utils.get_hosted_zone('spring.co.nz')
    load_balancer_dns = utils.get_load_balancer_dns(lb_arn)
    utils.create_dns_cname(hosted_zone,args.domain,load_balancer_dns)

    print("Load balancer creation completed")

if __name__=="__main__":
    args = parse_args()
    main()
