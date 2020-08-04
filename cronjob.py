# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.multi import OrTrigger

# Main cronjob function.
from main import cronjob
trigger = OrTrigger([CronTrigger(hour=1, minute=30), CronTrigger(hour=23, minute=10)]
# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(cronjob, trigger)

#scheduler.add_job(cronjob2, "interval", seconds=50)
scheduler.start()