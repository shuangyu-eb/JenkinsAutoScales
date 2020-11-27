from xml.etree.ElementTree import ElementTree
import re


def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree


# get busy docker cloud ips in jenkins master computer xml
def get_busy_docker_cloud_ips():
    root = read_xml('computer.xml').getroot()
    res = []
    for offspring in root.findall("computer"):
        format_des = re.findall(r"tcp://(.+?):4243", offspring.find("description").text)
        if format_des:
            res.append(format_des[0])
    return res