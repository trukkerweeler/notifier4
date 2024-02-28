import utils
# from email.message import EmailMessage
from datetime import datetime, timedelta
import sysdoc, sysdocsetup, corrective, input, supplier, noninvshl, recurring, project, correctivehelper, competency


def formatOverdueASL(overdueASL):
    formattedOverdueASL = "<table><tr><th>Supplier ID</th><th>Name</th><th>City</th><th>Active</th><th>QMS</th><th>Certificate</th><th>Expiry</th><th>Scope</th><th>Comments</th></tr>"
    for row in overdueASL:
        formattedOverdueASL += "<tr>"
        for item in row:
            formattedOverdueASL += "<td>" + str(item) + "</td>" 
        formattedOverdueASL += "</tr>"
    formattedOverdueASL += "</table>"
    return formattedOverdueASL


# def main():
    
    # Annual Quality Policy Review==(QAM 5.3))=================================
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


if __name__ == "__main__":
    competency.main()
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
    # project.main('TANDERSON')
    print("Done.")