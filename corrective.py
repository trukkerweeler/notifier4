import utils, os, sys
from datetime import datetime, timedelta

emails = {"TKENT": "tim.kent@ci-aviation.com","CHARRISON": "tim.kent@ci-aviation.com","CLEFTWICH": "tim.kent@ci-aviation.com"}
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
            email = emails[assignee.upper()]
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
                utils.sendMail(to_email=[email], subject="Overdue Correctives", message=str(odcas))
        utils.setLastSentFile('corrective')
    else:
        print("Not sending overdue CA's, too soon or off-hours. Last sent +10: " + str(utils.getLastSentFile('corrective')) + " Current: " + str(datetime.today()))


def closeout():
    """Identify closed correctives and send email to appropriate people."""
    sql4 = "select c.CORRECTIVE_ID from CORRECTIVE c left join CORRECTIVE_NOTIFY cn on c.CORRECTIVE_ID = cn.CORRECTIVE_ID where cn.NOTIFY_DATE is null and DATE(c.CLOSED_DATE) > '2023-08-14';"
    # sql4 = "select c.CORRECTIVE_ID from CORRECTIVE c left join CORRECTIVE_NOTIFY cn on c.CORRECTIVE_ID = cn.CORRECTIVE_ID where cn.NOTIFY_DATE is null;"
    noNotifications = utils.getDatabaseData(sql4)
    noNotificationsDisplay = "CA notifications: \n" + str(noNotifications) + "\n"
    # print(noNotificationsDisplay)
    for corrid in noNotifications:
        notification = '''The following corrective action has been closed. Please review and take appropriate action(s). \nCorrective id: %s''' % (corrid)
        # print(f"--- {corrid[0]} ---")
        print(notification)
        utils.sendMail(to_email=["tim.kent@ci-aviation.com","craig@ci-aviation.com"], subject=f"Corrective Action Closeout: {corrid[0]}", message=notification)
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
        notification = '''The following corrective action has been issued. Please review and comment as needed. \nCorrective id: %s \n\nDescription: %s''' % (corrid, trend)
        # print(f"--- {corrid} ---")
        # print(notification)
        asstoemail = utils.emailAddress(assto.upper())
        # asstoemail = emails[assto.upper()]
        # print(f'Assigned to: {asstoemail}')
        if assto != "TKENT":
            utils.sendMail(to_email=[asstoemail], subject=f"Corrective Action Issued: {corrid}", message=notification, cc_email=["tim.kent@ci-aviation.com"])
        else:
            utils.sendMail(to_email=[asstoemail], subject=f"Corrective Action Issued: {corrid}", message=notification)
        insertSql = f"insert into CORRECTIVE_NOTIFY (CORRECTIVE_ID, STAGE, NOTIFY_DATE) values ('{corrid}', 'I', NOW());"
        utils.updateDatabaseData(insertSql)


def main():
    issuedNotification()
    print("==========================================")
    overdues()
    print("==========================================")
    closeout()

    

if __name__ == '__main__':
    main()
    print("done")