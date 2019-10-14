import logging

from collections import defaultdict

from dateutil.parser import parse


class Processor:
    @staticmethod
    def process_data(data_input):
        logging.info("process_data - invoked")
        date = Processor.parse_date(data_input)
        if date is not None:
            data_input = data_input.replace(date, '')
        data = Processor.word_count(data_input)
        return {'date': date, 'data': data}

    @staticmethod
    def parse_date(string):
        logging.info("parse_date - invoked")
        try:
            return parse(string, fuzzy=True)
        except ValueError:
            return None

    @staticmethod
    def word_count(processed_data):
        logging.info("process_data - invoked")
        words = defaultdict(int)
        for word in processed_data.split(' '):
            words[word] += 1
        return words

    @staticmethod
    def filter_words():
        pass

    @staticmethod
    def group_words(self, words):
        pass


