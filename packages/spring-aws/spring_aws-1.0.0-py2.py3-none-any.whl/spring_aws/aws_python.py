import boto3

### Defining alternative credentials ###

# client = boto3.client('s3', aws_access_key_id='AKIAIQRYWFNLUCBBX26Q', aws_secret_access_key='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' )
# s3 = boto3.resource('s3', aws_access_key_id='AKIAIQRYWFNLUCBBX26Q', aws_secret_access_key='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' )
# s3_staging = boto3.resource('s3', aws_access_key_id='AKIAIZOZPE7NB2D4TROA', aws_secret_access_key='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' )

# Setup EC2 Client
awsec2 = boto3.client('ec2')

# Get the Instance Id of instance, based on Tag Name
gibsonprod = awsec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['awscvm005']}])['Reservations'][0]['Instances'][0]['InstanceId']

# Setup the Instance object for the particular instance
instance = ec2.Instance(gibsonprod)

# Stop Instance prior to snapshot-ing volume
instance.stop(DryRun=False)

# Get list of device mappings and extract volume ID
volid=instance.block_device_mappings[0]['Ebs']['VolumeId']

# Setup Volume object for target volume
volume = ec2.Volume(volid)

# Initiate Snapshot
volume.create_snapshot()

ec2.Snapshot(id='snap-52b52f61')

snapshot = ec2.Snapshot('snap-52b52f61')
snapshot.state
snapshot.progress


response = awsec2.create_volume(Size=200, SnapshotId='snap-52b52f61', AvailabilityZone=volume.availability_zone,VolumeType='gp2',Encrypted=False)
new_vol = ec2.Volume(response["VolumeId"])

volume.detach_from_instance(InstanceId=gibsonprod,Device='/dev/sda1')


new_vol.attach_to_instance(InstanceId=gibsonprod,Device='/dev/sda1')

instance.start(DryRun=False)

instance.public_dns_name


volume.delete(DryRun=False)




################ Listing Production Docker Instances ################

client = boto3.client('ec2')

# Get list of instances tagged with both env=prod and type=docker
prod_docker_hosts = client.describe_instances(Filters=[{'Name':'tag:env','Values':['prod']},{'Name':'tag:type','Values':['docker']}])

# List the instance ids of the instances filtered above
for instance in prod_docker_hosts['Reservations']:
    print instance['Instances'][0]['InstanceId']


def get_ips(env,tag_name):
    hosts = client.describe_instances(Filters=[{'Name':'tag:env','Values':[env]},{'Name':'tag:type','Values':[tag_name]}])

    # List the instance ids of the instances filtered above
    for instance in hosts['Reservations']:
        print instance['Instances'][0]['PublicIpAddress']

# Add those ids to a list
insids = []
for instance in prod_docker_hosts['Reservations']:                                                                                                                                                                                                                                                                                                                                                                                            
    insids.append(instance['Instances'][0]['InstanceId'])

# Attach Tags to Production Hosts
for id in insids:
    instance = ec2.Instance(id)
    instance.create_tags(
        DryRun=False,
        Tags=[
            {
                'Key': 'presto',
                'Value': ''
            },
        ]
    )


####### Report on ELB Status ######
import pprint

pprint.pprint(client.describe_instance_health(LoadBalancerName='http-wises-stage-frontend')['InstanceStates'])


## Create Load Balancer for Presto

response = client.create_load_balancer(
    LoadBalancerName='http-presto-frontend',
    Listeners=[
        {
            'Protocol': 'tcp',
            'LoadBalancerPort': 443,
            'InstanceProtocol': 'tcp',
            'InstancePort': 443
        },
        {
            'Protocol': 'HTTP',
            'LoadBalancerPort': 80,
            'InstanceProtocol': 'HTTP',
            'InstancePort': 80
        },
    ],
    Subnets=[
        'subnet-1848306f',
        'subnet-875c03c1',
        'subnet-baecbfdf',
    ],
    SecurityGroups=[
        'sg-2e3ed24a'
    ],
    Scheme='internet-facing',
    Tags=[
        {
            'Key': 'presto',
            'Value': ''
        },
    ]
)

response = client.enable_availability_zones_for_load_balancer(
    LoadBalancerName='http-presto-frontend',
    AvailabilityZones=[
        'ap-southeast-2b',
        'ap-southeast-2a',
        'ap-southeast-2c',
    ]
)

response = client.configure_health_check(
    LoadBalancerName='http-presto-frontend',
    HealthCheck={
        'Target': 'TCP:443',
        'Interval': 30,
        'Timeout': 5,
        'UnhealthyThreshold': 2,
        'HealthyThreshold': 10
    }
)

for id in insids:
    client.register_instances_with_load_balancer(
        LoadBalancerName='http-presto-frontend',
        Instances=[
            {
                'InstanceId': id
            },
        ]
    )


## Register and Deregister Instances from Load Balancer

client = boto3.client('elb')
elb_name='http-presto-stage-frontend'
instance_name='awscvm016'
ec2_client = boto3.client('ec2')

# Get the Instance Id of instance, based on Tag Name
instance_id = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])['Reservations'][0]['Instances'][0]['InstanceId']


# Remove Instance
response = client.deregister_instances_from_load_balancer(
    LoadBalancerName=elb_name,
    Instances=[
        {
            'InstanceId': instance_id
        },
    ]
)


# Add Instance
response = client.register_instances_with_load_balancer(
    LoadBalancerName=elb_name,
    Instances=[
        {
            'InstanceId': instance_id
        },
    ]
)


def elb_controller(instance_name, elb_name, action):
    client = boto3.client('elb')
    ec2_client = boto3.client('ec2')
    instance = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name ]}])
    instance_id = instance['Reservations'][0]['Instances'][0]['InstanceId']

    # Remove Instance
    if action == "remove":
        response = client.deregister_instances_from_load_balancer(
            LoadBalancerName=elb_name,
            Instances=[
                {
                    'InstanceId': instance_id
                },
            ]
        )
    elif action == "add":
        # Add Instance
        response = client.register_instances_with_load_balancer(
            LoadBalancerName=elb_name,
            Instances=[
                {
                    'InstanceId': instance_id
                },
            ]
        )
    elif action == "status":
        print "Current Status:"
    else:
        print "Incorrect action (add|remove)"

    pprint.pprint(client.describe_instance_health(LoadBalancerName=elb_name)['InstanceStates'])


## Changing Instance Type


gibprod.modify_attribute(DryRun=False,Attribute='instanceType',InstanceType={'Value': 'm4.large'})


# Get EIP Address into VPC
client.allocate_address(DryRun=False,Domain='vpc')
# Assign it to host
client.associate_address(DryRun=False,InstanceId='i-3110e0e0',AllocationId='eipalloc-2e7fec4b',AllowReassociation=False)



# def elb_controller(instance_name, elb_name, action):
#     instance = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
#     instance_id = instance['Reservations'][0]['Instances'][0]['InstanceId']

#     # Remove Instance
#     if action == "remove":
#         response = client.deregister_instances_from_load_balancer(
#             LoadBalancerName=elb_name,
#             Instances=[
#                 {
#                     'InstanceId': instance_id
#                 },
#             ]
#         )
#     elif action == "add":
#         # Add Instance
#         response = client.register_instances_with_load_balancer(
#             LoadBalancerName=elb_name,
#             Instances=[
#                 {
#                     'InstanceId': instance_id
#                 },
#             ]
#         )
#     elif action == "status":
#         print "Current Status:"
#     else:
#         print "Incorrect action (add|remove)"

#     pprint.pprint(client.describe_instance_health(LoadBalancerName=elb_name)['InstanceStates'])
