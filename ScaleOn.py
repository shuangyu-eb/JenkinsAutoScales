import awsUtils
import yamlUtils
import JenkinsUtils
import log_operation


def scale_on():
    instance_id = awsUtils.create_ec2()
    log_operation.operation_history("instance_id :" + str(instance_id))
    public_ip = awsUtils.get_public_ip_by_instance_id(instance_id).strip()
    log_operation.operation_history("public_ip :" + str(public_ip))
    launch_time = awsUtils.get_launch_time_by_instance_id(instance_id).strip()
    log_operation.operation_history("launch_time :" + str(launch_time))
    yamlUtils.add_new_ec2_instance_log(str(instance_id), str(public_ip), str(launch_time))
    yamlUtils.add_docker_cloud_in_jenkins(str(public_ip))
    JenkinsUtils.trigger_configuration_reload("newjenkins.tardisoneci.com")