import utils
# from email.message import EmailMessage
from datetime import datetime, timedelta
import sysdoc, sysdocsetup, corrective, input, supplier, noninvshl, recurring, project, correctivehelper


def formatOverdueASL(overdueASL):
    formattedOverdueASL = "<table><tr><th>Supplier ID</th><th>Name</th><th>City</th><th>Active</th><th>QMS</th><th>Certificate</th><th>Expiry</th><th>Scope</th><th>Comments</th></tr>"
    for row in overdueASL:
        formattedOverdueASL += "<tr>"
        for item in row:
            formattedOverdueASL += "<td>" + str(item) + "</td>" 
        formattedOverdueASL += "</tr>"
    formattedOverdueASL += "</table>"
    return formattedOverdueASL


def main():
    """Goes through tables and identifies overdue items. Sends email to appropriate people."""
    # Training==================================================
    sql2 = "select * from CTA_ATTENDANCE where datediff(Now(),EXPIRATION_DATE)>1;"
    overDueTraining = utils.getDatabaseData(sql2)
    overDueTraining = "Overdue Training: \n" + str(overDueTraining) + "\n"
    print(overDueTraining)
    if overDueTraining != "Overdue Training: \n[]\n":
        utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject="Overdue Training", message=overDueTraining)
    else:
        print("No overdue training")


    # Annual Quality Policy Review==(QAM 5.3))=================================
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


if __name__ == "__main__":
    main()
    sysdocsetup.main()
    sysdocsetup.distro()
    sysdoc.main()
    corrective.main()
    correctivehelper.main()
    input.main()
    supplier.main()
    noninvshl.main()
    recurring.main()
    project.main('CHARRISON')
    project.main('MTIPPETTS')
    project.main('RMATSAMAS')
    print("Done.")