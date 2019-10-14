from PIL import Image
import pytesseract
import re


class Reader:

    def read(self, filename):
        text = self.extract_text(filename)
        return text

    def extract_text(self, filename):
        text = pytesseract.image_to_string(Image.open(filename))
        prepared_text = self.prepare_text(text)
        return prepared_text

    def prepare_text(self, text):
        return self.remove_whitespace(text)

    @staticmethod
    def remove_whitespace(text):
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        return re.sub(' +', ' ', text)
