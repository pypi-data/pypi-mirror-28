import boto3
import json
import argparse
import re
import utils

def main():

    for env in args.envs:
        env_alert_list = utils.get_alarms(env.upper())
        utils.modify_alerts(env_alert_list,args.action)

def parse_args():
  parser = argparse.ArgumentParser(description='Deploy a load balancer') 
  parser.add_argument('-a','--action',required=True,choices=['enable','disable'],help='Enable or disable environment alarm')
  parser.add_argument('-e','--envs',nargs='+',choices=['dev','stage	','prod'],required=True,help='A list of environments to affect')
  return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    main()