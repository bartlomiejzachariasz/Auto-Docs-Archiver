from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import WordNetLemmatizer

from src.utils.basic_processor import BasicProcessor
from src.utils.ocr import Reader

stop_words = set(stopwords.words("english"))

ps = PorterStemmer()

lem = WordNetLemmatizer()

reader = Reader()
text = reader.read()

basic_processor = BasicProcessor()
words = basic_processor.process_data()


