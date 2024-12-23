import sched
import time
import sysdoc
import input
import datetime
import pmScanning
import ncm
import correctiveHelper
import autofilercal
import ncmHelper
import ncmScanning

def mailer():
    # if its a weekday
    if datetime.datetime.today().weekday() < 5:
        print("Corrective helper started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        correctiveHelper.main()
        print("Sysdoc release notification: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sysdoc.releaseNotifications()
        print("New action issued notification: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        input.Issue()
        print("PM scanning started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        pmScanning.main()
        print("NCM issue notification started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ncm.ncmIssueNotification()
        print("Autofiler CAL started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        autofilercal.main()
        print("NCM helper started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ncmHelper.makeNcmFolders()
        print("NCM scanning started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ncmScanning.main()
        

def run_scheduler():
    scheduler = sched.scheduler(time.time, time.sleep)
    interval = 1500  # seconds
    # interval = 40  # seconds

    while True:
        scheduler.enter(interval, 1, mailer, ())
        scheduler.run()

run_scheduler()