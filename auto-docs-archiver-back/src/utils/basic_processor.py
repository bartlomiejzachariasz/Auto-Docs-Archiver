import logging
import re

from dateutil.parser import parse

from src.utils.decorators import log


class BasicProcessor:
    @log
    def process_data(self, data_input):
        data = self.extract_data(data_input=data_input)

        return data

    @log
    def extract_data(self, data_input) -> dict:
        logging.info("extract_data - invoked")

        date = self.parse_date(data_input)

        words = self.extract_words(data_input)

        return {'date': date, 'data': words}


    @log
    def remove_whitespace(self, text) -> str:
        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')
        text = text.replace('\\', ' ')
        return re.sub(' +', ' ', text)

    @log
    def parse_date(self, string):
        try:
            from datetime import date
            import random

            start_date = date.today().replace(day=1, month=1, year=2019).toordinal()
            end_date = date.today().toordinal()
            random_day = date.fromordinal(random.randint(start_date, end_date))
            return str(random_day)
        except ValueError:
            return None

    @log
    def extract_words(self, data) -> list:
        data = self.remove_whitespace(data)
        words = data.split(' ')
        extracted_words = []
        for word in words:
            extracted_words.append(''.join(filter(str.isalpha, word)).lower())
        return extracted_words

