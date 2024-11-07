import pandas as pd
import datetime as dt
import utils
import icecream as ic

def noninvshl():
    # xlfile = r"C:\Users\timK\Documents\Non Inventory Expirations.xls"
    xlfile = r"K:\Quality\08540 - Preservation\Non Inventory Expirations.xls"
    df = pd.read_excel(xlfile, sheet_name="Sheet1", header=0, index_col=None, usecols="A:G", engine="xlrd")
    print(df)
    # notification = "<html><body><h3>Non-Inventory Expirations</h3>\n"
    # notification += "<table border=1><tr><th>PO</th><th>Part</th><th>Description</th><th>Lot</th><th>DOM</th><th>DOE</th><th>Disposition</th></tr>"
    notification = "Non-Inventory Expirations\n"
    notification += "PO      Part                 Description          Lot                  DOM        Expiration   Disposition\n"
    for row in df.iterrows():
        # print(row[0])
        # print(row[1])
        po = str(row[1]['PO'])
        while len(po) < 7:
            po = po + " "
        # if there is a period in the po, split it and use the first part
        if "." in po:
            po = po.split(".")[0]
        part = str(row[1]['PART'])
        while len(part) < 20:
            part = part + " "
        description = str(row[1]['DESCRIPTION'])
        while len(description) < 20:
            description = description + " "
        lot = str(row[1]['LOT/BATCH'])
        while len(lot) < 20:
            lot = lot + " "
        dom = row[1]['DOM']
        if dom == "nan":
            dom = "--"
        else:
            # remove time from date
            dom = str(dom)[0:10]
        while len(dom) < 10:
            dom = dom + " "

        doe = row[1]['DOE']
        # while len(str(doe)) < 10:
        #     doe = doe + " "
        disposition = str(row[1]['DISPOSITION'])
        if disposition == "nan":
            disposition = ""
            while len(disposition) < 10:
                disposition = disposition + " "
        # print(f"{doe} {type(doe)}")
        if isinstance(doe, dt.datetime):
            try:
                dtDoe = dt.datetime.strptime(str(doe), '%Y-%m-%d %H:%M:%S')
                dtDoe = dtDoe.date()
            except:
                print(f"Error converting {doe} to date, po: {po} part: {part} description: {description} lot: {lot} dom: {dom} disposition: {disposition}")

            # dtDoe = dt.datetime.strptime(str(doe), '%Y-%m-%d %H:%M:%S')
            # dtDoe = dtDoe.date()
            # # print(dtDoe)

            # print(dtDoe - dt.date.today())

            if disposition not in ['C', 'NF', 'D']:
                if dtDoe - dt.date.today() < dt.timedelta(days=30) and dtDoe - dt.date.today() > dt.timedelta(days=-500):
                    # notification += (f"<tr><td>{po}</td><td>{part}</td><td>{description}</td><td>{lot}</td><td>{dom}</td><td>{dtDoe}</td><td>{disposition}</td></tr>")
                    notification += (f"{po} {part} {description} {lot} {dom} {dtDoe} {disposition}\n")
                    # print("Yep")
    # notification += "</table><br></body></html>"    
    #Send the email
    # utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject=f"Expired Material Items", message=notification, cc_email=["tim.kent@ci-aviation.com"])
    # create datetime object for today remove the time
    mydate = dt.datetime.today()
    mydate = mydate.date()

    utils.sendMail(to_email=["ritam@ci-aviation.com", "craig@ci-aviation.com"], subject=f"Expiring Material Items: {mydate}", message=notification, cc_email=["tim.kent@ci-aviation.com"])
    

def main():
    """If week of month is 1 or 3: Read excel file and identify non-inventory items that are expiring soon; Send email"""
    test=0
    print("Starting non-inventory expirations...")
    lsdt = utils.getLastSentFile0('noninvshl')
    # print(lsdtplus10)
    
    if test == 1:
        noninvshl()
    else:
        # if days since last sent is greater than 7 and week of month is 1 or 3, send email and update last sent file
        if lsdt < dt.datetime.today() - dt.timedelta(days=7) and utils.week_of_month(dt.datetime.today()) in [1, 3]:
            noninvshl()
            utils.setLastSentFile('noninvshl')
        else:
            print("Not sending non-inventory expirations, too soon or off-hours. Last sent +10: " + str(utils.getLastSentFile('noninvshl')) + " Current: " + str(dt.datetime.today()))



if __name__ == "__main__":
    main()
    print("Done.")