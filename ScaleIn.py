import os
import xmlUtils
import yamlUtils
import JenkinsUtils
import awsUtils

f = os.popen('date')
now = f.read()
print("Today is ", now)


def Scale_in():
    # JenkinsUtils.get_current_busy_computer_xml()
    busy_ips = xmlUtils.get_busy_docker_cloud_ips()
    print("busy_ips", busy_ips)
    docker_cloud_ips = yamlUtils.collect_docker_cloud_ips('jenkins.yaml')
    print("docker_cloud_ips", docker_cloud_ips)
    deletable_ips = [x for x in docker_cloud_ips if
                     x not in busy_ips and yamlUtils.check_ec2_launch_time_over_2_hours(x) is True]
    print("deletable ips", len(deletable_ips))
    if len(deletable_ips) > 0:
        print("deletable deletable_ips[0]", deletable_ips[0])
        yamlUtils.delete_docker_cloud_in_jenkins(deletable_ips[0])
        deleted_instance_id= yamlUtils.get_instance_id_by_public_ip_from_ec2_creation_yaml(deletable_ips[0])
        print('deleted instance id', deleted_instance_id)
        yamlUtils.delete_ec2_instance_log_by_id(deleted_instance_id)
        awsUtils.terminate_ec2(deleted_instance_id)
        JenkinsUtils.trigger_configuration_reload("newjenkins.tardisoneci.com")
