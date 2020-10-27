import yaml
import os
import re
import bios


## 读取yaml文件
def read_yaml(file):
    if os.path.isfile(file):
        print("read", file)
        fr = open(file, 'r')
        yaml_info = yaml.load(fr)
        fr.close()
        return yaml_info
    return None


# def get_docker_clouds(docker_clouds):


# jenkinsconfiguration_path = os.path.join(os.getcwd(), 'jenkins.yaml')
# os.path.isfile(jenkinsconfiguration_path)
# yaml_infos = read_yaml(jenkinsconfiguration_path)


# print(yaml_infos['jenkins']['clouds'])
# print(type(yaml_infos['jenkins']['clouds']))
# print(len(yaml_infos['jenkins']['clouds']))

# docker_cloud_ips = []
# for i in range(len(yaml_infos['jenkins']['clouds'])):
#     str = "tcp://54.199.31.91:4243"
#     print(re.findall(r"tcp://(.+?):4243", str))
#     print(yaml_infos['jenkins']['clouds'][i]['docker']['dockerApi']['dockerHost']['uri'])
#     docker_cloud_ips.append(re.findall(r"tcp://(.+?):4243",
#                                        yaml_infos['jenkins']['clouds'][i]['docker']['dockerApi']['dockerHost']['uri'])[
#                                 0])
#
# print(docker_cloud_ips)

# get all the docker cloud ips form file f
def collect_docker_cloud_ips(file_name):
    jenkins_configuration_path = os.path.join(os.getcwd(), file_name)
    os.path.isfile(jenkins_configuration_path)
    yaml_infos = read_yaml(jenkins_configuration_path)
    docker_cloud_ips = []
    for i in range(len(yaml_infos['jenkins']['clouds'])):
        # str = "tcp://54.199.31.91:4243"
        # print(re.findall(r"tcp://(.+?):4243", str))
        # print(yaml_infos['jenkins']['clouds'][i]['docker']['dockerApi']['dockerHost']['uri'])
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
    f = open("ec2_creation_history.yaml", "w")
    yaml.dump(temp_dict, f)
    f.close()


#
# dict = {}
# instance_id = "i-0466c22ad696bcd0d"
# instance_id2 = "i-0bd8a6f2a3762a500"
# public_ip = "35.72.32.117"
# public_ip2 = "18.180.156.169"
# dict[instance_id] = {
#     "public_ip": public_ip,
#     "creation_time": "2020-10-20T03:22:53.000Z"
# }
# dict[instance_id2] = {
#     "public_ip": public_ip2,
#     "creation_time": "2020-10-20T03:22:53.000Z"
# }
# #
# f = open("ec2_creation_history.yaml", "w")
# yaml.dump(dict, f)
# f.close()
# 修改yaml配置

# delete ec2 instance history in ec2_creation_history.yaml by instance id
def delete_ec2_instance_log_by_id(instance_id):
    with open("ec2_creation_history.yaml", "r") as f:
        # print(f.read())
        result = f.read()
        x = yaml.load(result)
        print(type(x))
        print(x)
        if not x:
            x.pop(instance_id)
        print(x)
        with open("ec2_creation_history.yaml", 'w') as w_f:
            yaml.dump(x, w_f)


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
