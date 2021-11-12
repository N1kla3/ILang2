import nltk
from urllib.request import urlopen
from PyQt5 import QtWidgets
from bs4 import BeautifulSoup
from MainWindow import MainWindow

def print_hi(name):
    url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    raw = soup.get_text()
    print(raw)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

