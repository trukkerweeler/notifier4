import utils, os, sys
from datetime import datetime, timedelta
from icecream import ic
live = True

# emails = {"TKENT": "tim.kent@ci-aviation.com","CHARRISON": "tim.kent@ci-aviation.com","CLEFTWICH": "tim.kent@ci-aviation.com"}
# emails = {"TKENT": "tim.kent@ci-aviation.com","CHARRISON": "craig@ci-aviation.com","CLEFTWICH": "tim.kent@ci-aviation.com"}



def getAssignees():
    """Get assignees for overdue correctives."""
    sql = "SELECT DISTINCT ASSIGNED_TO FROM CORRECTIVE WHERE CLOSED = 'N' AND (DUE_DATE < CURRENT_DATE() or DUE_DATE is null)"
    records = utils.getDatabaseData(sql)
    assignees = []
    for row in records:
        assignees.append(row[0])
    return assignees


def overdues():
    """Identify overdue correctives and send email to appropriate people."""
    dayofweek = datetime.today().weekday()
    # print(dayofweek)
    # print(utils.getLastSentFile('corrective'))
    if dayofweek in [0,1,2,3] and datetime.today() > utils.getLastSentFile("corrective") and datetime.today().hour in [8,9,10,11,12,13,14,15,16,17,18,19,20,21]:
        assignees = getAssignees()
        for assignee in assignees:
            email = utils.emailAddress(assignee)
            # print(email)
            # odcas = "Dear Quality Team,\n\n"
            odcas = "The corrective action meeting is soon. Please prepare to discuss appropriate actions. The following correctives are overdue:\n\n"
            sql = f"SELECT CORRECTIVE_ID, ASSIGNED_TO, CORRECTIVE_DATE, DUE_DATE, TITLE FROM CORRECTIVE WHERE CLOSED = 'N' AND ASSIGNED_TO = '{assignee}' and (DUE_DATE < CURRENT_DATE() or DUE_DATE is null)"
            records = utils.getDatabaseData(sql)
            for row in records:
                caid = row[0]
                assto = row[1]
                cadate = row[2]
                cadate = cadate.strftime("%m/%d/%Y")
                cadate = cadate[0:10]
                duedate = row[3]
                if duedate is not None:
                    duedate = duedate.strftime("%m/%d/%Y")
                title = row[4]
                odcas += f"{caid} - {row[1]} - {cadate} - {duedate} - {title}\n"
            if len(odcas) > 0:
                utils.sendMail(to_email=[email], subject="Overdue Correctives", message=str(odcas), cc_email="")
                # utils.sendMail("tim.kent@ci-aviation.com", subject="Overdue Correctives", message=str(odcas), cc_email="")
        utils.setLastSentFile('corrective')
    else:
        print("Not sending overdue CA's, too soon or off-hours. Last sent +10: " + str(utils.getLastSentFile('corrective')) + " Current: " + str(datetime.today()))


