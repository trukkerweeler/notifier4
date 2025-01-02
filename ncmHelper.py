import os
import utils
from datetime import datetime
from icecream import ic

def makeNcmFolders():
    # get 4-digit current year
    year = datetime.now().strftime("%Y")
    my_path = r"K:\Quality - Records\8700 - Control of Nonconforming Product"+ "\\" + year
    # ic("my_path", my_path)
    # Cheeck if the path exists, if not create it
    if not os.path.exists(my_path):
        os.makedirs(my_path)
        ic("my_path created", my_path)    

    # make array of the folders in the path
    folders = os.listdir(my_path)
    sql = "select NCM_ID, CLOSED from NONCONFORMANCE where CLOSED = 'N'"
    data = utils.getDatabaseData(sql)
    for (ncm_id, closed) in data:
        for folder in folders:
            if ncm_id in folder:
                # ic("ncm_id", ncm_id, "folder", folder)
                break
        else:
            # ic("ncm_id", ncm_id, "not found")
            # create folder
            folder_path = my_path + "\\" + ncm_id
            os.mkdir(folder_path)
            ic("folder_path", folder_path)
    
    ic("makeNcmFolders done")
        
        
def main():
    makeNcmFolders()

if __name__ == "__main__":
    main()