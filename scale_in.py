import xml_utils
import yaml_utils
import jenkins_utils
import aws_utils
import global_constants


def scale_in():
    jenkins_utils.get_current_busy_computer_xml()
    busy_ips = xml_utils.get_busy_docker_cloud_ips()
    docker_cloud_ips = yaml_utils.collect_docker_cloud_ips('jenkins.yaml')
    deletable_ips = [x for x in docker_cloud_ips if
                     x not in busy_ips and yaml_utils.check_ec2_launch_time_over_2_hours(x) is True]
    if len(deletable_ips) > 0:
        yaml_utils.delete_docker_cloud_in_jenkins(deletable_ips[0])
        deleted_instance_id= yaml_utils.get_instance_id_by_public_ip_from_ec2_creation_yaml(deletable_ips[0])
        yaml_utils.delete_ec2_instance_log_by_id(deleted_instance_id)
        aws_utils.terminate_ec2(deleted_instance_id)
        jenkins_utils.trigger_configuration_reload(global_constants.server_domain)
