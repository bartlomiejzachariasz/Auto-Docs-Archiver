import logging
import re

from collections import defaultdict

from dateutil.parser import parse
from difflib import get_close_matches

from src.decorators import log
from src.words import Words


class Processor:
    accepted_parts_of_speech = ["adjective", "verb", "adverb"]

    def get_name(self):
        return self.get_name()

    @log
    def __init__(self, db_connector):
        self.words = Words(db_connector=db_connector)

    @log
    def process_data(self, data_input):
        data = self.extract_data(data_input=data_input)

        detailed_words = self.get_words_data(data)

        filtered_words = self.filter_words(detailed_words)

        return filtered_words

    @log
    def extract_data(self, data_input) -> dict:
        logging.info("extract_data - invoked")

        date = self.parse_date(data_input)
        if date is not None:
            data_input = data_input.replace(date, '')

        words = self.word_count(data_input)

        return {'date': date, 'data': words}

    @log
    def remove_whitespace(self, text) -> str:
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        return re.sub(' +', ' ', text)

    @log
    def parse_date(self, string):
        try:
            return parse(string, fuzzy=True)
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

    @log
    def word_count(self, processed_data) -> dict:
        words_counter = defaultdict(int)
        words = self.extract_words(processed_data)

        for word in words:
            words_counter[word] += 1
        return words_counter

    @log
    def get_words_data(self, words):
        detailed_words = []
        for word in words:
            response = self.words.check_for_word(word)
            if word is not None:
                continue

            detailed_words.append(response)

        return detailed_words

    def filter_words(self, words) -> list:
        return list(self.filter_parts_of_speech(words))

    def filter_parts_of_speech(self, words):
        return filter(lambda record: record["partOfSpeech"] in self.accepted_parts_of_speech, words)

    def group_words(self, words) -> list:
        groups = []

        for word in words:
            for group in groups:
                if len(get_close_matches(word, group)) > 0:
                    group.append(word)
                else:
                    groups.append([word])
        return groups

    def get_most_common_words(self, groups):
        most_common_words = []

        for group in groups:
            most_common_words.append(max(group, key=lambda x: x['frequency']))
        return most_common_words
