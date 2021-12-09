import nltk
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import ngrams, RegexpTokenizer
from regex import split

nltk.download('punkt')

urllist = {"https://en.wikipedia.org/wiki/Dog": "ENG",
           "https://en.wikipedia.org/wiki/Cat": "ENG",
           "https://en.wikipedia.org/wiki/Dragon": "ENG",
           "https://en.wikipedia.org/wiki/University": "ENG",
           "https://en.wikipedia.org/wiki/Unreal_Engine": "ENG",
           "https://es.wikipedia.org/wiki/Canis_familiaris": "ESP",
           "https://es.wikipedia.org/wiki/Felis_silvestris_catus": "ESP",
           "https://es.wikipedia.org/wiki/Drag%C3%B3n": "ESP",
           "https://es.wikipedia.org/wiki/Unreal_Engine": "ESP",
           "https://es.wikipedia.org/wiki/Universidad": "ESP"}


class NeuronMethod:
    __slots__ = ('_path_to_file', '_content')

    LANGUAGES = {'en': 'ENGLISH', 'es': 'SPANISH'}

    def __init__(self, path_to_file: str) -> None:
        self._path_to_file = path_to_file
        self.read_file()

    def read_file(self) -> None:
        with open(self._path_to_file, 'r', encoding='utf-8') as file:
            self._content = file.read()

    @property
    def get_result(self) -> str:
        from langdetect import detect
        return self.LANGUAGES.get(detect(self._content))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)
        self.btn_search.clicked.connect(self.btn_search_clicked)
        self.text_ngrams_map = []
        self.data_list = []
        self.create_data_dictionary()

    def btn_search_clicked(self):
        result = ""
        str = self.textEdit_search.toPlainText()
        html = urlopen(str).read()
        soup = BeautifulSoup(html)
        raw = soup.get_text()
        alpha_map = self.calculate_alpha(raw)
        temp_map = self.calculate_ngrams(raw)
        res = self.detect_language(temp_map)
        result = self.detect_lang_alpha(alpha_map)
        print(result)
        print(res)
        print(NeuronMethod('test_english.html').get_result)

    def calculate_ngrams(self, text: str):
        result = {}
        for token in nltk.sent_tokenize(text):
            for i in range(0, 4):
                for grams in ngrams(token.lower().split(), i):
                    if result.get(" ".join(grams)):
                        result[" ".join(grams)] += 1
                    else:
                        result[" ".join(grams)] = 1
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return result

    def calculate_alpha(self, text: str):
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)
        letters = {}
        for word in words:
            for letter in list(word.lower()):
                if letters.get(letter):
                    letters[letter] += 1
                else:
                    letters[letter] = 1
        result = sorted(letters.items(), key=lambda x: x[1], reverse=True)
        print(result)
        return result

    def create_data_dictionary(self):
        for url in urllist:
            html = urlopen(url).read()
            soup = BeautifulSoup(html)
            raw = soup.get_text()
            temp_map = self.calculate_ngrams(raw)
            alpha_map = self.calculate_alpha(raw)
            temp_list = [(t[0]) for t in temp_map]
            alpha_list = [(t[0]) for t in alpha_map]
            self.data_list.append((urllist[url], temp_list, alpha_list, url))

    def detect_language(self, ngram_list_amount):
        result = [1111111111, "url", "lang"]
        for example in self.data_list:
            value = 0
            for ngram in list(ngram_list_amount)[:100]:
                local_pos = ngram_list_amount.index(ngram)
                if ngram[0] in example[1]:
                    db_pos = example[1].index(ngram[0])
                    diff = abs(local_pos - db_pos)
                    value += diff
                else:
                    value += len(ngram_list_amount)
            if result[0] > value:
                result[0] = value
                result[1] = example[3]
                result[2] = example[0]
        return result

    def detect_lang_alpha(self, alpha_list):
        result = [1111111111, "url", "lang"]
        for example in self.data_list:
            value = 0
            for letter in alpha_list[:50]:
                local_pos = alpha_list.index(letter)
                if letter[0] in example[2]:
                    db_pos = example[2].index(letter[0])
                    diff = abs(local_pos - db_pos)
                    value += diff
                else:
                    value += len(alpha_list)
            if result[0] > value:
                result[0] = value
                result[1] = example[3]
                result[2] = example[0]
        return result
# TODO: add urlist and all comparable urls
