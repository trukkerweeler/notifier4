import shutil
from PIL import Image
from pdf2image import convert_from_path
import os
import ocrpng
import utils
from icecream import ic
import re
autofilersdir = r"C:\Users\TimK\Desktop\TKSCANS\autofilers"


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
                os.remove('preventivemx.png')
            except:
                pass

            # Convert the PDF to a png
            images = convert_from_path(my_file, poppler_path=poppler_path)
            print(len(images))
            images[0].save('out.png', 'PNG')

            # Open the PNG file
            image = Image.open('out.png')        
            # recordid = image.crop((650, 220, 1000, 325)) # PM
            recordid = image.crop((650, 275, 1000, 350)) # PM #This works for the Tig Welder 2024-0912

            # Save the cropped image
            recordid.save('preventivemx.png')

            iid = ocrpng.main('preventivemx.png', 'P')
            ic(iid)
            if titleimage:
                title = ocrpng.main('titleimage.png', 'N') #name
                # If theres a newlines in the title, split and return the first line
                if '\n' in title:
                    title = title.split('\n')[0]
                ic(title)
            caid = ''
            caid = iid.strip()        
            iid = iid.replace(' ', '')
            print("ocr: " + iid + "(" + str(len(iid)) + ")")

            # If Spot Welder in iid, then rename the file
            if 'Spot Welde' in iid or 'SpotWelde' in iid:
                month_date_code = input("Enter the month and date code for file: " + file)
                # replace the first part of the file name with the month date code
                new_file = file.replace(file[:front_length], month_date_code)
                new_file = new_file.replace('.pdf', ' - Spot Welder.pdf')
                ic("new file name: " + new_file)
                shutil.move(my_file, r"K:\Quality - Records\8511 - Equipment\Welder-Spot" + '\\' + new_file)
            
            # If Air Da in iid, then rename the file
            if 'Air Da' in iid or 'AirDa' in iid:
                month_date_code = input("Enter the month and date code for file: " + file)
                # replace the first part of the file name with the month date code
                new_file = file.replace(file[:front_length], month_date_code)
                new_file = new_file.replace('.pdf', ' - Air.pdf')
                ic("new file name: " + new_file)
                shutil.move(my_file, r"K:\Quality - Records\8511 - Equipment\Compressed Air" + '\\' + new_file)
            
            if 'Tumb' in iid:
                new_file = my_file.replace('.pdf', ' - Tumbler.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Tumbler'
                shutil.move(new_file, new_folder)
                print('')
            
            if 'Tig Weld' in iid or 'TigWeld' in iid:
                new_file = my_file.replace('.pdf', ' - Tig Welder.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Welder-TIG'
                shutil.move(new_file, new_folder)
                print('')

            if 'Nexus 8' in iid:
                new_file = my_file.replace('.pdf', ' - Nexus 8.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Mazak Nexus 800-30'
                shutil.move(new_file, new_folder)
                print('')
            
            if 'Nexus 5' in iid:
                new_file = my_file.replace('.pdf', ' - Nexus 5.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Mazak Nexus 510c II'
                shutil.move(new_file, new_folder)
                print('')
            
            if ('iki NH' in iid) or ('iki : NH' in iid) or ('iki: NH' in iid) or ('iki NH' in iid):
                new_file = my_file.replace('.pdf', ' - NH5000.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Mori-Seiki NH5000'
                shutil.move(new_file, new_folder)
                print('')

            if 'Okuma' in iid:
                new_file = my_file.replace('.pdf', ' - Okuma.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Okuma M560V'
                shutil.move(new_file, new_folder)
                print('')

            if 'zak : Quick' in iid:
                new_file = my_file.replace('.pdf', ' - Quick Turn.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Mazak Quick Turn'
                shutil.move(new_file, new_folder)
                print('')
            
            if re.search(r'E(U|T)(D|V)UST(C|L)', iid.upper()):
                print(iid + " matches regex for Dust Collector")
                new_file = my_file.replace('.pdf', ' - Dust Collector.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Wet Dust Collector'
                shutil.move(new_file, new_folder)
                print('')
            
            if 'Acer' in iid:
                new_file = my_file.replace('.pdf', ' - Acer.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Acer Mill'
                shutil.move(new_file, new_folder)
                print('')
            
            if 'SuperMax' in iid:
                new_file = my_file.replace('.pdf', ' - SuperMax.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\SuperMax'
                shutil.move(new_file, new_folder)
                print('')
            
            if 'Air Compr' in iid or 'AirCompr' in iid:
                ic("Air Compressor")
                new_file = my_file.replace('.pdf', ' - Compressor.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Compressed Air'
                shutil.move(new_file, new_folder)
                print('')
            
            # if my_file exists
            if os.path.isfile(my_file):
                movers = ['mer)', 'Bee', 'Citric', 'Nitric', 'TypeII', 'Deburr', 'Alodine1600']
                for mover in movers:
                    # ic("mover: " + mover)
                    # ic("iid: " + iid)
                    if mover in iid:
                        # Move new file to autofilers
                        ic('Moving ' + my_file + ' to ' + autofilersdir)                                                                                                                                                                                                                                                             
                        shutil.move(my_file, autofilersdir)
                        ic('')

            # ITW GEMA Powder Gun
            if re.search(r'(P|F)OW(D|O)ER', iid.upper()):
                new_file = my_file.replace('.pdf', ' - Gema Powder Gun.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\GEMA'
                shutil.move(new_file, new_folder)
                print('')
            
            # Mechanical Shear
            if re.search(r'EC(H|N)(ANI)C', iid.upper()):
                new_file = my_file.replace('.pdf', ' - Mechanical Shear.pdf')
                os.rename(my_file, new_file)
                print(new_file)
                # Move new file to a new folder
                new_folder = r'K:\Quality - Records\8511 - Equipment\Shear - Amada'
                shutil.move(new_file, new_folder)
                print('')
          


if __name__ == '__main__':
    main()
    