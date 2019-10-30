from PIL import Image
import pytesseract
import re


class Reader:

    def read(self, filename):
        text = self.extract_text(filename)
        return text

    def extract_text(self, filename):
        text = pytesseract.image_to_string(Image.open(filename))
        return text

