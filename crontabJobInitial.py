from crontab import CronTab

# 创建linux系统当前用户的crontab，当然也可以创建其他用户的，但得有足够权限,如:user='root'
my_cron = CronTab(user='zsy')
job = my_cron.new(command='python /Users/zsy/Desktop/JenkinsAutoScale/writeDate.py > testHello.txt')
job.minute.every(1)

my_cron.write()
