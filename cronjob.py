# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cronjob

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(cronjob, "interval", seconds=3600*4)
#scheduler.add_job(cronjob2, "interval", seconds=50)
scheduler.start()