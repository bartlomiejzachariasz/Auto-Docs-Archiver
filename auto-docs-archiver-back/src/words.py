import http.client
import json
import operator
from collections import defaultdict

from src.config import WORDS_API
from src.decorators import log


class Words:

    def __init__(self, db_connector):
        self.db_connector = db_connector

        self.api_connector = http.client.HTTPSConnection(WORDS_API["words_url"])

        self.headers = {
            'x-rapidapi-host': WORDS_API["host"],
            'x-rapidapi-key': WORDS_API["key"]
        }

        self.WORDS_API = "/words"

    def get_name(self):
        return self.__class__.__name__

    @log
    def check_for_word(self, word):
        word_result = self.db_connector.find_by_column("words", "word", word)
        if word_result is None:
            data = self.get_word_data(word)
            data = json.loads(data)
            if 'word' not in data.keys():
                return None
            json_data = self.prepare_json_response(data)
            self.save_word(json_data)
            del json_data["_id"]
            return json_data
        else:
            del word_result["_id"]
            return word_result

    @log
    def get_word_data(self, word):
        self.api_connector.request("GET", f"{self.WORDS_API}/{word}", headers=self.headers)
        res = self.api_connector.getresponse()
        data = res.read()
        return data.decode("utf-8")

    @log
    def prepare_json_response(self, json_dict) -> dict:
        json_response = {"word": json_dict["word"], "frequency": json_dict["frequency"]}
        if "results" in json_dict.keys():
            json_response["partOfSpeech"] = self.check_part_of_speech(json_dict["results"])
        else:
            json_response["partOfSpeech"] = "indefinite"

        return json_response


    @log
    def save_word(self, json_data):
        self.db_connector.save("words", json_data)

    @log
    def check_part_of_speech(self, results):
        occurrences = defaultdict(int)

        for result in results:
            occurrences[result["partOfSpeech"]] += 1

        if len(occurrences) == 0:
            return None

        return max(occurrences.items(), key=operator.itemgetter(1))[0]
