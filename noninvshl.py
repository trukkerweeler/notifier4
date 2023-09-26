import pandas as pd
import datetime as dt
import utils

def noninvshl():
    # xlfile = r"C:\Users\timK\Documents\Non Inventory Expirations.xls"
    xlfile = r"K:\Quality\08540 - Preservation\Non Inventory Expirations.xls"
    df = pd.read_excel(xlfile, sheet_name="Sheet1", header=0, index_col=None, usecols="A:G", engine="xlrd")
    print(df)
    for row in df.iterrows():
        # print(row[0])
        # print(row[1])
        po = row[1]['PO']
        part = row[1]['PART']
        description = row[1]['DESCRIPTION']
        lot = row[1]['LOT/BATCH']
        dom = row[1]['DOM']
        doe = row[1]['DOE']
        disposition = row[1]['DISPOSITION']

        # print(f"{po} {part} {description} {lot} {dom} {doe} {disposition}")
        # print(type(doe))
        dtDoe = dt.datetime.strptime(str(doe), '%Y-%m-%d %H:%M:%S')
        dtDoe = dtDoe.date()
        # print(dtDoe)

        print(dtDoe - dt.date.today())

        if disposition not in ['Q', 'NF']:
            if dtDoe - dt.date.today() < dt.timedelta(days=30) and dtDoe - dt.date.today() > dt.timedelta(days=-500):
                notification = (f"{po} {part} {description} {lot} {dom} {dtDoe} {disposition}")
                # print("Yep")
                utils.sendMail(to_email=["ritam@ci-aviation.com"], subject=f"Expired Material Report: {po}", message=notification, cc_email=["tim.kent@ci-aviation.com"])
            
            else:
                print("Nope")

    #     print(row['DESCRIPTION'][row])
    #     if row[0] == 0:
    #         print(row)
    #     else:
    #         pass
    # print(df.columns)
    # print(df.dtypes)
    # print(df["DESCRIPTION"])
    # print(df["Expiry Date"].dtypes)
    # print(df["Expiry Date"].dt.date)
    # print(df["Expiry Date"].dt.date[0])
    # print(type(df["Expiry Date"].dt.date[0]))
    # print(df["Expiry Date"].dt.date[0] - dt.date.today())
    # print(type(df["Expiry Date"].dt.date[0] - dt.date.today()))
    # print((df["Expiry Date"].dt.date[0] - dt.date.today()).days)
    # print(type((df["Expiry Date"].dt.date[0] - dt.date.today()).days))
    # print(df["Expiry Date"].dt.date[0] - dt.date.today() < dt.timedelta(days=30))
    # print(type(df["Expiry Date"].dt.date[0] - dt.date.today() < dt.timedelta(days=30)))
    # print(df["Expiry Date"].dt.date[0] - dt.date.today() < dt.timedelta(days=30) and df["Expiry Date"].dt.date[0] - dt.date.today() > dt.timedelta(days=0))


def main():
    """Read excel file and identify non-inventory items that are expiring soon."""
    if utils.getLastSentFile('noninvshl') < dt.datetime.today() - dt.timedelta(days=10):
        noninvshl()
        utils.setLastSentFile('noninvshl')
    else:
        print("Not sending non-inventory expirations, too soon or off-hours. Last sent +10: " + str(utils.getLastSentFile('noninvshl')) + " Current: " + str(dt.datetime.today()))

if __name__ == "__main__":
    main()
    print("Done.")