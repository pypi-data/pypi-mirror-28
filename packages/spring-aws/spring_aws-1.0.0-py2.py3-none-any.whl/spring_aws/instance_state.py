import utils
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Change the state of an instance(s)')
    parser.add_argument('-a', '--action', required=True, choices=['shutdown', 'poweron'],
                        help='The action to perform, start or stop an instance')
    parser.add_argument('-r', '--role', required=True, help='Instances with this role will be affected')
    return parser.parse_args()


def main():

    # Get list of instances that match tag
    tag_dict = {'instance_role': args.role }
    instances = utils.get_filtered_instances( tag_dict )
    instance_ids = utils.get_instance_id_from_manifest( instances )

    if args.action == "shutdown":
        print("Stopping instances")
        utils.ec2client.stop_instances(
            DryRun=False,
            InstanceIds=instance_ids,
            Force=True
        )
    elif args.action == "poweron":
        print("Starting hosts")
        utils.ec2client.start_instances(
            DryRun=False,
            InstanceIds=instance_ids
        )

if __name__ == "__main__":
    args = parse_args()
    main()