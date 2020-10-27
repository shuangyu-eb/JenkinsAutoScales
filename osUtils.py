import os

# import sys
# print(os.path.abspath('main.py'))
# print(os.getcwd())

ec2_create_history_path = os.path.join(os.getcwd(), 'ec2_creation_history.yaml')


def file_check_and_create(file_path):
    print("file_check_and_create" + file_path)
    if not os.path.isfile(ec2_create_history_path):
        os.system(r"touch {}".format(ec2_create_history_path))
    else:
        print("存在")


file_check_and_create(ec2_create_history_path)
