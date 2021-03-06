import command_execute_utils
import json


# Create aws ec2 and return instance id
def create_ec2():
    response = command_execute_utils.runcmd("aws ec2 run-instances \\\n"
                                           + "    --launch-template LaunchTemplateId=lt-01d8af9d139b59291,Version=2")
    return json.loads(response)["Instances"][0]["InstanceId"]


# get public ip of instance by id
def get_public_ip_by_instance_id(instance_id):
    return command_execute_utils.runcmd(f"aws ec2 describe-instances --instance-ids {instance_id} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text")


# get launch time of instance by id
def get_launch_time_by_instance_id(instance_id):
    return command_execute_utils.runcmd(f"aws ec2 describe-instances --instance-ids {instance_id} --query 'Reservations[*].Instances[*].LaunchTime' --output text")


def terminate_ec2(instance_id):
    return command_execute_utils.runcmd([f"aws ec2 terminate-instances --instance-ids {instance_id}"])
