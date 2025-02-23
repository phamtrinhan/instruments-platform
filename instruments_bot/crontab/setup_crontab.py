import os
from crontab import CronTab

my_cron = CronTab(user=True)
for job in my_cron:
    # print(job)
    my_cron.remove(job)
job = my_cron.new(command=f'source /Users/binhot/code_env/grapechain/grapebot/crontab/venv/bin/activate && python3 {os.getcwd()}/cron.py >> {os.getcwd()}/log.txt 2>&1')
job.minute.every(1)

my_cron.write()