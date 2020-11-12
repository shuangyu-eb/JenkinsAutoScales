import os

ec2_create_history_path = os.path.join(os.getcwd(), 'ec2_creation_history.yaml')

ec2_operation_history = os.path.join(os.getcwd(), 'operation_history.txt')

print(ec2_create_history_path)

def file_check_and_create(file_path):
    print("file_check_and_create" + file_path)
    if not os.path.isfile(file_path):
        os.system(r"touch {}".format(file_path))
    else:
        print("存在")


file_check_and_create(ec2_operation_history)
