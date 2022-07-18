import tesserocr
from PIL import Image
import cv2
import pytesseract
#import easyocr
from ppocronnx.predict_system import TextSystem
text_sys = TextSystem()

#print(tesserocr.tesseract_version())  # print tesseract-ocr version
#print(tesserocr.get_languages())  # prints tessdata path and list of available languages

#image = Image.open('/home/jin/下载/2CFDB9FCF5B4C4055A873747E47AC4BF.jpg')
#print(type(image))
#print(tesserocr.image_to_text(image))  # print ocr text from image
# or
#print(tesserocr.file_to_text('/home/jin/下载/2CFDB9FCF5B4C4055A873747E47AC4BF.jpg'))

#reader = easyocr.Reader(['en'])
img = text_sys.ocr_single_line(cv2.imread('0543AA8C23446DBC62EE7227B0FC3E3D.jpg'))
print(img[0])
# Adding custom options
#custom_config = r'--oem 3 --psm 6'
#print(pytesseract.image_to_string(img, config=custom_config))
