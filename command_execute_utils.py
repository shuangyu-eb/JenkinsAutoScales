import subprocess
import log_operation


def runcmd(command):
    print(command)
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if ret.returncode == 0:
        return ret.stdout
    else:
        log_operation.operation_history(ret)



