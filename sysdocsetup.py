import smtplib, ssl, os, re, utils
from email.message import EmailMessage
from datetime import datetime, timedelta
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
                sql = "insert ignore into DOCS_AVAIL (DOCUMENT_ID, CTRL_DOC, LAST_AUDIT) values ('{}', '{}', '{}');".format(docid, path, datetime.now())
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
                sql = "update DOCS_AVAIL set DIST_DOC = '{}' where DOCUMENT_ID = '{}'and DIST_DOC is null;".format(path, docid)
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
        if len(docidArray) == 3:
            # print(docidArray[2])
            base_length = len(docidArray[2])
            if docidArray[2][0] == "1" and base_length > 4:
                doc_folder_path = docidArray[2]
            else:
                doc_folder_path = "0" + docidArray[2]
            # print("==============================================")
            # print("Looking for: '" + doc_folder_path + "'")
            foundControlFolder = False
            for folder in control_doc_folders:
                if doc_folder_path == folder.split(" ")[0]:
                    folder_url = control_doc_url + "\\" + folder
                    # print(folder_url)
                    foundControlFolder = True
                    break
                else:
                    pass

            if foundControlFolder == False:
                print("Document ID: " + docid + " does not have a folder in the control doc folder.")
                continue
            
            procedureFolder = os.listdir(folder_url)
            distroFolder = os.listdir(dist_doc_url)

            for files in procedureFolder:
                fullpath = {}
                # found_p = re.search(r'(CI-[Q]*[M,S][M,P,S]-.*\.(docx)*(pdf)*)', files)
                found_p = re.search(r'(CI-[Q]*[M,S][M,P,S]-.*\.pdf)', files)
                if found_p: #procedures
                    fullpath['id'] = docid
                    fullpath['path'] = folder_url + "\\" + found_p.group(1)
                    upload_list.append(fullpath)
                
                found_f = re.search(r'(F#{4}-[#]*.*\.docx)', files)
                if found_f: # forms
                    fullpath['id'] = docid
                    fullpath['path'] = folder_url + "\\" + found_p.group(1)
                    upload_list.append(fullpath)
                    
            print(f'(upload list 131: {upload_list})')
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
    sqlDistro = "select d.DOCUMENT_ID, d.NAME, da.CTRL_DOC, da.DIST_DOC from DOCUMENTS d left join DOCS_AVAIL da on d.DOCUMENT_ID = da.DOCUMENT_ID where da.DIST_DOC is null;"
    documents = utils.getDatabaseData(sqlDistro)
    distroFolders = os.listdir(dist_doc_url)

    distros = []
    for docid, name, ctrl, dist in documents:
        docidArray = docid.split("-")
        fullpath = {}
        if len(docidArray) == 3:
            # print(docidArray[2])
            base_length = len(docidArray[2])
            if docidArray[2][0] == "1" and base_length > 4:
                doc_folder_path = docidArray[2]
            else:
                doc_folder_path = "0" + docidArray[2]
            print("==============================================")
            print("Looking for: '" + doc_folder_path + "'")
            foundDistroFolder = False
            for folder in distroFolders:
                if doc_folder_path == folder.split(" ")[0]:
                    # print("==============================================")
                    file_url = dist_doc_url + "\\" + folder
                    foundDistroFolder = True
                    if os.path.exists(file_url):
                        # print(f'Folder exists-- {file_url}')
                        foundFolder = os.listdir(file_url)

                        found_procedure = False
                        for files in foundFolder:
                            # found_p = re.search(r'(CI-[Q]*[M,S][M,P,S]-.*\.(docx)*(pdf)*)', files)
                            found_p = re.search(r'(CI-[Q]*[M,P,S][M,P,S]-.*\.pdf)', files)
                            if found_p: #procedures
                                fullpath['id'] = docid
                                fullpath['path'] = file_url + "\\" + found_p.group(1)
                                distros.append(fullpath)
                                print(f'Found procedure: {found_p.group(1)}')
                                found_procedure = True
                            found_f = re.search(r'(^F####-[#]*.*\.docx)', files)
                            if found_f: # forms
                                fullpath['id'] = docid
                                fullpath['path'] = file_url + "\\" + found_p.group(1)
                                distros.append(fullpath)
                                print(f'Found form: {found_f.group(1)}')
                        if found_procedure == False:
                            print(f'No distro procedure found for {docid}')
                    break
                else:
                    pass

            if foundDistroFolder == False:
                print("Document ID: " + docid + " does not have a folder in the distro doc folder.")
                continue
                    
            # print(distro_list)
    # print(f'distros:  {distros}')
    updateDatabaseData(distros)


if __name__ == "__main__":
    print("Starting setup.main================")
    main()
    print("Starting distro====================")
    distro()
    print("Done")
