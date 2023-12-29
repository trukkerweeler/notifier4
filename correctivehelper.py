import os
import shutil
import datetime
import utils


def main():
    """Goes through folders and records and creates folders for new corrective actions."""
    currentyear = datetime.datetime.today().year.__str__()
    cafileslocation = "K:\\Quality - Records\\10200C - Corrective Actions\\" + currentyear
    # get the folder list
    folderlist = os.listdir(cafileslocation)
    # print(folderlist)
    hasfolders = []
    for folder in folderlist:
        caid = folder[0:7]
        hasfolders.append(caid)
    # print(hasfolders)

    sql = "select * from CORRECTIVE where CLOSED = 'N' and year(CORRECTIVE_DATE) = year(curdate())"
    opencas = utils.getDatabaseData(sql)
    # print(opencas)
    for ca in opencas:
        caid = ca[0]
        # print(caid)
        if caid not in hasfolders:
            print(f"CA {caid} does not have a folder.")
            # create the folder
            folder = cafileslocation + "\\" + caid
            os.mkdir(folder)
            # copy CATemplate from parent folder into new folder
            source = cafileslocation + "\\CATemplate.docx"
            destination = folder + "\\CATemplate.docx"
            shutil.copy(source, destination)
            #rename CATemplate to CAID.docx
            os.rename(destination, folder + "\\" + caid + ".docx")

            # # get the attachments
            # sql = "select ATTACHMENT from CORRECTIVE_ATTACHMENT where CORRECTIVE_ID = '{caid}'".format(caid=caid)
            # attachments = utils.getDatabaseData(sql)
            # # print(attachments)
            # for attachment in attachments:
            #     # print(attachment)
            #     # copy the attachment
            #     source = attachment[0]
            #     # print(source)
            #     destination = folder + "\\" + os.path.basename(source)
            #     # print(destination)
            #     shutil.copy(source, destination)
            #     # print("copied")")
        # else:
        #     # print(f"CA {caid} has a folder.")
        #     pass


if __name__ == "__main__":
    main()

