#!/usr/bin/env python
# encoding: utf-8
import sys
from PyQt4.QtGui import QApplication
from downloader import downloader, interface


def main():
    app = QApplication(sys.argv)
    window = interface.MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
