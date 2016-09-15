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
        self.hL_navigationBtns = QtGui.QHBoxLayout()
        self.hL_navigationBtns.setObjectName(_fromUtf8("hL_navigationBtns"))
        self.pb_first = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_first.sizePolicy().hasHeightForWidth())
        self.pb_first.setSizePolicy(sizePolicy)
        self.pb_first.setSizeIncrement(QtCore.QSize(1, 0))
        self.pb_first.setObjectName(_fromUtf8("pb_first"))
        self.hL_navigationBtns.addWidget(self.pb_first)
        self.pb_prev = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_prev.sizePolicy().hasHeightForWidth())
        self.pb_prev.setSizePolicy(sizePolicy)
        self.pb_prev.setObjectName(_fromUtf8("pb_prev"))
        self.hL_navigationBtns.addWidget(self.pb_prev)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.hL_navigationBtns.addWidget(self.line_2)
        self.pb_next = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_next.sizePolicy().hasHeightForWidth())
        self.pb_next.setSizePolicy(sizePolicy)
        self.pb_next.setObjectName(_fromUtf8("pb_next"))
        self.hL_navigationBtns.addWidget(self.pb_next)
        self.pb_last = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_last.sizePolicy().hasHeightForWidth())
        self.pb_last.setSizePolicy(sizePolicy)
        self.pb_last.setSizeIncrement(QtCore.QSize(1, 0))
        self.pb_last.setObjectName(_fromUtf8("pb_last"))
        self.hL_navigationBtns.addWidget(self.pb_last)
        self.verticalLayout.addLayout(self.hL_navigationBtns)
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
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.pb_download = QtGui.QPushButton(self.centralwidget)
        self.pb_download.setSizeIncrement(QtCore.QSize(1, 0))
        self.pb_download.setObjectName(_fromUtf8("pb_download"))
        self.verticalLayout.addWidget(self.pb_download)
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
        self.action_About_app = QtGui.QAction(MainWindow)
        self.action_About_app.setObjectName(_fromUtf8("action_About_app"))
        self.action_Repo = QtGui.QAction(MainWindow)
        self.action_Repo.setObjectName(_fromUtf8("action_Repo"))
        self.menu_About.addAction(self.action_About_app)
        self.menu_About.addAction(self.action_Repo)
        self.menubar.addAction(self.menu_About.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Order of the stick", None))
        self.pb_first.setText(_translate("MainWindow", "&First", None))
        self.pb_first.setShortcut(_translate("MainWindow", "Up", None))
        self.pb_prev.setText(_translate("MainWindow", "< &Prev", None))
        self.pb_prev.setShortcut(_translate("MainWindow", "Left", None))
        self.pb_next.setText(_translate("MainWindow", "&Next >", None))
        self.pb_next.setShortcut(_translate("MainWindow", "Right", None))
        self.pb_last.setText(_translate("MainWindow", "&Last", None))
        self.pb_last.setShortcut(_translate("MainWindow", "Down", None))
        self.pb_download.setText(_translate("MainWindow", "&Download", None))
        self.menu_About.setTitle(_translate("MainWindow", "&About", None))
        self.action_About_app.setText(_translate("MainWindow", "&About app", None))
        self.action_Repo.setText(_translate("MainWindow", "&Repo", None))

