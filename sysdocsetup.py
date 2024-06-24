import smtplib, ssl, os, re, utils
from email.message import EmailMessage
from datetime import datetime, timedelta
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

PORT = 465
SERVER = "sh10.nethosting.com"
CONTEXT = ssl.create_default_context()
USERNAME = "quality@ci-aviation.com"
PASSWORD = os.getenv('PASSWORDQ')

upload_list = []
distro_list = []
control_doc_url = r'C:\Users\TimK\Documents\QMS'
dist_doc_url = "K:\\Quality"

def customSub(clause_no, file="controlaliases.json"):
    """Add child folder to the url"""
    subfolders_json = utils.getJson(file)
    try:
        subfolders = subfolders_json[clause_no]
    except KeyError:
        subfolders = None
    return subfolders

# insert database data==================================================
def insertDatabaseData(list):
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host=os.getenv('DB_HOST'),
                                             database=os.getenv('DB_NAME'),
                                             user=os.getenv('DB_USER'),
                                             password=os.getenv('DB_PASS'))
        if connection.is_connected():
            cursor = connection.cursor()
            for item in list:
                docid = item['id']
                path = item['path']
                path = path.replace("\\", "\\\\")
                nowdate = datetime.now()
                sql = "insert into DOCS_AVAIL (DOCUMENT_ID, CTRL_DOC, LAST_AUDIT) values ('{}', '{}', '{}') as new on duplicate key update CTRL_DOC = new.CTRL_DOC, LAST_AUDIT = new.LAST_AUDIT;".format(docid, path, nowdate)
                cursor.execute(sql)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

# insert database data==================================================
def updateDatabaseData(list):
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host=os.getenv('DB_HOST'),
                                             database=os.getenv('DB_NAME'),
                                             user=os.getenv('DB_USER'),
                                             password=os.getenv('DB_PASS'))
        if connection.is_connected():
            cursor = connection.cursor()
            for item in list:
                docid = item['id']
                path = item['path']
                path = path.replace("\\", "\\\\")
                # sql = "update DOCS_AVAIL set DIST_DOC = '{}' where DOCUMENT_ID = '{}'and DIST_DOC is null;".format(path, docid)
                sql = "update DOCS_AVAIL set DIST_DOC = '{}' where DOCUMENT_ID = '{}';".format(path, docid)
                cursor.execute(sql)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()



# Document Audit==================================================
def main():
    """Goes through Documents in db and adds control path to DOCS_AVAIL table"""
    # if week of year /2  = then contineu else pass
    if datetime.now().isocalendar()[1] % 2 != 0:
        print("Sysdoc main: Week of year is not even, exiting")
        return
    
    # get all documents that have been issued or revised
    #get all the folders in the control doc folder
    control_doc_folders = os.listdir(control_doc_url)
    distro_doc_folders = os.listdir(dist_doc_url)
    # print(control_doc_folders)
    # print(distro_doc_folders)
    arrNoCtrl = []

    sql3one = "select d.DOCUMENT_ID, d.NAME, da.CTRL_DOC, da.DIST_DOC from DOCUMENTS d left join DOCS_AVAIL da on d.DOCUMENT_ID = da.DOCUMENT_ID where da.LAST_AUDIT is null;"
    documents = utils.getDatabaseData(sql3one)
    
    # print(documents) #prints the documents in the database
    for docid, name, ctrl, dist in documents:
        docidArray = docid.split("-")
        # fullpath = {}
        
        # Format the document ID to get the folder number
        if len(docidArray) == 3: #Procedures
            # print(docidArray[2])
            base_length = len(docidArray[2])
            if docidArray[2][0] == "1" and base_length > 4:
                doc_folder_base = docidArray[2]
            else:
                doc_folder_base = "0" + docidArray[2]
        if len(docidArray) == 2:
            doc_folder_base = docidArray[0]
            doc_folder_base = doc_folder_base.replace("F", "0")
        findfolderthatstartswith = [folder for folder in control_doc_folders if folder.startswith(doc_folder_base)]
        
        # Find the folder that starts with the doc_folder_base
        if len(findfolderthatstartswith) > 0:
            findfolderthatstartswith = findfolderthatstartswith[0]
            if len(findfolderthatstartswith) > 0:
                doc_folder = control_doc_url + "\\" + findfolderthatstartswith
            # Add subfolder from json aliases
            customSubfolder = customSub(doc_folder_base, "json/controlaliases.json")
            if customSubfolder != None:
                doc_folder = doc_folder + "\\" + customSubfolder
        elif len(findfolderthatstartswith) == 0:
            customSubfolder = customSub(doc_folder_base, "json/controlaliases.json")
            ic(customSubfolder)
            if customSubfolder != None:
                doc_folder = control_doc_url + "\\" + customSubfolder
                print(f"Document ID: cannot determine folder for {docid} in the {customSubfolder} folder.")
            else:
                print(f"Document ID: cannot determine folder for {docid} in the control doc folder.")
                doc_folder = control_doc_url
                print(doc_folder)
                continue
        else:
            print(f"Document ID: cannot determine folder for {docid} in the control doc folder.")
            doc_folder = control_doc_url
            print(doc_folder)
            continue

        print("==============================================")
        # ic(findfolderthatstartswith)
        ic("Looking for: '" + docid + "'")
        ic("In: '" + doc_folder + "'")
        for files in os.listdir(doc_folder):
            fullpath = {}
            found_p = re.search(r'(CI-[Q]*[M,S][M,P,S]-.*\.pdf)', files)
            if found_p: #procedures
                fullpath['id'] = docid
                fullpath['path'] = doc_folder + "\\" + found_p.group(1)
                upload_list.append(fullpath)
                print(f'Found procedure: {found_p.group(1)}')
                break
            found_f = re.search(r'F\d{4}-\d{1,2}.*\.(docx|xlsx|oxps|pdf|doc|xls)', files)
            if found_f: # forms
                # ic(f'found_f: {found_f.group(0).split(" ")[0]}')
                # ic(docid.split(" ")[0])
                if found_f.group(0).split(" ")[0] == docid.split(" ")[0]:
                    fullpath['id'] = docid
                    fullpath['path'] = doc_folder + "\\" + found_f.group(0)
                    upload_list.append(fullpath)
                    print(f'Found form: {found_f.group(0)}')
                    break
        
        # procedureFolder = os.listdir(folder_url)
        # distroFolder = os.listdir(dist_doc_url)
    print("upload length: " + str(len(upload_list)))
    print(upload_list)
    if len(upload_list) > 0:
        insertDatabaseData(upload_list)
    else:
        nonStdNaming = "Document ID: " + docid + " does not follow standard naming convention."
        print(nonStdNaming)
    if ctrl is None:
        noCtrl = "Document ID: " + docid + " control is not in the docs avail table."
        print(noCtrl)
        arrNoCtrl.append(noCtrl)
    if len(arrNoCtrl) > 0:
        utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject="Documents not in DOCS_AVAIL", message=str(arrNoCtrl))
            


