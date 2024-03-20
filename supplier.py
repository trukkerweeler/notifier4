import utils
from datetime import datetime, timedelta

def supplierExpirations():
    """Identify suppliers that have expired and send email to appropriate people."""
    # sql = '''SELECT s.SUPPLIER_ID, s.NAME, MAX(q.EXPIRY_DATE) FROM SUPPLIER s LEFT JOIN SUPPLIER_QMS q ON s.SUPPLIER_ID = q.SUPPLIER_ID WHERE (q.EXPIRY_DATE < NOW() or q.EXPIRY_DATE is null) and s.STATUS = 'A';'
    sql = '''with allsuppliers as (SELECT s.SUPPLIER_ID, s.NAME, s.STATUS as state, MAX(q.EXPIRY_DATE) as expiration FROM SUPPLIER s LEFT JOIN SUPPLIER_QMS q ON s.SUPPLIER_ID = q.SUPPLIER_ID group by s.SUPPLIER_ID) select * from allsuppliers where expiration < NOW() and state = 'A' '''

    
    expiredSuppliers = utils.getDatabaseData(sql)
    expiredSuppliersDisplay = "Expired suppliers: \n" + str(expiredSuppliers) + "\n"
    # print(expiredSuppliersDisplay)
    for supplierid, name, expdate in expiredSuppliers:
        notification = '''This supplier's qms expired on %s. Please review and take appropriate action. \nSupplier id: %s, name: %s''' % (expdate, supplierid, name)
        asstoemail = "tim.kent@ci-aviation.com"
        # utils.sendMail(to_email=[asstoemail], subject=f"Corrective Action Issued: {corrid}", message=notification, cc_email=["tim.kent@ci-aviation.com"])
        utils.sendMail(to_email=[asstoemail], subject=f"Supplier reapproval", message=notification)
        # print(notification)


def main():
    """Goes through tables and identifies overdue supplier reviews. Sends email to TKENT. In the 4th week of the month."""
    if utils.week_of_month(datetime.today()) in [4]:
        if utils.getLastSentFile0('supplier') < datetime.now() - utils.timedelta(days=7):
            supplierExpirations()
            utils.setLastSentFile('supplier')


if __name__ == '__main__':
    main()
    print("Done.")