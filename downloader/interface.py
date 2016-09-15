from PyQt4 import QtGui, QtCore
import downloader
from ui import mainwindow, dialog
import os

import logging

log = logging.getLogger('oots-downloader')


class Downloader(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self._isRunning = False
        self.parent = parent

        # signals
        self.download_start = QtCore.SIGNAL('download_start(int)')
        self.new_comic = QtCore.SIGNAL('new_comic_available(QString)')
        self.download_stop = QtCore.SIGNAL('download_stop()')

    def __del__(self):
        self.wait()

    def run(self):
        self._isRunning = True

        last_downloaded, last = downloader.get_range(directory='./comics')

        # handle indexes for strings
        last_downloaded = last_downloaded + 1
        last_available = last + 1

        # notify the start of the download
        # with the total amount of files to download
        comic_to_download = last_available - last_downloaded
        self.emit(self.download_start, comic_to_download)

        log.info('Beginning download... last comic downloaded: %s, latest: %s'
                 ', to download: %s' % (last_downloaded - 1, last_available,
                                        last_available - last_downloaded - 1))

        # while self._isRunning is True and we haven't reached the end of the
        # available comic pages keep downloading and saving the images
        for i in range(last_downloaded, last_available):
            if self._isRunning is False:
                # stop the cycle if the user call for a stop.
                break

            # get the image from the website and save it locally
            img, ext = downloader.get_image(i)
            fileName = 'oots%04d%s' % (i, ext)
            downloader.save_image(img, fileName)

            # notify in the logger
            log.info('New comic available: %s' % fileName)

            # notify that a new file is available to other app components
            self.emit(self.new_comic, fileName)

    def stop(self):
        self._isRunning = False
        self.terminate()
        self.emit(self.download_stop)

        log.info('Download interrupted by the user.')


class Viewer(QtGui.QLabel):
    def __init__(self, img, parent=None):
        super(Viewer, self).__init__(parent)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        try:
            self.pixmap = QtGui.QPixmap(img)
        except:
            log.error('Error in creating the image')

    def paintEvent(self, event):
        """
        Paint and scale comic pixmap correctly.
        """

        try:
            size = self.size()
            painter = QtGui.QPainter(self)
            point = QtCore.QPoint(0, 0)

            pix = self.pixmap.scaled(
                size,
                QtCore.Qt.KeepAspectRatio,
                transformMode=QtCore.Qt.SmoothTransformation)

            point.setX((size.width() - pix.width()) / 2)
            point.setX((size.height() - pix.height()) / 2)

            painter.drawPixmap(point, pix)
        except AttributeError:
            # If no images are present in /comics this event will raise an
            # AttributeError in self.pixmap. catch it and do nothing...
            pass

    def changePage(self, img):
        self.pixmap = QtGui.QPixmap(img)  # change the source for the pixmap
        self.repaint()  # will trigger paintEvent


class Dialog(QtGui.QDialog, dialog.Ui_dialog_downloading):
    """
    QDialog that will handle the downloder functionality.
    """
    def __init__(self, parent=None, downloaderThread=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.downloader = downloaderThread

        self._total = 0
        self._current = 0

        self.setupConnection()

    def setupConnection(self):
        self.pb_abort.clicked.connect(self.abort)

        self.connect(self.downloader,
                     self.downloader.download_start,
                     self.on_download_start)

        self.connect(self.downloader,
                     self.downloader.download_stop,
                     self.on_download_stop)

        self.connect(self.downloader,
                     self.downloader.new_comic,
                     self.on_download_new_comic)

    def hideEvent(self, event):
        """Override the default close event to also stop the downloader. """
        self.stop_downloader()
        event.accept()

    def on_download_start(self, total):
        """
        Called when the downloader starts to download and pass the total pages
        to download.
        Will handle the initial setup for the progress bar.
        """
        self._total = total
        self._current = 0
        self.pb_abort.setEnabled(True)
        # update the values for the progress bar
        self.download_progress.setMaximum(total)
        self.download_progress.setValue(0)

    def on_download_new_comic(self, fileName):
        """
        Called when the downloader has downloaded a new comic. Will handle the
        progress bar update.
        """

        # update the progress bar
        self.download_progress.setValue(self.download_progress.value() + 1)
        self._current += 1

        # compile the label for the dialog
        new_label = '[%s/%s] %s' % (self._current, self._total, fileName)

        self.label_notifier.setText(QtCore.QString(new_label))
        pass

    def on_download_stop(self):
        """
        Called when the download finishes to download.
        """
        self.pb_abort.setEnabled(True)

    def abort(self):
        """
        Callback for the abort button click.
        """
        self.close()

    def start_downloader(self):
        """
        Start downloading new comics if needed and stop when there aren't more
        to download or stopped by the user.
        """
        self.downloader.start()

    def stop_downloader(self):
        """
        Stop downloading.
        """
        self.downloader.stop()


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.filename_regex = downloader._img_filename

        self.downloader = Downloader(self)
        self.dialog = Dialog(self, downloaderThread=self.downloader)

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
        # actions
        self.action_first.activated.connect(self.go_to_first)
        self.action_last.activated.connect(self.go_to_last)
        self.action_next.activated.connect(self.go_to_next)
        self.action_prev.activated.connect(self.go_to_prev)

        # comboBox change
        self.cb_pages.currentIndexChanged.connect(self.change_page)

        # download button
        self.action_download.activated.connect(self.show_download_dialog)

        # Catch signal from downloader
        # TODO: Switch all to signals and move the downloader inside this obj
        self.connect(self.downloader,
                     self.downloader.new_comic,
                     self.on_new_comic_available)

    def generate_list(self):
        """
        Generate the list of the currently available comics and add them to
        the combo box.
        """
        self.cb_pages.clear()
        for fName in os.listdir('./comics/'):
            # for each file add an item with the number of the page as display
            # text and the file path as itemData
            self.add_item_to_list(fName)

        self.go_to_last()

    def add_item_to_list(self, fName):
        """
        Add one item to the combobox list and sort the items.
        """
        self.cb_pages.addItem(self.filename_regex.match(fName).group(1),
                              './comics/%s' % fName)

        self.cb_pages.model().sort(0)

    def go_to_next(self):
        """
        Go to the next page if possible.
        """

        current = self.cb_pages.currentIndex()
        last = self.cb_pages.count() - 1

        if current is not last:
            self.cb_pages.setCurrentIndex(current + 1)
            self.action_prev.setEnabled(True)
            self.action_first.setEnabled(True)
        else:
            self.action_next.setEnabled(False)
            self.action_last.setEnabled(False)

    def go_to_prev(self):
        """
        Go to the previous page if possible.
        """

        current = self.cb_pages.currentIndex()

        if current is not 1:
            self.cb_pages.setCurrentIndex(current - 1)
            self.action_next.setEnabled(True)
            self.action_last.setEnabled(True)
        else:
            self.action_prev.setEnabled(False)
            self.action_first.setEnabled(False)

    def go_to_first(self):
        """
        Go to the first page.
        """

        self.cb_pages.setCurrentIndex(0)
        self.action_prev.setEnabled(False)
        self.action_first.setEnabled(False)
        self.action_next.setEnabled(True)
        self.action_last.setEnabled(True)

    def go_to_last(self):
        """
        Go to the last.
        """

        self.cb_pages.setCurrentIndex(self.cb_pages.count() - 1)
        self.action_next.setEnabled(False)
        self.action_last.setEnabled(False)
        self.action_prev.setEnabled(True)
        self.action_first.setEnabled(True)

    def change_page(self, index):
        """
        Change the viewed comic page.
        Callback for whenever the comboBox change currentIndex.
        """
        filePath = self.cb_pages.itemData(index).toPyObject()

        if filePath is not None:
            log.debug('Loading page"%s"' % filePath)
            pic = QtGui.QPixmap(filePath)
            pic = pic.scaledToHeight(self.frameGeometry().width())

            self.viewer.changePage(filePath)

    def show_download_dialog(self):
        """
        Check for new comics and download if available.
        """
        self.downloader.start()
        self.dialog.show()

    def on_new_comic_available(self, fName):
        """Update the list when new comics are downloaded.
        a string containing the new item is passed but for now is not used
        here. Later we'll add a function to just add new items to the combobox
        instead of regenerating the whole list that will use that string.
        """
        self.add_item_to_list(fName)
