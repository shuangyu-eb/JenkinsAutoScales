import json
import jenkins
import commandExcuteUtils

server = jenkins.Jenkins('http://54.154.89.252:8080', username='admin', password='Zsy950108')


# def runcmd(command):
#     ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
#     if ret.returncode == 0:
#         return ret.stdout
#     else:
#         print("error:", ret)


def generate_jenkins_crumb(host_ip):
    return commandExcuteUtils.runcmd(
        ["curl " + host_ip + ":8080/crumbIssuer/api/xml?xpath=concat\(//crumbRequestField,%22:%22,//crumb\) -c "
                             "cookies.txt --user 'admin:Zsy950108'"])


def generate_jenkins_api_token(jenkins_crumb, host_ip):
    api_result_json = commandExcuteUtils.runcmd(
        ["curl '" + host_ip + ":8080/user/admin/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken'  "
                              "--data 'newTokenName=fresh-reload-token'  --user 'admin:Zsy950108' -b cookies.txt  -H "
         + jenkins_crumb])
    return json.loads(api_result_json)['data']['tokenValue']


def trigger_configuration_reload(host_ip):
    crumb = generate_jenkins_crumb(host_ip)
    api_token = generate_jenkins_api_token(crumb, host_ip)
    return commandExcuteUtils.runcmd(
        ["curl -X POST http://admin:" + api_token +
         "@" + host_ip + ":8080/configuration-as-code/reload -H " + crumb + ""])


# get job number in build queue
def get_job_count_in_build_queue():
    queue_info = server.get_queue_info()
    return len(queue_info)


def get_jenkins_configuration_yaml(host_ip):
    crumb = generate_jenkins_crumb(host_ip)
    api_token = generate_jenkins_api_token(crumb, host_ip)
    return commandExcuteUtils.runcmd(
        ["curl -X POST http://admin:" + api_token + "@" +
         host_ip + ":8080/configuration-as-code/export -H " + crumb + "> jenkins.yaml"])
