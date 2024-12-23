import shutil
from PIL import Image
from pdf2image import convert_from_path
import os
import ocrpng
import utils
from icecream import ic
import re
autofilersdir = r"C:\Users\TimK\Desktop\TKSCANS\autofilers"
import datetime


def main():
    """Searches the TKSCANS folder for PDFs and renames/files them based on the text in the PDF."""
    poppler_path = r'C:\poppler-24.02.0-0\Library\bin'
    my_folder = r'C:\Users\TimK\Desktop\TKSCANS'
    titleimage = None

    # Get the list of files in the folder
    files = os.listdir(my_folder)
    for file in files:
        if file.endswith('.pdf'):
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
                os.remove('ncmmx.png')
            except:
                pass

            # Convert the PDF to a png
            images = convert_from_path(my_file, poppler_path=poppler_path)
            print(len(images))
            images[0].save('out.png', 'PNG')

            # Open the PNG file
            image = Image.open('out.png')        
            recordid = image.crop((100, 350, 400, 405)) # NCM ID

            # Save the cropped image
            recordid.save('ncmmx.png')

            nid = ocrpng.main('ncmmx.png', 'P')
            ic(nid)
            if titleimage:
                title = ocrpng.main('titleimage.png', 'N') #name
                # If theres a newlines in the title, split and return the first line
                if '\n' in title:
                    title = title.split('\n')[0]
                ic(title)
            # caid = ''
            nid = nid.replace('NCM Id:', '')
            caid = nid.strip()        
            nid = nid.replace(' ', '')
            print("ocr: " + nid + "(" + str(len(nid)) + ")")
            # get the current year from today's date using datetime
            thisyear = str(datetime.datetime.now().year)
            lastyear = str(datetime.datetime.now().year - 1)
            
            # so check if the folder exists in this year and last year directories in path K:\Quality - Records\8700 - Control of Nonconforming Product\2024
            # if it does, move the file to that directory and rename it to the NCM ID
            for year in [thisyear, lastyear]:
                if os.path.exists(f"K:\\Quality - Records\\8700 - Control of Nonconforming Product\\{year}\\{nid}"):
                    print(f"Found {nid} in {year}")
                    # if a file already exists in the destination folder, rename our file to the NCM ID plus a number
                    if os.path.exists(f"K:\\Quality - Records\\8700 - Control of Nonconforming Product\\{year}\\{nid}\\{nid}.pdf"):
                        print(f"File already exists in {year} folder. Renaming {nid} to {nid}1")
                        shutil.move(my_file, f"K:\\Quality - Records\\8700 - Control of Nonconforming Product\\{year}\\{nid}\\{nid}1.pdf")
                        break
                    else:
                        shutil.move(my_file, f"K:\\Quality - Records\\8700 - Control of Nonconforming Product\\{year}\\{nid}\\{nid}.pdf")
                        break

            
          


if __name__ == '__main__':
    main()
    print('<<<<<<Nonconformance scan complete.')
    