def distro():
    """Goes through DOCS_AVAIL in db and adds distro path to DOCS_AVAIL table if it is not there"""
    sqlDistro = "select d.DOCUMENT_ID, d.NAME, da.CTRL_DOC, da.DIST_DOC from DOCUMENTS d left join DOCS_AVAIL da on d.DOCUMENT_ID = da.DOCUMENT_ID where (da.DIST_DOC is null or LENGTH(da.DIST_DOC) <2);"
    documents = utils.getDatabaseData(sqlDistro)
    distroFolders = os.listdir(dist_doc_url)

    distros = []
    for docid, name, ctrl, dist in documents:
        print("==============================================")
        print("Looking for: '" + docid + "'")
        docidArray = docid.split("-")
        fullpath = {}
        if len(docidArray) == 3:
            # print(docidArray[2])
            base_length = len(docidArray[2])
            if docidArray[2][0] == "1" and base_length > 4:
                doc_folder_path = docidArray[2]
            else:
                doc_folder_path = "0" + docidArray[2]
        if len(docidArray) == 2: #Forms
            doc_folder_path = docidArray[0]
            doc_folder_path = doc_folder_path.replace("F", "0")
            # doc_folder_path = "0" + doc_folder_path

        print("==============================================")
        ic("Looking for: '" + doc_folder_path + "'")
        foundDistroFolder = False
        for folder in distroFolders:
            if doc_folder_path == folder.split(" ")[0]:
                # print("==============================================")
                file_url = dist_doc_url + "\\" + folder
                # customSubfolder = customSub(folder.split(" ")[0])
                # if customSubfolder != None:
                #     file_url = file_url + "\\" + customSubfolder
                foundDistroFolder = True
                ic(file_url)
                if os.path.exists(file_url):
                    ic(f'Folder exists-- {file_url}')
                    foundFolder = os.listdir(file_url)

                    found_procedure = False
                    for files in foundFolder:
                        file_id = files.split(" ")[0]
                        # ic (f'file_id: {file_id}')
                        # ic (f'document id: {docid}')
                        if file_id == docid:
                            fullpath = {}
                            found_p = re.search(r'(CI-[Q]*[M,S][M,P,S]-.*\.pdf)', files)
                            if found_p: #procedures
                                fullpath['id'] = docid
                                fullpath['path'] = file_url + "\\" + found_p.group(1)
                                distros.append(fullpath)
                                print(f'Found procedure: {found_p.group(1)}')
                                found_procedure = True
                                break
                            else:
                                ic(f'No procedure found for {docid}')
                            # print(files)
                            found_f = re.search(r'F\d{4}-\d{1,2}.*\.(docx|xlsx|oxps|pdf)', files)
                            if found_f: # forms
                                fullpath['id'] = docid
                                fullpath['path'] = file_url + "\\" + found_f.group(0)
                                ic(fullpath)
                                distros.append(fullpath)
                                print(f'Found form: {found_f.group(0)}')
                            else:
                                ic(f'No form found for {docid}')
                break
            else:
                pass

        if foundDistroFolder == False:
            print("Document ID: " + docid + " does not have a folder in the distro doc folder.")
            continue
                    
    # print(f'distros:  {distros}')
    updateDatabaseData(distros)


if __name__ == "__main__":
    # print("Starting setup.main================")
    main()
    # print("Starting distro====================")
    # distro()
    # ic(customSub("08511", "json/distroaliases.json"))
    print("Done")
