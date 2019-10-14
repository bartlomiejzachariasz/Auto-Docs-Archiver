import http.client
import operator
from collections import defaultdict

from src.config import WORDS_API


class Words:

    def __init__(self, db_connector):
        self.db_connector = db_connector

        self.api_connector = http.client.HTTPSConnection(WORDS_API["words_url"])

        self.headers = {
            'x-rapidapi-host': WORDS_API["host"],
            'x-rapidapi-key': WORDS_API["key"]
        }

        self.WORDS_API = "/words"

    def get_word_data(self, word):
        self.api_connector.request("GET", f"{self.WORDS_API}/{word}", headers=self.headers)
        res = self.api_connector.getresponse()
        data = res.read()
        return data.decode("utf-8")

    @staticmethod
    def prepare_json_response(json_dict):
        return {"word": json_dict["word"], "frequency": json_dict["frequency"],
                "partOfSpeech": Words.check_part_of_speech(json_dict["results"])}

    def check_for_word(self, word):
        word_result = self.db_connector.find_by_column("words", word)
        if word_result is None:
            data = self.get_word_data(word)
            json_data = self.prepare_json_response(data)
            self.save_word(json_data)
            return json_data
        else:
            return word_result

    def save_word(self, json_data):
        self.db_connector.save("words", json_data)

    @staticmethod
    def check_part_of_speech(results):
        occurrences = defaultdict(int)

        for result in results:
            occurrences[result["partOfSpeech"]] += 1

        return max(occurrences.items(), key=operator.itemgetter(1))[0]
