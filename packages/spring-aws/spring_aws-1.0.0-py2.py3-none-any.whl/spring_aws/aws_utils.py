#!/usr/bin/env python

import boto3
import pprint
import tabulate

# Setup AWS Clients and Resources
ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')


## HELPER FUNCTIONS ##

# Get the host instance_id based on the tagged instance name (i.e. 'awscvm004')
def get_host_instance_id(instance_name):
    ec2_client = boto3.client('ec2')
    print ("Instance name = " + instance_name)
    instance = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [ instance_name ]}])
    return instance['Reservations'][0]['Instances'][0]['InstanceId']

# Get public ip adddress based on instance hostname
def get_host_ip(instance_id):
    return ec2.Instance(instance_id).public_ip_address

def list_host_names(instance_list):
    instance_ids=[]
    for instance in instance_list['Reservations']:
        for host in instance['Instances']:
            print(get_tag_value('Name',get_instance_tags(host['InstanceId'])) + " - " + get_tag_value('description',get_instance_tags(host['InstanceId'])))
            instance_ids.append(host['InstanceId'])
    return instance_ids

def get_instance_tags(instance_id):
    return ec2.Instance(instance_id).tags

def get_tag_value( key_name, tag_array ):
    for tag in tag_array:
        if isinstance( tag, dict ):
            if tag['Key'] == key_name:
                return tag['Value']
    return ""

# Specify list of tags and get matched hosts (i.e. get_filtered_instances({'env': 'prod', 'type': 'docker'}))
def get_filtered_instances(tag_dict):
    filters=[]
    for key,value in tag_dict.items():
        filters.append({'Name': 'tag:'+key, 'Values':[value]})
    return ec2_client.describe_instances(Filters=filters)

def attach_multiple_tags(instance_id_list,tag_name,tag_value):
    for id in instance_id_list:
        ec2.Instance(id).create_tags(
            DryRun=False,
            Tags=[
                {
                    'Key': tag_name,
                    'Value': tag_value
                },
            ]
        )

def show_all_instances():
    all_hosts = ec2_client.describe_instances()
    table = []
    header = ['Instance ID','Name','State','ASG','Public IP','Private IP','AZ']

    for result in all_hosts['Reservations']:
        for host in result['Instances']:
            instance = ec2.Instance(host['InstanceId'])
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
    print (tabulate.tabulate(sorted(table, key=lambda ins: ins[1]),header,tablefmt='orgtbl'))

def reformat_dict(dicta):
    for key,value in dicta.items():
        print("Key: " + key + ", Value: " + value)


def shutdown_nodes(instance_id_list):
    for id in instance_id_list:
        ec2.Instance(id).stop(DryRun=False)

if __name__=="__main__":
    show_all_instances()
