import nltk
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import ngrams

urllist = {"",
           ""}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)
        self.btn_search.clicked.connect(self.btn_search_clicked)
        self.text_ngrams_map = []
        self.read_test_examples()
        nltk.download('punkt')

    def read_test_examples(self):
        pass

    def btn_search_clicked(self):
        result = ""
        str = self.textEdit_search.toPlainText()
        html = urlopen(str).read()
        soup = BeautifulSoup(html)
        raw = soup.get_text()
        temp_map = self.calculate_ngrams(raw)
        print(raw)

    def calculate_ngrams(self, text: str):
        result = {}
        for token in nltk.sent_tokenize(text):
            for i in range(0, 4):
                for grams in ngrams(token.split(), i):
                    if result.get(" ".join(grams)):
                        result[" ".join(grams)] += 1
                    else:
                        result[" ".join(grams)] = 1
                    print(grams)
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return result
