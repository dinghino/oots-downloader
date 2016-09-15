from PyQt4 import QtGui, QtCore
import downloader
from ui import mainwindow
import os
import logging

LOG = logging.getLogger('oots-downloader')


class Viewer(QtGui.QLabel):
    def __init__(self, img, parent=None):
        super(Viewer, self).__init__(parent)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        if img is not None:
            self.pixmap = QtGui.QPixmap(img)

    def paintEvent(self, event):
        """
        Paint and scale comic pixmap correctly.
        """

        if self.pixmap is None:
            return

        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0, 0)

        pix = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio,
                                 transformMode=QtCore.Qt.SmoothTransformation)

        point.setX((size.width() - pix.width()) / 2)
        point.setX((size.height() - pix.height()) / 2)

        painter.drawPixmap(point, pix)

    def changePage(self, img):
        self.pixmap = QtGui.QPixmap(img)  # change the source for the pixmap
        self.repaint()  # will trigger paintEvent


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.createViewer()
        self.setupConnection()

        self.generate_list()

    def _createViewer(self):
        """
        Create an instance of the custom QLabel widget.
        """

        self.viewer = Viewer(None, parent=self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.viewer.sizePolicy().hasHeightForWidth())

        self.viewer.setSizePolicy(sizePolicy)
        # add at the beginning of the the vertical layout
        self.verticalLayout.insertWidget(0, self.viewer)

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
        """
        Go to the next page if possible.
        """

        current = self.cb_pages.currentIndex()
        last = self.cb_pages.count() - 1

        if current is not last:
            self.cb_pages.setCurrentIndex(current + 1)

    def go_to_prev(self):
        """
        Go to the previous page if possible.
        """

        current = self.cb_pages.currentIndex()

        if current is not 0:
            self.cb_pages.setCurrentIndex(current - 1)

    def go_to_first(self):
        """
        Go to the first page.
        """

        self.cb_pages.setCurrentIndex(0)

    def go_to_last(self):
        """
        Go to the last.
        """

        self.cb_pages.setCurrentIndex(self.cb_pages.count() - 1)

    def change_page(self, index):
        """
        Change the viewed comic page.
        Callback for whenever the comboBox change currentIndex.
        """
        filePath = self.cb_pages.itemData(index).toPyObject()

        LOG.info('Loading page"%s"' % filePath)
        pic = QtGui.QPixmap(filePath)
        pic = pic.scaledToHeight(self.frameGeometry().width())

        self.viewer.changePage(filePath)
