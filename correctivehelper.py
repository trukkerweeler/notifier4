import os
import shutil
import datetime
import utils
from icecream import ic



def makeproject():
    '''Creates a project in the PROJECT table for Audit Corrective Actions.'''
    # How to determine which require projects?
    sql = "select * from CORRECTIVE where CLOSED = 'N' and year(CORRECTIVE_DATE) = year(curdate())"
    opencas = utils.getDatabaseData(sql)


def makedirectory():
    """Goes through folders and records and creates folders for new corrective actions."""
    currentyear = datetime.datetime.today().year.__str__()
    cafileslocation = "K:\\Quality - Records\\10200 - Corrective Actions\\" + currentyear
    
    # if the year folder does not exist, create it
    if not os.path.exists(cafileslocation):
        os.mkdir(cafileslocation)

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
            catitle = utils.getcatitle(caid)
            if catitle:
                folder = folder + " - " + catitle
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
    ic("Make CA directory - Done.")

def creatercainput():
    """Go through CAR PROJECTS and create input for RCA where it doesn't exist."""
    text = "Please provide root case analysis. Use 5-why methodology for determining root cause. Root cause cannot be a restatement of the finding."
    sql = """select * from PROJECT p left join PEOPLE_INPUT pi on p.PROJECT_ID = pi.PROJECT_ID 
    where p.CLOSED = 'N' and PROJECT_TYPE = 'CAR' and pi.PROJECT_ID is null"""
    opencas = utils.getDatabaseData(sql)
    for ca in opencas:
        caid = ca[0]
        assto = ca[2]
        input = {"PROJECT_ID": caid, "PEOPLE_ID": "TKENT", "ASSIGNED_TO": assto, "SUBJECT": "RCA", "CREATED_BY": "CIQMS", "TEXT": text}
        utils.insertInput(input)
        
def createicainput(): #immediate corrective action
    """Go through CAR PROJECTS and create input for immediate action where it doesn't exist."""
    text = "Please take immediate action to correct the issue. Document the action taken and the results of the action including dates."
    sql = """SELECT DISTINCT p.* 
            FROM PROJECT p 
            left join CORRECTIVE c on concat('CAR', c.CORRECTIVE_ID) = p.PROJECT_ID
            WHERE p.CLOSED = 'N' 
            AND p.PROJECT_TYPE = 'CAR' 
            and c.CLOSED = 'N'
            AND NOT EXISTS (
                SELECT 1 
                FROM PEOPLE_INPUT pi 
                WHERE pi.PROJECT_ID = p.PROJECT_ID 
                    AND pi.SUBJECT = 'ICA'
            );"""
    opencas = utils.getDatabaseData(sql)
    # ic(opencas)
    for ca in opencas:
        caid = ca[0]
        assto = ca[2]
        input = {"PROJECT_ID": caid, "PEOPLE_ID": "TKENT", "ASSIGNED_TO": assto, "SUBJECT": "ICA", "CREATED_BY": "CIQMS", "TEXT": text}
        utils.insertInput(input)
        
def updatecaprojects():
    """for CAs that dont reference a project id, add project id reference to PROJECT if there is a project ."""
    sql = "select * from CORRECTIVE where PROJECT_ID is null and CLOSED = 'N'"
    opencas = utils.getDatabaseData(sql)
    for ca in opencas:
        caid = ca[0]
        sql = "select * from PROJECT where PROJECT_ID = CONCAT('CAR','{caid}')".format(caid=caid)
        project = utils.getDatabaseData(sql)
        if project:
            projectid = project[0][0]
            sql = "update CORRECTIVE set PROJECT_ID = '{projectid}' where CORRECTIVE_ID = '{caid}'".format(projectid=projectid, caid=caid)
            # ic(sql)
            utils.updateDatabaseData(sql)
            print(f"CA {caid} has been updated with project {projectid}.")
        else:
            print(f"CA {caid} does not have a project.")
    ic("Done.")

def main():
    """Creates folders on the network for new corrective actions; creates input for RCA where it doesn't exist."""
    makedirectory()
    creatercainput() #Root cause analysis
    createicainput() #Immediate corrective action
    updatecaprojects()
    ic("Corrective Helper -main- Done.")

    

if __name__ == "__main__":
    main()
    # create project for Audit Corrective Actions?
    # makeproject()
    ic("Done.")