def closeout():
    """Identify closed correctives and send email to appropriate people."""
    # sql4 = "select c.CORRECTIVE_ID from CORRECTIVE c left join CORRECTIVE_NOTIFY cn on c.CORRECTIVE_ID = cn.CORRECTIVE_ID where cn.NOTIFY_DATE is null and DATE(c.CLOSED_DATE) > '2023-08-14';"
    # sql4 = "select c.CORRECTIVE_ID, c.CLOSED_DATE, cn.NOTIFY_DATE, cn.STAGE from CORRECTIVE c left join CORRECTIVE_NOTIFY cn on c.CORRECTIVE_ID = cn.CORRECTIVE_ID and cn.STAGE = 'C' where (cn.NOTIFY_DATE is null) and DATE(c.CLOSED_DATE) > '2023-08-14';"
    sql4 = "select c.CORRECTIVE_ID from CORRECTIVE c left join CORRECTIVE_NOTIFY cn on c.CORRECTIVE_ID = cn.CORRECTIVE_ID and cn.STAGE = 'C' where (cn.NOTIFY_DATE is null) and DATE(c.CLOSED_DATE) > '2023-08-14';"
    noNotifications = utils.getDatabaseData(sql4)
    noNotificationsDisplay = "CA notifications: \n" + str(noNotifications) + "\n"
    # print(noNotificationsDisplay)
    for corrid in noNotifications:
        attachmentPath = utils.getAttachmentPath(corrid[0], "corrective")
        if attachmentPath is not None:
            attachment = attachmentPath
        else:
            attachment = "K:\\Quality - Records\\10200C - Corrective Actions"
        notification = '''<p>The following corrective action has been closed. Please review and take appropriate final action(s). </p><br> <p>%s</p> <p>Corrective id: %s</p>''' % (attachment, corrid[0])
        # print(f"--- {corrid[0]} ---")
        # print(notification)
        utils.sendHtmlMail(to_email=["tim.kent@ci-aviation.com","craig@ci-aviation.com"], subject=f"Corrective Action Closeout: {corrid[0]}", message=notification)

        # # print(f"attachment: {attachment}")
        # if (attachment is None):
        #     # utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject=f"Corrective Action Closeout: {corrid[0]}", message=notification)
        #     utils.sendMail(to_email=["tim.kent@ci-aviation.com","craig@ci-aviation.com"], subject=f"Corrective Action Closeout: {corrid[0]}", message=notification)
        # else:
        #     # utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject=f"Corrective Action Closeout: {corrid[0]}", message=notification, add_attachment={attachment})
        #     utils.sendMail(to_email=["tim.kent@ci-aviation.com","craig@ci-aviation.com"], subject=f"Corrective Action Closeout: {corrid[0]}", message=notification, attachment=attachment)

        insertSql = f"insert into CORRECTIVE_NOTIFY (CORRECTIVE_ID, STAGE, NOTIFY_DATE) values ('{corrid[0]}', 'C', NOW());"
        utils.updateDatabaseData(insertSql)


def issuedNotification():
    """Identify issued correctives and send email to appropriate people."""
    sql3 = f"select c.CORRECTIVE_ID, c.ASSIGNED_TO, ct.NC_TREND from CORRECTIVE c " \
    f"left join CORRECTIVE_NOTIFY cn on c.CORRECTIVE_ID = cn.CORRECTIVE_ID " \
    f"left join CORRECTIVE_TREND ct on c.CORRECTIVE_ID = ct.CORRECTIVE_ID " \
    f"where cn.NOTIFY_DATE is null and c.CLOSED = 'N' and c.CORRECTIVE_ID > '0001210';"

    issued = utils.getDatabaseData(sql3)    
    for corrid, assto, trend in issued:
        # print(corrid)
        notification = '''<p>The following corrective action has been issued. Please review and take action as needed. \nCorrective id: %s \n\nDescription: %s''' % (corrid, trend)
        notification += "<br><br>Corrective Action files are found at:</p> <a href='K:\\\\Quality - Records\\\\10200C - Corrective Actions'>K:/Quality - Records/10200C - Corrective Actions</a>"
        # print(f"--- {corrid} ---")
        # print(notification)
        asstoemail = utils.emailAddress(assto.upper())
        # asstoemail = emails[assto.upper()]
        # print(f'Assigned to: {asstoemail}')
        if assto != "TKENT":
            utils.sendHtmlMail(to_email=[asstoemail], subject=f"Corrective Action Issued: {corrid}", message=notification, cc_email=["tim.kent@ci-aviation.com"])
        else:
            utils.sendHtmlMail(to_email=[asstoemail], subject=f"Corrective Action Issued: {corrid}", message=notification)
        if live:
            insertSql = f"insert into CORRECTIVE_NOTIFY (CORRECTIVE_ID, STAGE, NOTIFY_DATE) values ('{corrid}', 'I', NOW());"
            utils.updateDatabaseData(insertSql)

