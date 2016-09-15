# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
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

class Ui_dialog_downloading(object):
    def setupUi(self, dialog_downloading):
        dialog_downloading.setObjectName(_fromUtf8("dialog_downloading"))
        dialog_downloading.resize(394, 119)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_downloading.sizePolicy().hasHeightForWidth())
        dialog_downloading.setSizePolicy(sizePolicy)
        dialog_downloading.setMinimumSize(QtCore.QSize(394, 119))
        dialog_downloading.setMaximumSize(QtCore.QSize(394, 119))
        self.verticalLayout = QtGui.QVBoxLayout(dialog_downloading)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_notifier = QtGui.QLabel(dialog_downloading)
        self.label_notifier.setObjectName(_fromUtf8("label_notifier"))
        self.verticalLayout.addWidget(self.label_notifier)
        self.download_progress = QtGui.QProgressBar(dialog_downloading)
        self.download_progress.setMaximum(100)
        self.download_progress.setProperty("value", 0)
        self.download_progress.setObjectName(_fromUtf8("download_progress"))
        self.verticalLayout.addWidget(self.download_progress)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 8, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pb_pause_restart = QtGui.QPushButton(dialog_downloading)
        self.pb_pause_restart.setObjectName(_fromUtf8("pb_pause_restart"))
        self.horizontalLayout.addWidget(self.pb_pause_restart)
        self.pb_abort = QtGui.QPushButton(dialog_downloading)
        self.pb_abort.setObjectName(_fromUtf8("pb_abort"))
        self.horizontalLayout.addWidget(self.pb_abort)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dialog_downloading)
        QtCore.QMetaObject.connectSlotsByName(dialog_downloading)

    def retranslateUi(self, dialog_downloading):
        dialog_downloading.setWindowTitle(_translate("dialog_downloading", "Downloading new comics...", None))
        self.label_notifier.setText(_translate("dialog_downloading", "notifier", None))
        self.pb_pause_restart.setText(_translate("dialog_downloading", "&Pause", None))
        self.pb_abort.setText(_translate("dialog_downloading", "&Abort", None))

