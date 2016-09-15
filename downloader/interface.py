from PyQt4 import QtGui, QtCore
import downloader
from ui import mainwindow, dialog
import os
import logging

LOG = logging.getLogger('oots-downloader')


class Downloader(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)
        self._isRunning = False
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        self._isRunning = True

        last_downloaded, last = downloader.get_range(directory='./comics')

        # last downloaded file
        current = last_downloaded + 1

        LOG.info('last downloaded: %s, downloading %s more'
                 % (current, (last + 1) - current))

        # notify the start of the download
        # with the total amount of files to download
        comic_to_download = (last + 1) - (last_downloaded + 1)
        self.emit(QtCore.SIGNAL('download_start'), comic_to_download)

        # while self._isRunning is True and we haven't reached the end of the
        # available comic pages keep downloading and saving the images
        for i in range(last_downloaded + 1, last + 1):
            if self._isRunning is False:
                break

            img, ext = downloader.get_image(i)
            downloader.save_image(img, 'oots%04d%s' % (i, ext))

            # notify that a new file is available
            self.emit(QtCore.SIGNAL('new_comic'))

    def stop(self):
        self._isRunning = False
        self.terminate()
        self.emit(QtCore.SIGNAL('download_stop'))

        LOG.info('Download interrupted by the user.')


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
        self.thread = Downloader(self)
        self.downloading = False

    def setupConnection(self):
        self.pb_pause_restart.clicked.connect(self.pause)
        self.pb_abort.clicked.connect(self.stop)

        # self.connect(self.thread,
        #              QtCore.SIGNAL('download_start'),
        #              self.on_download_start)
        #
        # self.connect(self.thread,
        #              QtCore.SIGNAL('new_comic'),
        #              self.on_download_new_comic)
        #
        # self.connect(self.thread,
        #              QtCore.SIGNAL('download_stop'),
        #              self.on_download_stop)

    # @QtCore.pyqtSlot(int)
    def on_download_start(self, total):
        """
        Called when the downloader starts to download and pass the total pages
        to download.
        Will handle the initial setup for the progress bar.
        """
        print total
        self.change_btn_label('&Pause')

        # update the values for the progress bar
        self.download_progress.setMaximum(total)
        self.download_progress.setValue(0)

    # @QtCore.pyqtSlot()
    def on_download_new_comic(self):
        """
        Called when the downloader has downloaded a new comic. Will handle the
        progress bar update.
        """

        # update the progress bar
        self.download_progress.setValue(self.download_progress.value() + 1)
        # TODO: catch signal in MainWindow to update the list
        pass

    # @QtCore.pyqtSlot()
    def on_download_stop(self):
        """
        Called when the download finishes to download.
        """
        self.change_btn_label('&Resume')
        pass

    def pause(self):
        if self.thread._isRunning is True:
            self.stop()
        else:
            self.start()

    def change_btn_label(self, string):
        self.pb_pause_restart.setText(string)

    def start(self):
        """
        Start downloading new comics if needed and stop when there aren't more
        to download or stopped by the user.
        """
        self.thread.start()

    def stop(self):
        """
        Stop downloading.
        """
        self.thread.stop()


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