def rootcse():
    """Identify CA project that do not have a root cause, send email to those people."""
    sql = "select pi.PROJECT_ID, pi.ASSIGNED_TO, p.NAME from PEOPLE_INPUT pi " \
    "left join PROJECT p on pi.PROJECT_ID = p.PROJECT_ID " \
    "where pi.SUBJECT = 'RCA' and pi.CLOSED = 'N' "
    records = utils.getDatabaseData(sql)
    for row in records:
        prjcaid = row[0]
        if prjcaid[0:3] == "CAR":
            caid = prjcaid[3:]
        else:
            caid = prjcaid
        assto = row[1]
        projectname = row[2]
        pcount = utils.getRcaRequestCount(caid, "R")
        # ic(pcount)
        notification = f'''<p>A root cause determination is needed. Please reply with root cause statement. The root cause statement cannot be a restatement of the finding. 
If you have any questions please contact the quality manager.</p> <p>Corrective id: {caid} </p><p>Description: {projectname} </p><a href='\\\\fs1\\Common\\Quality - Records\\10200C - Corrective Actions'>\\\\fs1\\Common\\Quality - Records\\10200C - Corrective Actions</a><br><p>(Count of previous requests: {pcount})</p>'''
        asstoemail = utils.emailAddress(assto.upper())
        # asstoemail = emails[assto.upper()]
        # print(f'Assigned to: {asstoemail}')
        if live == True:
            utils.sendHtmlMail(to_email=[asstoemail], subject=f"Corrective Action Root Cause: {caid}", message=notification)
            # remove CAR prefix from caid
            caid = caid[3:]
            utils.notifyCorrective(caid, "R")
        else:
            # notification = "<p>This is a paragraph!</p><br><a href='K:\\\\Quality - Records\\\\10200C - Corrective Actions'>K:/Quality/10200C - Corrective Actions</a>"
            notification = f'''<p>A root cause determination is needed. Please reply with root cause statement. The root cause statement cannot be a restatement of the finding. Helpful information on making good root cause analysis are attached. 
If you have any questions please contact the quality manager.</p> <p>Corrective id: {caid} </p><p>Description: {projectname} </p><a href='\\\\fs1\\Common\\Quality - Records\\10200C - Corrective Actions'>\\\\fs1\\Common\\Quality - Records\\10200C - Corrective Actions</a><br><p>(Count of previous requests: {pcount})</p>'''
        
            utils.sendHtmlMail(to_email=['tim.kent@ci-aviation.com'], subject=f"Corrective Action Root Cause: {caid}", message=notification)
            print(notification)
            print(asstoemail)                                                                                                                                           


def main():
    """Sends email to appropriate people for issue and closeout. Sends overdue email on weeks 2 and 4."""
    #Issued
    issuedNotification()

    #root cause
    if utils.week_of_month(datetime.today()) in [2, 4]:
        if utils.getLastSentFile0('corrective') < datetime.today() - timedelta(days=7):
            rootcse()
    
    #Closed
    closeout()

    # Overdues
    if utils.week_of_month(datetime.today()) in [2, 4]:
        if utils.getLastSentFile0('corrective') < datetime.today() - timedelta(days=7):
            overdues()
    
    #Update last sent
    utils.setLastSentFile('corrective')


def rootcseai():
    '''for each project that begins with CAR, if a rootcse ai does not exist, create RCA action item for the project.'''
    sql = "select * from PROJECT where PROJECT_ID like 'CAR%' and PROJECT_ID not in (select PROJECT_ID from PEOPLE_INPUT where SUBJECT = 'RCA')"
    records = utils.getDatabaseData(sql)
    # print(records)
    for row in records:
        prjcaid = row[0]
        projectname = row[1]
        assto = row[2]
        due_date  = utils.inthismanymysqldays(14)
        # get the next input id
        inputid = utils.getNextSysid("INPUT_ID")
        insertqsl = f"insert into PEOPLE_INPUT (INPUT_ID, PEOPLE_ID, PROJECT_ID, ASSIGNED_TO, INPUT_TYPE, SUBJECT, INPUT_DATE, DUE_DATE, CLOSED, CREATE_BY, CREATE_DATE) values ('{inputid}', 'TKENT', '{prjcaid}', '{assto}', 'STMT', 'RCA', NOW(), '{due_date}', 'N', 'CIQMS', NOW());"
        ic(insertqsl)
        utils.updateDatabaseData(insertqsl)
        # insert the ai text
        insertsql2 = f"insert into PPL_INPT_TEXT (INPUT_ID, INPUT_TEXT) values ('{inputid}', 'Root cause analysis for {projectname}');"
        ic(insertsql2)
        utils.updateDatabaseData(insertsql2)

                 


if __name__ == '__main__':
    main()
    rootcseai()
    # rootcse() #Seems redundant to the action item notification...
    closeout()
    print("done")