from datetime import datetime

def cronjob():
    """
    Main cron job.
    The main cronjob to be run continuously.
    """
    print("Cron job is running")
    print("Tick! The time is: %s" % datetime.now())

def cronjob2():
    """
    Main cron job.
    The main cronjob to be run continuously.
    """
    print("Cron job2 is running")
    print("Tick! The time is: %s" % datetime.now())