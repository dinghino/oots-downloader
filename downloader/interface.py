from PyQt4 import QtCore, QtGui
import downloader
from ui import mainwindow
import os
import logging

LOG = logging.getLogger('oots-downloader')

class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupConnection()

        self.generate_list()

    def setupConnection(self):
        """
        Setup connection for the UI elements.
        """
        # navigation buttons
        self.pb_first.clicked.connect(self.go_to_first)
        self.pb_last.clicked.connect(self.go_to_last)
        self.pb_next.clicked.connect(self.go_to_next)
        self.pb_prev.clicked.connect(self.go_to_prev)

        # comboBox change
        self.cb_pages.currentIndexChanged.connect(self.change_page)

    def generate_list(self):
        """
        Generate the list of the currently available comics and add them to
        the combo box.
        """

        regex = downloader._img_filename

        for fName in os.listdir('./comics/'):
            # for each file add an item with the number of the page as display
            # text and the file path as itemData
            self.cb_pages.addItem(regex.match(fName).group(1),
                                  './comics/%s' % fName)

        self.cb_pages.model().sort(0)
        self.go_to_last()

    def go_to_next(self):
        current = self.cb_pages.currentIndex()
        last = self.cb_pages.count() - 1

        if current is not last:
            self.cb_pages.setCurrentIndex(current + 1)

    def go_to_prev(self):
        current = self.cb_pages.currentIndex()

        if current is not 0:
            self.cb_pages.setCurrentIndex(current - 1)

    def go_to_first(self):
        self.cb_pages.setCurrentIndex(0)

    def go_to_last(self):
        self.cb_pages.setCurrentIndex(self.cb_pages.count() - 1)

    def change_page(self, index):
        filePath = self.cb_pages.itemData(index).toPyObject()

        LOG.info('Loading page"%s"' % filePath)
