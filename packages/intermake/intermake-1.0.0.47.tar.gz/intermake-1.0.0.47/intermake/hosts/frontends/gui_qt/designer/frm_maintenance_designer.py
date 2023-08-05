# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/intermake/intermake/hosts/frontends/gui_qt/designer/frm_maintenance_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1025, 891)
        Dialog.setStyleSheet("QDialog\n"
"{\n"
"background: #808080;\n"
"}\n"
"\n"
"QToolButton\n"
"{\n"
"background: #C0C0C0;\n"
"border-radius: 4px;\n"
"margin: 2px;\n"
"padding: 2px;\n"
"}\n"
"\n"
"QToolButton:checked\n"
"{\n"
"background: #E0E0E0;\n"
"}\n"
"\n"
"QTreeWidget\n"
"{\n"
"background: white;\n"
"color: black;\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: white;\n"
"border-radius: 8px;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"background: white;\n"
"color: black;\n"
"border-width: 1px;\n"
"border-color: #00FF00;\n"
"border-radius: 8px;\n"
"}\n"
"\n"
"QTextEdit[style=\"console\"]\n"
"{\n"
"background: black;\n"
"color: white;\n"
"}\n"
"\n"
"QPushButton[style=\"completed\"]\n"
"{\n"
"background: #0080C0;\n"
"color: white;\n"
"padding: 8px;\n"
"border-color: white;\n"
"border-width: 1px;\n"
"border-radius: 8px;\n"
"}\n"
"\n"
"QPushButton[style=\"cancel\"]\n"
"{\n"
"background: #C00000;\n"
"color: white;\n"
"padding: 8px;\n"
"border-color: white;\n"
"border-width: 1px;\n"
"border-radius: 8px;\n"
"}\n"
"\n"
"QFrame[style=\"title\"]\n"
"{\n"
"background: #C0C0C0;\n"
"border-radius: 8px;\n"
"padding: 4px;\n"
"}")
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.FRA_TITLE = QtWidgets.QFrame(Dialog)
        self.FRA_TITLE.setObjectName("FRA_TITLE")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.FRA_TITLE)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.TXT_TITLE_2 = QtWidgets.QLabel(self.FRA_TITLE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TXT_TITLE_2.sizePolicy().hasHeightForWidth())
        self.TXT_TITLE_2.setSizePolicy(sizePolicy)
        self.TXT_TITLE_2.setMaximumSize(QtCore.QSize(24, 24))
        self.TXT_TITLE_2.setText("")
        self.TXT_TITLE_2.setPixmap(QtGui.QPixmap(":/images/resource_files/script.svg"))
        self.TXT_TITLE_2.setScaledContents(True)
        self.TXT_TITLE_2.setObjectName("TXT_TITLE_2")
        self.horizontalLayout_3.addWidget(self.TXT_TITLE_2)
        self.TXT_TITLE = QtWidgets.QLabel(self.FRA_TITLE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TXT_TITLE.sizePolicy().hasHeightForWidth())
        self.TXT_TITLE.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.TXT_TITLE.setFont(font)
        self.TXT_TITLE.setObjectName("TXT_TITLE")
        self.horizontalLayout_3.addWidget(self.TXT_TITLE)
        self.BTN_ESTIMATE = QtWidgets.QToolButton(self.FRA_TITLE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_ESTIMATE.sizePolicy().hasHeightForWidth())
        self.BTN_ESTIMATE.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/resource_files/dropdown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_ESTIMATE.setIcon(icon)
        self.BTN_ESTIMATE.setObjectName("BTN_ESTIMATE")
        self.horizontalLayout_3.addWidget(self.BTN_ESTIMATE)
        self.verticalLayout.addWidget(self.FRA_TITLE)
        self.SPL_MAIN = QtWidgets.QSplitter(Dialog)
        self.SPL_MAIN.setOrientation(QtCore.Qt.Vertical)
        self.SPL_MAIN.setObjectName("SPL_MAIN")
        self.FRA_PROGRESS = QtWidgets.QFrame(self.SPL_MAIN)
        self.FRA_PROGRESS.setObjectName("FRA_PROGRESS")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.FRA_PROGRESS)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.BTN_SHOW_PROGRESS = QtWidgets.QToolButton(self.FRA_PROGRESS)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_SHOW_PROGRESS.sizePolicy().hasHeightForWidth())
        self.BTN_SHOW_PROGRESS.setSizePolicy(sizePolicy)
        self.BTN_SHOW_PROGRESS.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/resource_files/maximise.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SHOW_PROGRESS.setIcon(icon1)
        self.BTN_SHOW_PROGRESS.setCheckable(True)
        self.BTN_SHOW_PROGRESS.setObjectName("BTN_SHOW_PROGRESS")
        self.horizontalLayout.addWidget(self.BTN_SHOW_PROGRESS)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.TVW_LOG = QtWidgets.QTreeWidget(self.FRA_PROGRESS)
        self.TVW_LOG.setObjectName("TVW_LOG")
        self.TVW_LOG.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.TVW_LOG)
        self.FRA_MESSAGES = QtWidgets.QFrame(self.SPL_MAIN)
        self.FRA_MESSAGES.setObjectName("FRA_MESSAGES")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.FRA_MESSAGES)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.BTN_SHOW_OUTPUT = QtWidgets.QToolButton(self.FRA_MESSAGES)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_SHOW_OUTPUT.sizePolicy().hasHeightForWidth())
        self.BTN_SHOW_OUTPUT.setSizePolicy(sizePolicy)
        self.BTN_SHOW_OUTPUT.setText("")
        self.BTN_SHOW_OUTPUT.setIcon(icon1)
        self.BTN_SHOW_OUTPUT.setCheckable(True)
        self.BTN_SHOW_OUTPUT.setObjectName("BTN_SHOW_OUTPUT")
        self.horizontalLayout_4.addWidget(self.BTN_SHOW_OUTPUT)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.TXT_MESSAGES = QtWidgets.QTextEdit(self.FRA_MESSAGES)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.TXT_MESSAGES.setFont(font)
        self.TXT_MESSAGES.setStyleSheet("")
        self.TXT_MESSAGES.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.TXT_MESSAGES.setReadOnly(True)
        self.TXT_MESSAGES.setObjectName("TXT_MESSAGES")
        self.verticalLayout_3.addWidget(self.TXT_MESSAGES)
        self.verticalLayout.addWidget(self.SPL_MAIN)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.BTN_CANCEL = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/resource_files/checkno.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_CANCEL.setIcon(icon2)
        self.BTN_CANCEL.setAutoDefault(False)
        self.BTN_CANCEL.setObjectName("BTN_CANCEL")
        self.horizontalLayout_2.addWidget(self.BTN_CANCEL)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.BTN_CLOSE = QtWidgets.QPushButton(Dialog)
        self.BTN_CLOSE.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/resource_files/checkyes.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_CLOSE.setIcon(icon3)
        self.BTN_CLOSE.setAutoDefault(False)
        self.BTN_CLOSE.setDefault(True)
        self.BTN_CLOSE.setObjectName("BTN_CLOSE")
        self.horizontalLayout_2.addWidget(self.BTN_CLOSE)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.FRA_TITLE.setProperty("style", _translate("Dialog", "title"))
        self.TXT_TITLE.setText(_translate("Dialog", "Text goes here"))
        self.BTN_SHOW_PROGRESS.setToolTip(_translate("Dialog", "Expand view"))
        self.BTN_SHOW_OUTPUT.setToolTip(_translate("Dialog", "Expand view"))
        self.TXT_MESSAGES.setProperty("style", _translate("Dialog", "console"))
        self.BTN_CANCEL.setText(_translate("Dialog", "Cancel"))
        self.BTN_CANCEL.setProperty("style", _translate("Dialog", "cancel"))
        self.BTN_CLOSE.setText(_translate("Dialog", "Close"))
        self.BTN_CLOSE.setProperty("style", _translate("Dialog", "completed"))


