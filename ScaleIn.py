import os
import xmlUtils
import yamlUtils
import awsUtils

f = os.popen('date')
now = f.read()
print("Today is ", now)

busy_ips = xmlUtils.get_busy_docker_cloud_ips()
docker_cloud_ips = yamlUtils.collect_docker_cloud_ips('jenkins.yaml')
print("busy", busy_ips)
print("all ips", docker_cloud_ips)
deletable_ips = [x for x in docker_cloud_ips if x not in busy_ips]
print("deletable ips", deletable_ips)


yamlUtils.delete_docker_cloud_in_jenkins(deletable_ips[0])