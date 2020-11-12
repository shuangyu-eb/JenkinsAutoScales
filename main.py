import JenkinsUtils
import yamlUtils
import log_operation
import ScaleOn
import ScaleIn

JenkinsUtils.get_jenkins_configuration_yaml("newjenkins.tardisoneci.com")
# print(len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")))
# print(JenkinsUtils.get_job_count_in_build_queue())
# docker cloud number below Max 4 and the build job count > 1 means we need to scale on our docker clouds cluster
print(">1",JenkinsUtils.get_job_count_in_build_queue())
print("cloud number",len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")))
if JenkinsUtils.get_job_count_in_build_queue() > 1 and len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")) < 3:
   log_operation.operation_history("scale on")
   # ScaleOn.scale_on()
# docker
elif len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")) > 2 and JenkinsUtils.get_job_count_in_build_queue() == 0:
    log_operation.operation_history("scale in")
    ScaleIn.Scale_in()