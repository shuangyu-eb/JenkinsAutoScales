import JenkinsUtils
import yamlUtils


print(len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")))
print(JenkinsUtils.get_job_count_in_build_queue())
# docker cloud number below Max 4 and the build job count > 1 means we need to scale on our docker clouds cluster
if JenkinsUtils.get_job_count_in_build_queue() > 1 and len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")) < 9:
    print("scale on")
# docker
elif len(yamlUtils.collect_docker_cloud_ips("jenkins.yaml")) > 2 and JenkinsUtils.get_job_count_in_build_queue() == 0:
    print("scale in")
