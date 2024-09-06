import sched
import time
import sysdoc
import input

def mailer():
    print("Sysdoc release notification")
    sysdoc.releaseNotifications()
    print("New action issued notification")
    input.Issue()

def run_scheduler():
    scheduler = sched.scheduler(time.time, time.sleep)
    interval = 1800  # seconds

    while True:
        scheduler.enter(interval, 1, mailer, ())
        scheduler.run()

run_scheduler()