import logging
import re

from collections import defaultdict

from dateutil.parser import parse
from difflib import get_close_matches


class Processor:
    accepted_parts_of_speech = ["adjective", "verb", "adverb"]

    @staticmethod
    def process_data(data_input):
        logging.info("process_data - invoked")
        date = Processor.parse_date(data_input)
        if date is not None:
            data_input = data_input.replace(date, '')
        data = Processor.word_count(data_input)
        return {'date': date, 'data': data}

    @staticmethod
    def remove_whitespace(text):
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        return re.sub(' +', ' ', text)

    @staticmethod
    def parse_date(string):
        logging.info("parse_date - invoked")
        try:
            return parse(string, fuzzy=True)
        except ValueError:
            return None

    def extract_words(self, data):
        data = self.remove_whitespace(data)
        words = data.split(' ')
        extracted_words = []
        for word in words:
            extracted_words.append(''.join(filter(str.isalpha, word)))
        return extracted_words

    @staticmethod
    def word_count(processed_data):
        words = defaultdict(int)
        for word in processed_data.split(' '):
            words[word] += 1
        return words

    def filter_words(self, words):
        words = self.filter_parts_of_speech(words)

    def filter_parts_of_speech(self, json_records):
        return filter(lambda record: record["partOfSpeech"] in self.accepted_parts_of_speech, json_records)

    @staticmethod
    def group_words(words):
        groups = []

        for word in words:
            for group in groups:
                if len(get_close_matches(word, group)) > 0:
                    group.append(word)
                else:
                    groups.append([word])
        return groups

    @staticmethod
    def get_most_common_words(groups):
        most_common_words = []

        for group in groups:
            most_common_words.append(max(group, key=lambda x: x['frequency']))
        return most_common_words
