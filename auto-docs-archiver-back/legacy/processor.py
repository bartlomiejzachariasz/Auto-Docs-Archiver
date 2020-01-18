import logging

from collections import defaultdict

from difflib import get_close_matches

from src.utils.basic_processor import BasicProcessor
from src.utils.decorators import log
from legacy import Words


class Processor(BasicProcessor):
    accepted_parts_of_speech = ["adjective", "verb", "adverb"]

    def __init__(self, db_connector):
        self.words = Words(db_connector=db_connector)

    @log
    def process_data(self, data_input):
        data = self.extract_data(data_input=data_input)

        detailed_words = self.get_words_data(data)

        filtered_words = self.filter_words(detailed_words)

        data['data'] = self.get_most_common_words(self.group_words(filtered_words))

        return data

    @log
    def extract_data(self, data_input) -> dict:
        logging.info("extract_data - invoked")

        date = super().parse_date(data_input)
        if date is not None:
            data_input = data_input.replace(str(date), '')

        words = self.word_count(data_input)

        return {'date': date, 'data': words}

    @log
    def word_count(self, processed_data) -> dict:
        words_counter = defaultdict(int)
        words = super().extract_words(processed_data)

        for word in words:
            words_counter[word] += 1
        return words_counter

    @log
    def get_words_data(self, words):
        detailed_words = []
        for word in words['data']:
            response = self.words.check_for_word(word)

            if response is None:
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
                if len(get_close_matches(word['word'], list(map(lambda x: x['word'], group)), cutoff=0.8)) > 0:
                    group.append(word)
            else:
                groups.append([word])
        return groups

    def get_most_common_words(self, groups):
        most_common_words = []

        for group in groups:
            result = max(group, key=lambda x: x['frequency'])
            most_common_words.append(result)
        return most_common_words
