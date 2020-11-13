import JenkinsUtils
import yamlUtils
import log_operation
import ScaleOn
import ScaleIn

JenkinsUtils.get_jenkins_configuration_yaml("newjenkins.tardisoneci.com")
if JenkinsUtils.get_job_count_in_build_queue() > 1 and len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")) < 3:
    log_operation.operation_history("scale on")
    ScaleOn.scale_on()
elif len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")) > 2 and JenkinsUtils.get_job_count_in_build_queue() == 0:
    log_operation.operation_history("scale in")
    ScaleIn.scale_in()
