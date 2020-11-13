import yaml
import os
import re
from datetime import date, datetime, time
from backports.datetime_fromisoformat import MonkeyPatch

MonkeyPatch.patch_fromisoformat()


## 读取yaml文件
def read_yaml(file):
    if os.path.isfile(file):
        print("read", file)
        fr = open(file, 'r')
        yaml_info = yaml.load(fr)
        fr.close()
        return yaml_info
    return None


# get all the docker cloud ips form file f
def collect_docker_cloud_ips(file_name):
    jenkins_configuration_path = os.path.join(os.getcwd(), file_name)
    os.path.isfile(jenkins_configuration_path)
    yaml_infos = read_yaml(jenkins_configuration_path)
    docker_cloud_ips = []
    for i in range(len(yaml_infos['jenkins']['clouds'])):
        print(re.findall(r"tcp://(.+?):4243",
                         yaml_infos['jenkins']['clouds'][i]['docker']['dockerApi']['dockerHost'][
                             'uri']))
        docker_cloud_ips.append(re.findall(r"tcp://(.+?):4243",
                                           yaml_infos['jenkins']['clouds'][i]['docker']['dockerApi']['dockerHost'][
                                               'uri'])[
                                    0])
    return docker_cloud_ips


# add instance log in ec2_creation_history.yaml
def add_new_ec2_instance_log(instance_id, public_ip, launch_time):
    temp_dict = {instance_id: {
        "public_ip": public_ip,
        "launch_time": launch_time
    }}
    f = open("ec2_creation_history.yaml", "a+")
    yaml.dump(temp_dict, f)
    f.close()


# delete ec2 instance history in ec2_creation_history.yaml by instance id
def delete_ec2_instance_log_by_id(instance_id):
    with open("ec2_creation_history.yaml", "r") as f:
        result = f.read()
        x = yaml.load(result)
        x.pop(instance_id)
        with open("ec2_creation_history.yaml", 'w') as w_f:
            yaml.dump(x, w_f)


def check_ec2_launch_time_over_2_hours(instance_ip):
    jenkins_ec2_creation_history_file_path = os.path.join(os.getcwd(), "ec2_creation_history.yaml")
    yaml_info = read_yaml(jenkins_ec2_creation_history_file_path)
    for instance_id in yaml_info:
        if yaml_info[instance_id]['public_ip'] == instance_ip:
            if (datetime.fromisoformat(yaml_info[instance_id]['launch_time'][:-1]) - datetime.now()).total_seconds() < -7200:
                return True
    return False


def get_instance_id_by_public_ip_from_ec2_creation_yaml(instance_ip):
    jenkins_ec2_creation_history_file_path = os.path.join(os.getcwd(), "ec2_creation_history.yaml")
    yaml_info = read_yaml(jenkins_ec2_creation_history_file_path)
    for instance_id in yaml_info:
        if yaml_info[instance_id]['public_ip'] == instance_ip:
            return instance_id


# add new docker cloud info in jenkins.yaml in jenkins master
def add_docker_cloud_in_jenkins(public_ip):
    jenkins_configuration_path = os.path.join(os.getcwd(), "jenkins.yaml")
    os.path.isfile(jenkins_configuration_path)
    yaml_infos = read_yaml(jenkins_configuration_path)
    clouds_info = yaml_infos['jenkins']['clouds']
    cloud_template_info = read_yaml(os.path.join(os.getcwd(), "docker_cloud.yaml"))
    cloud_template_info[0]["docker"]["dockerApi"]["dockerHost"]["uri"] = "tcp://" + public_ip + ":4243"
    clouds_info.append(cloud_template_info[0])
    with open('jenkins.yaml', 'w') as f:
        print(yaml_infos)
        print(clouds_info)
        yaml.dump(yaml_infos, f)


# delete new docker cloud info in jenkins.yaml in jenkins master
def delete_docker_cloud_in_jenkins(deleted_public_ip):
    jenkins_configuration_path = os.path.join(os.getcwd(), "jenkins.yaml")
    os.path.isfile(jenkins_configuration_path)
    yaml_infos = read_yaml(jenkins_configuration_path)
    clouds_info = yaml_infos['jenkins']['clouds']
    yaml_infos['jenkins']['clouds'] = list(filter(
        lambda node: (re.findall(r"tcp://(.+?):4243", node['docker']['dockerApi']['dockerHost']["uri"])[0] !=
                      deleted_public_ip), clouds_info))
    with open('jenkins.yaml', 'w') as f:
        print(yaml_infos)
        print(yaml_infos['jenkins']['clouds'])
        yaml.dump(yaml_infos, f)
