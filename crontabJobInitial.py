from crontab import CronTab

my_cron = CronTab(user='zsy')
job = my_cron.new(command='python /Users/zsy/Desktop/JenkinsAutoScale/log_operation.py')
job.minute.every(1)

my_cron.write()
