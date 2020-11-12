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
    # JenkinsUtils.upload_jenkins_yaml()
    JenkinsUtils.trigger_configuration_reload("newjenkins.tardisoneci.com")


# yamlUtils.add_new_ec2_instance_log(str("i-02e62db6e0e320d18"), str("18.181.46.37"), str("2020-11-12T07:32:51.000Z"))

yamlUtils.add_docker_cloud_in_jenkins("18.181.46.37")
