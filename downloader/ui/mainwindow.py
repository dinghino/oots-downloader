# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(467, 822)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cb_pages = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_pages.sizePolicy().hasHeightForWidth())
        self.cb_pages.setSizePolicy(sizePolicy)
        self.cb_pages.setSizeIncrement(QtCore.QSize(2, 0))
        self.cb_pages.setEditable(False)
        self.cb_pages.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.cb_pages.setObjectName(_fromUtf8("cb_pages"))
        self.verticalLayout.addWidget(self.cb_pages)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 467, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_About = QtGui.QMenu(self.menubar)
        self.menu_About.setObjectName(_fromUtf8("menu_About"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar_main = QtGui.QToolBar(MainWindow)
        self.toolBar_main.setMovable(False)
        self.toolBar_main.setIconSize(QtCore.QSize(32, 32))
        self.toolBar_main.setFloatable(False)
        self.toolBar_main.setObjectName(_fromUtf8("toolBar_main"))
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar_main)
        self.action_About_app = QtGui.QAction(MainWindow)
        self.action_About_app.setObjectName(_fromUtf8("action_About_app"))
        self.action_Repo = QtGui.QAction(MainWindow)
        self.action_Repo.setObjectName(_fromUtf8("action_Repo"))
        self.action_first = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/fA/resources/arrow-circle-left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_first.setIcon(icon)
        self.action_first.setObjectName(_fromUtf8("action_first"))
        self.action_last = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/fA/resources/arrow-circle-right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_last.setIcon(icon1)
        self.action_last.setObjectName(_fromUtf8("action_last"))
        self.action_next = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/fA/resources/arrow-circle-o-right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_next.setIcon(icon2)
        self.action_next.setObjectName(_fromUtf8("action_next"))
        self.action_prev = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/fA/resources/arrow-circle-o-left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_prev.setIcon(icon3)
        self.action_prev.setObjectName(_fromUtf8("action_prev"))
        self.action_download = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/fA/resources/download.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_download.setIcon(icon4)
        self.action_download.setObjectName(_fromUtf8("action_download"))
        self.menu_About.addAction(self.action_About_app)
        self.menu_About.addAction(self.action_Repo)
        self.menubar.addAction(self.menu_About.menuAction())
        self.toolBar_main.addAction(self.action_first)
        self.toolBar_main.addAction(self.action_prev)
        self.toolBar_main.addAction(self.action_next)
        self.toolBar_main.addAction(self.action_last)
        self.toolBar_main.addSeparator()
        self.toolBar_main.addAction(self.action_download)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Order of the stick", None))
        self.menu_About.setTitle(_translate("MainWindow", "&About", None))
        self.toolBar_main.setWindowTitle(_translate("MainWindow", "Navigation toolbar", None))
        self.action_About_app.setText(_translate("MainWindow", "&About app", None))
        self.action_Repo.setText(_translate("MainWindow", "&Repo", None))
        self.action_first.setText(_translate("MainWindow", "&First", None))
        self.action_first.setToolTip(_translate("MainWindow", "Go to the first comic page", None))
        self.action_first.setShortcut(_translate("MainWindow", "Up", None))
        self.action_last.setText(_translate("MainWindow", "&Last", None))
        self.action_last.setToolTip(_translate("MainWindow", "Go to the last downloaded page", None))
        self.action_last.setShortcut(_translate("MainWindow", "Down", None))
        self.action_next.setText(_translate("MainWindow", "&Next", None))
        self.action_next.setToolTip(_translate("MainWindow", "Go to the next page", None))
        self.action_next.setShortcut(_translate("MainWindow", "Right", None))
        self.action_prev.setText(_translate("MainWindow", "&Previous", None))
        self.action_prev.setToolTip(_translate("MainWindow", "Go to the previous page", None))
        self.action_prev.setShortcut(_translate("MainWindow", "Left", None))
        self.action_download.setText(_translate("MainWindow", "&Download", None))
        self.action_download.setToolTip(_translate("MainWindow", "Download new pages if available", None))

import oots_icons_rc
