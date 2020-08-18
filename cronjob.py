import multiprocessing
import json
import requests
# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cronjob

base = "https://api.telegram.org/bot1228033872:AAHsI3oFOQLKVC7mmnVH0bNyQuPGitiBEXQ/"
def get_updates(offset=None):
        url = base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        try:
            r = requests.get(url)
            return json.loads(r.content)
        except:
            return None
def send_message(msg, chat_id):
        url = base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            try:
                requests.get(url)
            except:
                pass
def scheduling():
    # Create an instance of scheduler and add function.
    scheduler = BlockingScheduler()

    #scheduler.add_job(cronjob, 'cron', hour='7', minute='45')
    scheduler.add_job(cronjob, 'cron', hour='11', minute='0')
    scheduler.add_job(cronjob, 'cron', hour='15', minute='30')
    #scheduler.add_job(cronjob, "interval", seconds=3600*4)
    #scheduler.add_job(cronjob2, "interval", seconds=50)
    scheduler.start()

def triggering():
    send_message('Started','582942300')
    update_id = None
    while True:
        try:
            updates = get_updates(offset=update_id)   
            updates = updates["result"]
        except:
            updates=None

        if updates:
            for item in updates:
                update_id = item["update_id"]
                from_ = item["message"]["from"]["id"]
                try:
                    data = str(item["message"]["text"])
                except:
                    data = None
                if data == 'calendar':
                    try:
                        send_message('Executing','582942300')
                        cronjob()
                    except:
                        print("exception occured in cd ")

p1 = multiprocessing.Process(target = scheduling)
p2 = multiprocessing.Process(target = triggering)

p1.start()
p2.start()

p1.join()
p2.join()