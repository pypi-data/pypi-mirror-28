import utils
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
    'dev': ['dev-2'],
    'stage': ['dev-2'],
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
        instance_ids=get_instance_id_list(instances)

        for instance in instances:
            for env in args.envs:
                for app in APPLICATIONS[env]:
                    utils.remove_instance_from_lb(app['lb_name'],instance)
                    print("Removing instance {} from load balancer: {}".format(instance,app['lb_name']))

    elif args.action == "poweron":
        instance_ids=get_instance_id_list(instances)
        # Check all instances are running before proceeding 

        for instance in instances:
            for env in args.envs:
                for app in APPLICATIONS[env]:
                    print("Adding instance {} to load balancer: {}".format(instance,app['lb_name']))
                    utils.add_instance_to_lb(app['lb_name'],instance)

if __name__=="__main__":
    args = parse_args()
    main()
        