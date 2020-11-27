import json
import jenkins
import command_execute_utils
import gl

server = jenkins.Jenkins("https://" + gl.server_domain, username='tardisone',
                         password='43f8d1c5d1864500b75db1f2c0f8177e')


def generate_jenkins_crumb(host_ip):
    return command_execute_utils.runcmd(
        ["curl https://" + host_ip + "/crumbIssuer/api/xml?xpath=concat\(//crumbRequestField,%22:%22,//crumb\) -c "
                                     "cookies.txt --user 'tardisone:43f8d1c5d1864500b75db1f2c0f8177e'"])


def generate_jenkins_api_token(jenkins_crumb, host_ip):
    api_result_json = command_execute_utils.runcmd(
        [
            "curl 'https://" + host_ip + "/user/tardisone/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken' "
                                         "--data 'newTokenName=fresh-reload-token'  "
                                         "--user 'tardisone:43f8d1c5d1864500b75db1f2c0f8177e' -b cookies.txt  -H "
            + jenkins_crumb])
    print(api_result_json)
    return json.loads(api_result_json)['data']['tokenValue']


def trigger_configuration_reload(host_ip):
    crumb = generate_jenkins_crumb(host_ip)
    api_token = generate_jenkins_api_token(crumb, host_ip)
    return command_execute_utils.runcmd(
        ["curl -X POST -u tardisone:" + api_token + " https://" + host_ip + "/configuration-as-code/reload "])


# get job number in build queue
def get_job_count_in_build_queue():
    queue_info = server.get_queue_info()
    return len(queue_info)


def get_jenkins_configuration_yaml(host_ip):
    crumb = generate_jenkins_crumb(host_ip)
    api_token = generate_jenkins_api_token(crumb, host_ip)
    return command_execute_utils.runcmd(
        ["curl -X POST https://tardisone:" + api_token + "@" +
         host_ip + "/configuration-as-code/export -H " + crumb + "> jenkins.yaml"])


def get_current_busy_computer_xml():
    command_execute_utils.runcmd(
        ["curl https://" + gl.server_domain + "/computer/api/xml?depth=1"
                                              " --user 'tardisone:43f8d1c5d1864500b75db1f2c0f8177e' > computer.xml"])
