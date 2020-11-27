import aws_utils
import yaml_utils
import jenkins_utils
import log_operation
import gl


def scale_out():
    instance_id = aws_utils.create_ec2()
    log_operation.operation_history("instance_id :" + str(instance_id))
    public_ip = aws_utils.get_public_ip_by_instance_id(instance_id).strip()
    log_operation.operation_history("public_ip :" + str(public_ip))
    launch_time = aws_utils.get_launch_time_by_instance_id(instance_id).strip()
    log_operation.operation_history("launch_time :" + str(launch_time))
    yaml_utils.add_new_ec2_instance_log(str(instance_id), str(public_ip), str(launch_time))
    yaml_utils.add_docker_cloud_in_jenkins(str(public_ip))
    jenkins_utils.trigger_configuration_reload(gl.server_domain)


