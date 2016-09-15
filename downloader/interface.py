from PyQt4 import QtGui, QtCore
import downloader
from ui import mainwindow, dialog
import os
import logging

LOG = logging.getLogger('oots-downloader')


class Viewer(QtGui.QLabel):
    def __init__(self, img, parent=None):
        super(Viewer, self).__init__(parent)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
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


class Dialog(QtGui.QDialog, dialog.Ui_dialog_downloading):
    """
    QDialog that will handle the downloder functionality.
    """
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.setupConnection()
        self.downloading = False

    def setupConnection(self):
        self.pb_pause_restart.clicked.connect(self.pause)
        self.pb_abort.clicked.connect(self.stop)

    def pause(self):
        if self.downloading is True:
            self.pb_pause_restart.setText('&Pause')
            self.stop()

        else:
            self.pb_pause_restart.setText('&Resume')
            self.start()

    def start(self):
        """
        Start downloading new comics if needed and stop when there aren't more
        to download or stopped by the user.
        """
        # FIXME: Since I'm dumb... this need another thread to run into or else
        # everything will freeze..
        # TODO: Create QThread class for the downloader
        self.downloading = True

        last_downloaded, last = downloader.get_range(directory='./comics')

        # rng = range(last_downloaded + 1, last + 1)
        current = last_downloaded + 1
        LOG.info('last downloaded: %s, downloading %s more'
                 % (current, last + 1))

        while self.downloading is True:
            if current == last + 1:
                break

            img, ext = downloader.get_image(current)
            downloader.save_image(img, 'oots%04d%s' % (current, ext))
            current + 1
            LOG.info('going next')

    def stop(self):
        """
        Stop downloading.
        """
        self.downloading = False
        LOG.info('Download interrupted by the user.')


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.downloader = downloader
        self.dialog = Dialog(self)

        # create the image viewer label
        self._createViewer()
        # setup UI connections with the logic
        self.setupConnection()

        # generate the combo box content
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

        # download button
        self.pb_download.clicked.connect(self.show_download_dialog)

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

    def show_download_dialog(self):
        """
        Check for new comics and download if available.
        """
        self.dialog.show()
