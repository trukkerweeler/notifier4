import utils
from datetime import datetime, timedelta
from icecream import ic
import datetime

def ncmIssueNotification():
    """sends notifications for open NCMs that have not been notified"""
    sql = """select n.NCM_ID, NCM_DATE, PRODUCT_ID, DESCRIPTION, CLOSED, CLOSED_DATE, n.ASSIGNED_TO 
    from NONCONFORMANCE n
    left join NCM_DESCRIPTION d on n.NCM_ID = d.NCM_ID
    left join NCM_NOTIFY s on n.NCM_ID = s.NCM_ID 
    where s.ACTION is null or 
    n.ASSIGNED_TO != (select ASSIGNED_TO from NONCONFORMANCE where NCM_ID = n.NCM_ID);"""

    noNotifications = utils.getDatabaseData(sql)
    for ncmid, ncmdate, productid, description, closed, closeddate, assto in noNotifications:
        # print(ncmid, ncmdate, description, closed, closeddate, assto)
        # if closed == 'Y':
        #     status = 'C'
        # else:
        status = 'I'
        asstoemail = utils.emailAddress(assto)
        notification = f'''New NCM issued. Please review and take appropriate and timely action. \nNCM id: {ncmid} \nDate: {ncmdate} \nProduct Id: {productid} \nDescription: {description} \n\nAssociated files can be found at \\\\fs1\\Quality - Records\\8700 - Nonconformance\\YYYY\\NCMID. \n\nIf you have any questions please contact the quality manager.'''
        # if "tim" in asstoemail:
        utils.sendMail(to_email=[asstoemail], cc_email="tim.kent@ci-aviation.com", subject=f"NCM Notification: {ncmid} - {description}", message=notification, from_email="tim")

        insertSql = f"insert into NCM_NOTIFY (NCM_ID, ACTION, NOTIFIED_DATE, ASSIGNED_TO) values ('{ncmid}','{status}',LOCALTIME(), '{assto}');"
        utils.updateDatabaseData(insertSql)

if __name__ == '__main__':
    ncmIssueNotification()