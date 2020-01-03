import os
import pandas as pd

from stempel import StempelStemmer
from sklearn import model_selection, naive_bayes, svm
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.basic_processor import BasicProcessor
from src.resources.config import DATA_CONFIG


class Classifier:
    def __init__(self):
        self.DATASET_PATH = DATA_CONFIG["data_path"]
        self.corpus = None
        self.bayes = None
        self.svm_model = None
        self.stemmer = StempelStemmer.polimorf()
        self.processor = BasicProcessor()
        self.tfidf = TfidfVectorizer(max_features=5000)
        self.encoder = LabelEncoder()
        self.stop_words = self.read_file(DATA_CONFIG["stopwords_path"]).split(
            '\n')
        self.codes_map = {
            "POWTRZ": "Wniosek o powtórzenie roku studiów/powtarzanie przedmiotu",
            "PRZEP": "Wniosek o przepisanie oceny",
            "WYKR": "Wniosek o wykreślenie z listy studentów",
            "IPS": "Wniosek o Indywidualny Program Studiów",
            "ECTS": "Wniosek o kontynuowanie studiów z deficytem punktów ECTS",
            "INZ": "Rejestracja pracy inżynierskiej",
            "DZIEKAN": "Podanie do dziekana",
            "PRAKT": "Wniosek o zgodę na odbycie praktyki studenckiej",
            "WARUN": "Wniosek o wpis warunkowy",
            "REAKT": "Wniosek o reaktywację studiów",
            "LIC": "Rejestracja pracy licencjackiej"
        }
        self.get_data()
        self.train_model()

    def train_model(self):
        train_X, test_X, train_Y, test_Y = model_selection.train_test_split(self.corpus['text_final'],
                                                                            self.corpus['title'],
                                                                            test_size=0.3)

        train_Y = self.encoder.fit_transform(train_Y)
        test_Y = self.encoder.fit_transform(test_Y)

        self.tfidf.fit(self.corpus['text_final'])

        train_X_tfidf = self.tfidf.transform(train_X)
        test_X_tfidf = self.tfidf.transform(test_X)

        self.bayes = naive_bayes.MultinomialNB()
        self.bayes.fit(train_X_tfidf, train_Y)

        self.svm_model = svm.SVC(C=65536.0, degree=3, gamma=1.52587890625e-05)
        self.svm_model.fit(train_X_tfidf, train_Y)

    def get_data(self):
        dataset = os.listdir(self.DATASET_PATH)
        data = []
        for datafile in dataset:
            if datafile == '.DS_Store':
                continue
            data.append(self.prepare_row(self.DATASET_PATH + '/' + datafile, self.processor))

        self.corpus = pd.DataFrame(data)
        self.corpus = self.prepare_dataframes(self.corpus, self.stop_words)

    def prepare_dataframes(self, dataframes, stop_words):
        for index, row in dataframes.iterrows():
            row['text'] = [entry.lower() for entry in row['text'] if entry != '']

        for index, entry in enumerate(dataframes['text']):
            final_words = []
            for word in entry:
                if word not in stop_words:
                    final_words.append(self.stemmer.stem(word))
            dataframes.loc[index, 'text_final'] = str(final_words)
        return dataframes

    def prepare_row(self, filename, processor):
        with open(filename, 'r') as f:
            row = {}
            row['text'] = processor.extract_words(f.read())
            fn = filename.split('/')[-1]
            row['title'] = fn.split('_')[0]
            return row

    def predict_title(self, processed_data, method='SVC'):
        if method == 'SVC':
            return self.svm_model.predict(processed_data)
        elif method == 'bayes':
            return self.bayes.predict(processed_data)

    def classify(self, text):
        row = {}
        row['text'] = text
        df = pd.DataFrame([row])
        df = self.prepare_dataframes(df, self.stop_words)
        sample = self.tfidf.transform(df.iloc[0]['text'])
        predicted = self.predict_title(sample)
        predicted_label = max(set(predicted.tolist()), key=predicted.tolist().count)
        code = self.encoder.inverse_transform([predicted_label])
        return self.get_title_from_code(code.tolist()[0])

    def get_title_from_code(self, code):
        if code in self.codes_map.keys():
            return self.codes_map[code]
        else:
            return "Dokument nierozpoznany"

    def read_file(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
        return text
