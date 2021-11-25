import json
import jenkins
import command_execute_utils
import global_constants

server = jenkins.Jenkins("https://" + global_constants.jenkins_server_domain, username=global_constants.jenkins_user,
                         password=global_constants.jenkins_password)


def generate_jenkins_crumb():
    return command_execute_utils.runcmd(
        [
            f"curl https://{global_constants.jenkins_server_domain}/crumbIssuer/api/xml?xpath=concat\(//crumbRequestField,%22:%22,//crumb\) -c "
            f"cookies.txt --user '{global_constants.jenkins_user}:{global_constants.jenkins_password}'"])


def generate_jenkins_api_token(jenkins_crumb):
    api_result_json = command_execute_utils.runcmd(
        [
            f"curl 'https://{global_constants.jenkins_server_domain}/user/tardisone/descriptorByName/jenkins.security.ApiTokenProperty"
            f"/generateNewToken' --data 'newTokenName=fresh-reload-token' --user "
            f"'{global_constants.jenkins_user}:{global_constants.jenkins_password}' -b cookies.txt  -H {jenkins_crumb} "])
    print(api_result_json)
    return json.loads(api_result_json)['data']['tokenValue']


def trigger_configuration_reload():
    crumb = generate_jenkins_crumb()
    api_token = generate_jenkins_api_token(crumb)
    return command_execute_utils.runcmd(
        [
            f"curl -X POST -u tardisone:{api_token} https://{global_constants.jenkins_server_domain}/configuration-as-code/reload "])


# get job number in build queue
def get_job_count_in_build_queue():
    queue_info = server.get_queue_info()
    return len(queue_info)


def get_jenkins_configuration_yaml():
    crumb = generate_jenkins_crumb()
    api_token = generate_jenkins_api_token(crumb)
    return command_execute_utils.runcmd(
        [
            f"curl -X POST https://tardisone:{api_token}@{global_constants.jenkins_server_domain}/configuration-as-code/export -H {crumb} > "
            f"jenkins.yaml"])


def get_current_busy_computer_xml():
    command_execute_utils.runcmd(
        [f"curl https://{global_constants.jenkins_server_domain}/computer/api/xml?depth=1"
         f" --user '{global_constants.jenkins_user}:{global_constants.jenkins_password}' > computer.xml"])