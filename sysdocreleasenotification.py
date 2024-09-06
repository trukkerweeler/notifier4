import os, utils
from datetime import datetime, timedelta
from icecream import ic


def releaseNotifications():
    """Identify documents that have been released or obsoleted and send email to appropriate people. Designed to run automatically from chron/task."""

    print("Running releaseNotifications")
    sql3 = "select d.DOCUMENT_ID, d.REVISION_LEVEL, d.NAME, d.STATUS from DOCUMENTS d left join DOCUMENTS_NOTIFY dn on d.DOCUMENT_ID = dn.DOCUMENT_ID and d.REVISION_LEVEL = dn.REVISION_LEVEL where dn.NOTIFIED_DATE is null;"
    noNotifications = utils.getDatabaseData(sql3)
    noNotificationsDisplay = "Document notifications: \n" + str(noNotifications) + "\n"
    # print(noNotificationsDisplay)
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
        noNotifications = None


def main():
    releaseNotifications()

if __name__ == "__main__":
    main()