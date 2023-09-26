import utils
from datetime import datetime, timedelta

def Issue():
    """send email to person assigned action."""
    sql3 = "select pi.PROJECT_ID, p.NAME, pi.INPUT_ID, INPUT_DATE, PEOPLE_ID, INPUT_TYPE, SUBJECT, pi.ASSIGNED_TO, pi.DUE_DATE, pi.CLOSED, pi.CLOSED_DATE, pit.INPUT_TEXT, ni.NOTIFIED_DATE from PEOPLE_INPUT pi left join INPUTS_NOTIFY ni on pi.INPUT_ID = ni.INPUT_ID left join PPL_INPT_TEXT pit on pi.INPUT_ID = pit.INPUT_ID left join PROJECT p on pi.PROJECT_ID = p.PROJECT_ID where ni.NOTIFIED_DATE is null and pi.CLOSED = 'N'"
    noNotifications = utils.getDatabaseData(sql3)
    noNotificationsDisplay = "Action notifications: \n" + str(noNotifications) + "\n"
    # print(noNotificationsDisplay)

    # match 
    status = 'I' #Issued
    for projectid, projectname,inputid, inputdate, reqby, inptype, subject, assto, due, closed, closedate, reqtext, notifiedDate in noNotifications:
        if notifiedDate == None:
            inputdate = inputdate.strftime("%m/%d/%Y")
            if due != None:
                due = due.strftime("%m/%d/%Y")
            shortreq = reqtext.split('.')[0] + '...'
            asstoemail = utils.getDatabaseData(f"select WORK_EMAIL_ADDRESS from PEOPLE where PEOPLE_ID = '{assto}'")[0][0]
            # print(asstoemail)
            notification = '''The following action item has been assigned. Please review and take appropriate and timely action. \nAction id: %s \nRequest date: %s \nRequest: %s \nProject: %s - %s\n\nIf you have any questions please contact Tim Kent.''' % (inputid, inputdate, reqtext, projectid, projectname)
            # print(notification)
            utils.sendMail(to_email=[asstoemail], subject=f"Action Item Notification: {inputid} - {shortreq}", message=notification, from_email="tim", cc_email="tim.kent@ci-aviation.com")

            insertSql = f"insert into INPUTS_NOTIFY (INPUT_ID, ACTION, NOTIFIED_DATE, ASSIGNED_TO) values ('{inputid}','{status}',LOCALTIME(), '{assto}');"
            utils.updateDatabaseData(insertSql)


def Reminder():
    '''remind person assigned action.'''
    status = 'R' #Reminder  
    #  I dont know how to do this sql yet
    sql = "select pi.PROJECT_ID, p.NAME, pi.INPUT_ID, INPUT_DATE, PEOPLE_ID, INPUT_TYPE, SUBJECT, pi.ASSIGNED_TO, pi.DUE_DATE, pi.CLOSED, pi.CLOSED_DATE, pit.INPUT_TEXT, ni.NOTIFIED_DATE from PEOPLE_INPUT pi left join INPUTS_NOTIFY ni on pi.INPUT_ID = ni.INPUT_ID left join PPL_INPT_TEXT pit on pi.INPUT_ID = pit.INPUT_ID left join PROJECT p on pi.PROJECT_ID = p.PROJECT_ID where ni.NOTIFIED_DATE is not null and ni.ACTION in ('I','R') and pi.CLOSED != 'Y';"
    noNotifications = utils.getDatabaseData(sql)
    # print(noNotifications)
    for projectid, projectname, inputid, *others in noNotifications:
        sql2 = f'select * from INPUTS_NOTIFY where INPUT_ID = {inputid} order by NOTIFIED_DATE desc limit 1;'
        # send reminder
        lastNotifiedDate = utils.getDatabaseData(sql2)[0][2]
        sql3 = f'select INPUT_TEXT from PPL_INPT_TEXT where INPUT_ID = {inputid};'
        # reqtext = utils.getDatabaseData(sql3)[0][1]
        reqtext = utils.getDatabaseData(sql3)[0][0]
        # print("=====================================")
        # print(f'assto: {others[4]}')
        # print(f'Request text: {reqtext}')
        asstoEmail = utils.emailAddress(others[4])

        try:
            # reqtext = utils.getDatabaseData(sql3)[0][1]
            shortreq = reqtext.split('.')[0] + '...'
            # print(f'Short request text: {shortreq}')
        except:
            shortreq = "(No short request text)"
            reqtext = "No request text"
        # print(lastNotifiedDate)
        if datetime.now() > lastNotifiedDate + timedelta(days=7):
            # print("send reminder")
            notification = '''Action items reminder. Please review and take appropriate and timely action. \nAction id: %s \nRequest date: %s \nRequest: %s \nProject: %s - %s\n\nIf you have any questions please contact Tim Kent.''' % (inputid, others[0], others[8], projectid, projectname)
            # print(notification)
            # print(shortreq)
            utils.sendMail(to_email=[asstoEmail], cc_email="tim.kent@ci-aviation.com", subject=f"Action Item Reminder: {inputid} - {shortreq}", message=notification, from_email="tim")

            insertSql = f"insert into INPUTS_NOTIFY (INPUT_ID, ACTION, NOTIFIED_DATE, ASSIGNED_TO) values ('{inputid}','{status}',LOCALTIME(), '{others[4]}');"
            utils.updateDatabaseData(insertSql)
        else:
            print(f"{inputid}: dont send reminder: too soon {lastNotifiedDate + timedelta(days=7)}") 

        # print()  


def main():
    Issue()
    Reminder()


if __name__ == '__main__':
    main()
    print("done")