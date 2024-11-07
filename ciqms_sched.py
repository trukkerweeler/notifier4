import sched
import time
import sysdoc
import input
import datetime
import preventivemx
import ncm

def mailer():
    # if its a weekday
    if datetime.datetime.today().weekday() < 5:
        print("Sysdoc release notification: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sysdoc.releaseNotifications()
        print("New action issued notification: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        input.Issue()
        print("PM scanning started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        preventivemx.main()
        print("NCM issue notification started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ncm.ncmIssueNotification()

def run_scheduler():
    scheduler = sched.scheduler(time.time, time.sleep)
    interval = 1200  # seconds
    # interval = 30  # seconds

    while True:
        scheduler.enter(interval, 1, mailer, ())
        scheduler.run()

run_scheduler()