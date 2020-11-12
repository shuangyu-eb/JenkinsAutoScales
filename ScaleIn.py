import os
import xmlUtils
import yamlUtils
import JenkinsUtils
import awsUtils

f = os.popen('date')
now = f.read()
print("Today is ", now)


def Scale_in():
    JenkinsUtils.get_current_busy_computer_xml()
    busy_ips = xmlUtils.get_busy_docker_cloud_ips()
    docker_cloud_ips = yamlUtils.collect_docker_cloud_ips('jenkins.yaml')
    print("busy", busy_ips)
    print("all ips", docker_cloud_ips)
    deletable_ips = [x for x in docker_cloud_ips if x not in busy_ips]
    print("deletable ips", deletable_ips)
    yamlUtils.delete_docker_cloud_in_jenkins(deletable_ips[0])
    awsUtils.terminate_ec2(deletable_ips[0])
    JenkinsUtils.trigger_configuration_reload("newjenkins.tardisoneci.com")
