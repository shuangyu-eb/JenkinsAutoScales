import jenkins_utils
import yaml_utils
import log_operation
import scale_out
import scale_in

if __name__ == '__main__':
    jenkins_utils.get_jenkins_configuration_yaml()
    if jenkins_utils.get_job_count_in_build_queue() > 1 and len(
            yaml_utils.collect_docker_cloud_ips("jenkins.yaml")) < 3:
        log_operation.operation_history("scale out")
        scale_out.scale_out()
    elif len(yaml_utils.collect_docker_cloud_ips(
            "jenkins.yaml")) > 2 and jenkins_utils.get_job_count_in_build_queue() == 0:
        log_operation.operation_history("scale in")
        scale_in.scale_in()
