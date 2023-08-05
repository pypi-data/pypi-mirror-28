import utils
import argparse

def parse_args():
  parser = argparse.ArgumentParser(description='Deploy a load balancer') 
  parser.add_argument('-n','--lb-name',required=True,help='The name of the load balancer to modify')
  parser.add_argument('-a','--action',required=True,choices=['add','remove'],help='The action to perform, add or remove instance')
  parser.add_argument('-i','--instances',nargs='+',required=True,help='A list of instances to add to the load balancer')
  return parser.parse_args()


def main():
    if args.action == "add":
        for instance in args.instances:
            utils.add_instance_to_lb(args.lb_name,instance)
    elif args.action == "remove":
        for instance in args.instances:
            utils.remove_instance_from_lb(args.lb_name,instance)

if __name__=="__main__":
    args = parse_args()
    main()
        
