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
        self.download_finish = QtCore.SIGNAL('download_finish()')

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
                 ', to download: %s' % (last_downloaded, last_available,
                                        range(last_downloaded, last_available)))

        # while self._isRunning is True and we haven't reached the end of the
        # available comic pages keep downloading and saving the images
        for i in range(last_downloaded, last_available):
            if self._isRunning is False:
                # stop the cycle if the user call for a stop.
                break

            if len(range(last_downloaded, last_available)) == 0:
                break

            # get the image from the website and save it locally
            img, ext = downloader.get_image(i)
            fileName = 'oots%04d%s' % (i, ext)
            downloader.save_image(img, fileName)

            # notify in the logger
            log.info('New comic available: %s' % fileName)

            # notify that a new file is available to other app components
            self.emit(self.new_comic, fileName)

        self._isRunning = False
        self.emit(self.download_finish)

    def stop(self):
        if self._isRunning:
            log.info('Download interrupted')
            self._isRunning = False
            self.terminate()
            self.emit(self.download_stop)

        log.info('Download thread closed.')


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

        self.setup_connection()

    def setup_connection(self):
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

        self.connect(self.downloader,
                     self.downloader.download_finish,
                     self.on_download_finish)

    def hideEvent(self, event):
        """Override the default close event to also stop the downloader. """
        self.stop_downloader()
        event.accept()

    def reset_dialog_content(self, total):
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
        self.label_notifier.setText('Comics up to date...')

    def on_download_start(self, total):
        self.reset_dialog_content(total)

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
        self.pb_abort.setText('&Close')
        self.close()

    def on_download_finish(self):
        self.reset_dialog_content(0)
        self.close()

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

        self.image_scrollArea.setAlignment(QtCore.Qt.AlignHCenter)

        # wether the first or last image are shown. Used to update the UI
        # elements
        self._isLastShowing = True
        self._isFirstShowing = True

        # scale factor for the image
        self.scaleFactor = 1.0

        # regex for filename of the comic pages
        self.filename_regex = downloader._img_filename

        # instance of the downloader QThread object
        self.downloader = Downloader(self)
        # downloader dialog
        self.dialog = Dialog(self, downloaderThread=self.downloader)

        # create the image viewer label
        self._createViewer()
        # setup UI connections with the logic
        self.setup_connection()

        # generate the combo box content
        self.generate_list()

    def _createViewer(self):
        """
        Create an instance of the custom QLabel widget.
        """

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter)

        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                      QtGui.QSizePolicy.Ignored)
        # self.imageLabel.setScaledContents(True)

        self.image_scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.image_scrollArea.setWidget(self.imageLabel)

    def setup_connection(self):
        """
        Setup connection for the UI elements.
        """
        # navigation
        self.action_first.triggered.connect(self.go_to_first)
        self.action_last.triggered.connect(self.go_to_last)
        self.action_next.triggered.connect(self.go_to_next)
        self.action_prev.triggered.connect(self.go_to_prev)

        # image zoom
        self.action_zoom_in.triggered.connect(self.image_zoom_in)
        self.action_zoom_out.triggered.connect(self.image_zoom_out)

        # comboBox change
        self.cb_pages.currentIndexChanged.connect(self.change_page)

        # download button
        self.action_download.triggered.connect(self.show_download_dialog)

        # Catch signal from downloader
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

        current = self.cb_pages.currentIndex() + 1
        last = self.cb_pages.count()

        if current is not last:
            self.cb_pages.setCurrentIndex(current)

        self._update_nav_buttons()

    def go_to_prev(self):
        """
        Go to the previous page if possible.
        """

        current = self.cb_pages.currentIndex()

        if current is not 0:
            self.cb_pages.setCurrentIndex(current - 1)

        self._update_nav_buttons()

    def go_to_first(self):
        """
        Go to the first page.
        """

        self.cb_pages.setCurrentIndex(0)
        self._update_nav_buttons()

    def go_to_last(self):
        """
        Go to the last.
        """

        self.cb_pages.setCurrentIndex(self.cb_pages.count() - 1)
        self._update_nav_buttons()

    def image_zoom_in(self):
        """
        Ask the image to zoom in.
        """
        self.scaleImage(1.25)

    def image_zoom_out(self):
        """
        Ask the image to zoom in.
        """
        self.scaleImage(0.8)

    def scaleImage(self, factor):
        self.scaleFactor *= factor

        self.imageLabel.resize(
            self.scaleFactor * self.imageLabel.pixmap().size())

    def _update_nav_buttons(self):
        """
        Update the navigation elements depending on what images is currently
        shown.
        """

        # evaluate current page and last page counts
        current = self.cb_pages.currentIndex() + 1
        last = self.cb_pages.count()

        # update the view status
        self._isLastShowing = current == last
        self._isFirstShowing = current == 1

        # update the ui elements
        self.action_next.setEnabled(not self._isLastShowing)
        self.action_last.setEnabled(not self._isLastShowing)

        self.action_prev.setEnabled(not self._isFirstShowing)
        self.action_first.setEnabled(not self._isFirstShowing)

    def change_page(self, index):
        """
        Change the viewed comic page.
        Callback for whenever the comboBox change currentIndex.
        """
        filePath = self.cb_pages.itemData(index).toPyObject()

        if filePath is not None:
            log.debug('Loading page"%s"' % filePath)

            self.image = QtGui.QImage(filePath)

            # set the min size of the image relative to the wrapper
            width, height = self.adjust_page_size()
            self.imageLabel.setMinimumSize(QtCore.QSize(width, height))
            self.imageLabel.setMaximumSize(
                QtCore.QSize(self.image.width(), self.image.height()))

            self.imageLabel.setScaledContents(True)

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
            self.imageLabel.adjustSize()
            self.scaleFactor = 1.0

        self.adjust_scrollbars(self.image_scrollArea.verticalScrollBar(), 1)

    def adjust_page_size(self):
        """
        Adjust the page image size into the scroll area wrapper, keeping the
        correct aspect ratio and return the new width and height values.
        Setting the sizes on the imageLabel should cause the image to be as
        large as the widget and the length to be proportional and scrollable if
        needed.

        :returns: (width, heigth)
        """

        image = self.image
        wrapperWidth = self.image_scrollArea.size().width()

        imageWidth = float(image.width()) * self.scaleFactor
        imageHeight = float(image.height()) * self.scaleFactor

        newHeight = wrapperWidth * float(imageHeight / imageWidth)

        newHeight = newHeight if newHeight < imageHeight else imageHeight
        newWidth = wrapperWidth if wrapperWidth < imageWidth else imageWidth

        return (newWidth, newHeight)

    def adjust_scrollbars(self, scrollbar, factor):
        scrollbar.setValue(int(factor * scrollbar.value()
                               + ((factor - 1) * scrollbar.pageStep() / 2)))

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

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        self.adjust_page_size()

if __name__ == '__main__':
    from PyQt4.QtGui import QApplication
    import sys

    def main():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

    main()
