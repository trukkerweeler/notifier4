import pytesseract
from PIL import Image
from icecream import ic
# C:\Users\TimK\AppData\Local\Programs\Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\TimK\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def main(my_file, mycase):
    # Open the PNG file
    image = Image.open(my_file)

    # Apply OCR using pytesseract
    if mycase in ['T', 'C', 'O', 'V']:
        # text = pytesseract.image_to_string(image, config='-c tessedit_char_whitelist=0123456789- --psm 6')
        text = pytesseract.image_to_string(image, config='-c tessedit_char_whitelist=0123456789 --psm 6')
    elif mycase in ['H']:
        text = pytesseract.image_to_string(image, config='-c tessedit_char_whitelist=JanuryFebMchApilMJlgStONvD01234567890/ --psm 6')
        
    else:
        text = pytesseract.image_to_string(image)
    text = text.strip()
    # if there is a carriage return in the text, return the text before the carriage return
    if text.find('\n') > 0:
        text = text.split('\n')[0]

    return text

if __name__ == "__main__":
    my_file = r'rotated_outshined.png'
    text = main(my_file, 'T')
    ic(text)
    ic(len(text))