import time
from datetime import datetime
import os

ticks = time.time()


def operation_history(operation):
    ec2_operation_history = os.path.join(os.getcwd(), 'operation_history.txt')
    file_handle = open(ec2_operation_history, mode='a+')
    file_handle.write('Execute python script to ' + operation + " at time:" + str(datetime.now()) + '\n')

