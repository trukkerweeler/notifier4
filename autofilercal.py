import shutil
import time
from PyPDF2 import PdfWriter, PdfReader, PageObject
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import ocrpng
import utils
import re

from icecream import ic

poppler_path = r'C:\poppler-24.02.0-0\Library\bin'

my_folder = r'C:\Users\TimK\Desktop\TKSCANS\autofilers'

titleimage = None

def main():
    """for each file in the folder, if it is a calibration certificate, extract the record id and move the file to the appropriate folder"""
    files = os.listdir(my_folder)
    for file in files:
        if file.endswith('Calibration.pdf') and file.startswith('SKM'):
            front_length = len(file) - 4
            my_file = os.path.join(my_folder, file)
            ic(my_file)

            # Delete out.png if it exists
            try:
                os.remove('out.png')
            except:
                pass

            # Delete outshined.png if it exists
            try:
                os.remove('outshined.png')
            except:
                pass

            # Convert the PDF to a png
            images = convert_from_path(my_file, poppler_path=poppler_path)
            print(len(images))
            images[0].save('out.png', 'PNG')

            # Open the PNG file
            image = Image.open('out.png')

            # crop the image
            mycase = 'CAL'
            recordid = image.crop((1400, 50, 1675, 250)) # WSC certificates       
            
            # Save the cropped image
            recordid.save('outshined.png')

            rid = ocrpng.main('outshined.png', mycase)
            # ic(rid)
            patternsearch = re.search(r'C(I|l)-(\d){3}', rid)
            if patternsearch:
                toolid = patternsearch.group()
                toolid = toolid.replace('l', 'I')
                # ic(toolid)
                
                # iterate through this directory to find a folder that starts with the toolid: K:\Quality - Records\7150 - Calibration\Calibration
                mypath = r'K:\Quality - Records\7150 - Calibration\Calibration'
                for root, dirs, files in os.walk(mypath):
                    for dir in dirs:
                        if dir.startswith(toolid):
                            ic(dir)
                            # extract the scan date from the filename
                            scan_date = "20" + file[8:14]
                            # put the dashes in the date
                            scan_date = scan_date[:4] + '-' + scan_date[4:6] + '-' + scan_date[6:]
                            # rename the file to the toolid
                            new_file = os.path.join(root, dir, toolid + ' ' + scan_date + ' Certificate.pdf')
                            # move the file to the directory
                            shutil.move(my_file, new_file)
                            break
    print('<<<<<<Autofilercal Done')
    
            

if __name__ == '__main__':
    main()