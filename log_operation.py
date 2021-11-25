# from datetime import datetime
# import os
# import logging
#
# # logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO, filename="test.log")
#
# def operation_history(operation):
#     ec2_operation_history = os.path.join(os.getcwd(), 'operation_history.txt')
#     file_handle = open(ec2_operation_history, mode='a+')
#     file_handle.write('Execute python script to ' + operation + " at time:" + str(datetime.now()) + '\n')

# logging.warning('And this, too')
# logging.info('scale_out')