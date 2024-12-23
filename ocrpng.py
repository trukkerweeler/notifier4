import pytesseract
from PIL import Image
from icecream import ic
# C:\Users\TimK\AppData\Local\Programs\Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\TimK\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# Modified for calibrations!!!!!!!!!!!!!!!!

def main(my_file, mycase):
    # Open the PNG file
    image = Image.open(my_file)
    
    text = pytesseract.image_to_string(image)
    # text = pytesseract.image_to_string(image, config='-c tessedit_char_whitelist=CI-0123456789 --psm 6')
    text = text.strip()

    return text

if __name__ == "__main__":
    my_file = r'rotated_outshined.png'
    text = main(my_file, 'T')
    ic(text)
    ic(len(text))