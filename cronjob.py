# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cronjob,cronjob2

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(cronjob, "interval", seconds=30)
scheduler.add_job(cronjob2, "interval", seconds=50)
scheduler.start()