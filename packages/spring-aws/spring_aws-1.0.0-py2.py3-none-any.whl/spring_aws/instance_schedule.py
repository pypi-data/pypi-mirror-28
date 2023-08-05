import utils
import time
import argparse

def parse_args():
  parser = argparse.ArgumentParser(description='Deploy a load balancer') 
  parser.add_argument('-a','--action',required=True,choices=['shutdown','poweron'],help='The action to perform, add or remove instance')
  parser.add_argument('-e','--envs',nargs='+',choices=['dev','stage','prod'],required=True,help='A list of environments to shutdown')
  return parser.parse_args()

APPLICATIONS = {
        'dev': [
            {
                'name': 'calendar-dev',
                'lb_name': 'calendar-dev-elb',
                'domain': 'dev.calendar.spring.co.nz'
            },
            {
                'name': 'acceleration-dev',
                'lb_name': 'acceleration-dev-elb',
                'domain': 'dev.acceleration.spring.co.nz'
            },
            {
                'name': 'bar-dev',
                'lb_name': 'bar-dev-elb',
                'domain': 'dev.bar.spring.co.nz'
            },
            {
                'name': 'mi-dev',
                'lb_name': 'mi-dev-elb',
                'domain': 'dev.mi.spring.co.nz'
            }
        ],
        'stage': [
            {
                'name': 'calendar-stage',
                'lb_name': 'calendar-stage-elb',
                'domain': 'stage.calendar.spring.co.nz'
            },
            {
                'name': 'acceleration-stage',
                'lb_name': 'acceleration-stage-elb',
                'domain': 'stage.acceleration.spring.co.nz'
            },
            {
                'name': 'bar-stage',
                'lb_name': 'bar-stage-elb',
                'domain': 'stage.bar.spring.co.nz'
            }
        ],
}

INSTANCES = {
    'dev': ['dev-1'],
    'stage': ['dev-1'],
    'prod': ['prod-3']
    }

def get_instance_list(env_list,instance_list):
    instances = []
    for env in env_list:
        instances = instances + instance_list[env] 
    print(list(set(instances)))
    return list(set(instances))

def get_instance_id_list(instance_list):
    ids=[]
    for instance in instance_list:
        ids.append(utils.get_instance_id(instance))
    print(ids)
    return ids

def main():
    # get full list of instances to modify
    instances = get_instance_list(args.envs, INSTANCES)
    
    # SHUTDOWN ACTIONS
    if args.action == "shutdown":

        # Start by disabling alerts.
        for env in args.envs:
            env_alert_list = utils.get_alarms(env.upper())
            utils.modify_alerts(env_alert_list,'disable') 

        instance_ids=get_instance_id_list(instances)

        for instance in instances:
            for env in args.envs:
                for app in APPLICATIONS[env]:
                    utils.remove_instance_from_lb(app['lb_name'],instance)
                    print("Removing instance {} from load balancer: {}".format(instance,app['lb_name']))
        
        # Check all instances are running before proceeding 

        print("Stopping instances")
        utils.ec2client.stop_instances(
                DryRun=False,
                InstanceIds=get_instance_id_list(instances),
                Force=True
                )

    elif args.action == "poweron":
        instance_ids=get_instance_id_list(instances)
        # Start up hosts
        print("Starting hosts")
        utils.ec2client.start_instances(
                DryRun=False,
                InstanceIds=instance_ids
                )

        # Check all instances are running before proceeding 
        for id in instance_ids:
            instance = utils.ec2resource.Instance(id)
            print("Waiting for instance with id: '{}' to start".format(id))
            instance.wait_until_running()
            print("Instance started")

        for instance in instances:
            for env in args.envs:
                for app in APPLICATIONS[env]:
                    print("Adding instance {} to load balancer: {}".format(instance,app['lb_name']))
                    utils.add_instance_to_lb(app['lb_name'],instance)

        print("Waiting 5 minutes for alarms to return to okay state...")
        time.sleep(300)

        # Reenable the appropriate alarms. 
        for env in args.envs:
            env_alert_list = utils.get_alarms(env.upper())
            utils.modify_alerts(env_alert_list,'enable') 
        

if __name__=="__main__":
    args = parse_args()
    main()
        
