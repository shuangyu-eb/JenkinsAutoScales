import os


ec2_operation_history = os.path.join(os.getcwd(), 'operation_history.txt')


def file_check_and_create(file_path):
    if not os.path.isfile(file_path):
        os.system(r"touch {}".format(file_path))
    else:
        print("file exists")


file_check_and_create(ec2_operation_history)
