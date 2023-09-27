import os, utils
from datetime import datetime, timedelta


def releaseNotifications():
    """Identify documents that have been released or obsoleted and send email to appropriate people."""
    sql3 = "select d.DOCUMENT_ID, d.REVISION_LEVEL, d.NAME, d.STATUS from DOCUMENTS d left join DOCUMENTS_NOTIFY dn on d.DOCUMENT_ID = dn.DOCUMENT_ID and d.REVISION_LEVEL = dn.REVISION_LEVEL where dn.NOTIFIED_DATE is null;"
    noNotifications = utils.getDatabaseData(sql3)
    noNotificationsDisplay = "Document notifications: \n" + str(noNotifications) + "\n"
    print(noNotificationsDisplay)
    for docid, revlvl, name, status in noNotifications:
        match status:
            case "C":
                notification = '''The following document has been issued/revised. Please review and take appropriate action. \nDocument id: %s, revision: %s''' % (docid, revlvl)
                utils.sendMail(to_email=["tim.kent@ci-aviation.com","craig@ci-aviation.com"], subject=f"Document Release Notification: {docid} - {name}", message=notification)

            case "O":
                notification = '''The following document is obsolete. Please review and take appropriate action. \nDocument id: %s, revision: %s''' % (docid, revlvl)
                utils.sendMail(to_email=["tim.kent@ci-aviation.com","craig@ci-aviation.com"], subject=f"Document Obsolescense Notification: {docid} - {name}", message=notification)

        print(notification)
        insertSql = f"insert into DOCUMENTS_NOTIFY (DOCUMENT_ID, REVISION_LEVEL, ACTION, NOTIFIED_DATE) values ('{docid}','{revlvl}','{status}',NOW());"
        utils.updateDatabaseData(insertSql)


def checkDocs():
    """Goes through docs_avail table and checks that each file exists for both the control and distribution locations. 
    Sends email for missing docs. Only runs once per day."""
  
    audit = []
    sql = "SELECT * FROM DOCS_AVAIL join DOCUMENTS on DOCS_AVAIL.DOCUMENT_ID = DOCUMENTS.DOCUMENT_ID where DOCUMENTS.STATUS = 'C';"
    records = utils.getDatabaseData(sql)
    for row in records:
        # check control location
        if row[1] is None:
            # print("Control location missing: " + row[0])
            audit.append(row[0] + " (ctrl/missing db entry)")
        else:
            if not os.path.exists(row[1]):
                # print(f"Control location moved?: {row[0]} - {row[1]}")
                audit.append(row[0] + " (ctrl/moved?)")
        
        # check distribution location
        if row[2] is None:
            # print(f"Distribution location missing:  {row[0]}")
            audit.append(row[0] + " (dist/missing db entry)")
        else:
            if not os.path.exists(row[2]):
                # print(f"Distribution location moved?: {row[0]} - {row[2]}")
                audit.append(row[0] + " (dist/moved?)")
    utils.sendMail("tim.kent@ci-aviation.com", f"Missing Documents - {datetime.now()}", f"Missing Documents: {len(audit)}\n\n{audit}")


def main():
    if utils.ranToday("sysdoc") == True:
        print("Already ran today - sysdoc.py")
    else:  
        releaseNotifications()
        checkDocs()


if __name__ == '__main__':
    main()
    print("done")