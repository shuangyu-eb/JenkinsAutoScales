import aws_utils
import yaml_utils
import jenkins_utils
import logging
import global_constants

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO, filename="slave_scale_log")


def scale_out():
    instance_id = aws_utils.create_ec2()
    public_ip = aws_utils.get_public_ip_by_instance_id(instance_id).strip()
    launch_time = aws_utils.get_launch_time_by_instance_id(instance_id).strip()
    logging.info(f"scale out one ec2 with {instance_id}")
    yaml_utils.add_new_ec2_instance_log(str(instance_id), str(public_ip), str(launch_time))
    yaml_utils.add_docker_cloud_in_jenkins(str(public_ip))
    jenkins_utils.trigger_configuration_reload(global_constants.server_domain)
