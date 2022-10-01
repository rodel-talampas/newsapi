# main.py

import sys
from logging import Logger
from news import SearchNews

from PyQt6.QtCore import Qt, QAbstractTableModel

from PyQt6.QtWidgets import QApplication, QFormLayout, QVBoxLayout, QTableView, QPushButton, QLabel, QMainWindow, QLineEdit, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        layout = QVBoxLayout()
        self.setLayout(layout)

        formLayout = QFormLayout()
        layout.addLayout(formLayout)

        self.setWindowTitle("Latest News")
        self.setFixedWidth(800)
        self.setFixedHeight(1000)
        titleMsg = QLabel("Latest News", parent=self)
        titleMsg.move(60, 10)

        self.lblSearch = QLabel("Text Search: ", parent=self)
        self.lblSearch.move(5, 45)
        self.lblSort = QLabel("Sort by: ", parent=self)
        self.lblSort.move(5, 85)

        self.searchBox = QLineEdit(self)
        self.searchBox.move(100, 45)
        self.searchBox.textChanged.connect(self._data_update)

        self.sortField = QComboBox(self)
        self.sortField.move(90,85)
        self.sortField.addItem("author")
        self.sortField.addItem("title")
        self.sortField.addItem("publishAt")
        self.sortField.currentTextChanged.connect(self._data_update)   

        self.searchButton = QPushButton("Search", self)
        self.searchButton.move(200,85)
        self.searchButton.setEnabled(False)
        self.searchButton.clicked.connect(self._search_news)

        self.table = QTableView()
        self.table.move(5, 150)
        self.table.setModel(self.model)

    def _data_update(self):
        if "" == self.searchBox.text():
            self.searchButton.setEnabled(False)
        else:
            self.searchButton.setEnabled(True)

    def _search_news(self):
        print("this is a test")
        search_news = SearchNews(self.searchBox.text(), self.sortField.itemText(self.sortField.currentIndex()),"2022-09-28")
        self.results = search_news.search()
        self.model = TableModel(self.results['articles'])
        self.table.setModel(self.model)
        self.table.setRowCount(self.results.size)
        print(self.results['articles'])

    def get_results_model(self):
        return self.model

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()