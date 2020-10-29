import awsUtils
import yamlUtils
import JenkinsUtils


def scale_on():
    instance_id = awsUtils.create_ec2()
    public_ip = awsUtils.get_public_ip_by_instance_id(instance_id).strip()
    launch_time = awsUtils.get_launch_time_by_instance_id(instance_id).strip()
    yamlUtils.add_new_ec2_instance_log(instance_id, public_ip, launch_time)
    yamlUtils.add_docker_cloud_in_jenkins(public_ip)
    JenkinsUtils.upload_jenkins_yaml()
    JenkinsUtils.trigger_configuration_reload("54.154.89.252")