# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/intermake/intermake/hosts/frontends/gui_qt/designer/frm_arguments_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1119, 989)
        Dialog.setStyleSheet("/**\n"
"    This is the default style-sheet used by all Intermake dialogues.\n"
"    It can be retrieved via `intermake_gui.default_style_sheet()` function.\n"
"    \n"
"    Attach a string property named \"theme\" to widgets to use the unique styles listed below:\n"
"    \n"
"    WIDGET        | THEME               APPEARANCE (GUIDE)              USAGE (GUIDE)\n"
"    --------------+-------------\n"
"    QLabel        | heading               border, big, bold               section titles \n"
"    QLabel        | subheading               border, big, bold               section titles \n"
"    QTextEdit     | console             monospaced, black background    code, console output\n"
"    QPushButton   | completed           \n"
"    QPushButton   | cancel              red                             abort button\n"
"    QFrame        | header               border                          section titles\n"
"    QToolButton   | listbutton          condensed                       buttons in lists\n"
"    QLabel        | helpbox             tooltip background              help labels\n"
"    QLabel        | icon                background suitable for image   label showing an icon\n"
"*/\n"
"\n"
"QDialog\n"
"{\n"
"    background : #EEEEEE;\n"
"}\n"
"\n"
"QFrame[style=\"heading\"]\n"
"{\n"
"    background    : #C0C0C0;\n"
"    border-radius : 8px;\n"
"    padding       : 4px;\n"
"}\n"
"\n"
"QLabel[style=\"heading\"]\n"
"{\n"
"    background    : #C0C0C0;\n"
"    border-radius : 4px;\n"
"    margin        : 2px;\n"
"    padding       : 2px;\n"
"    color         : black;\n"
"    font-weight   : bold;\n"
"}\n"
"\n"
"QLabel[style=\"subheading\"]\n"
"{\n"
"    background    : #FFFFFF;\n"
"    border-radius : 4px;\n"
"    margin        : 2px;\n"
"    padding       : 2px;\n"
"    color         : black;\n"
"    font-weight   : bold;\n"
"}\n"
"\n"
"\n"
"QLabel[style=\"helpbox\"]\n"
"{\n"
"    background    : #FFFFD0;\n"
"}\n"
"\n"
"QToolButton\n"
"{\n"
"    background    : #0080C0;\n"
"    border-radius : 4px;\n"
"    margin        : 2px;\n"
"    padding       : 2px;\n"
"    color         : white;\n"
"    font-weight   : bold;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    background    : #0080C0;\n"
"    color         : white;\n"
"    font-weight   : bold;\n"
"    padding       : 4px;\n"
"    border-color  : white;\n"
"    border-width  : 1px;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QTreeWidget\n"
"{\n"
"    background    : white;\n"
"    color         : black;\n"
"    border-style  : solid;\n"
"    border-width  : 1px;\n"
"    border-color  : white;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background    : white;\n"
"    color         : black;\n"
"    border-width  : 1px;\n"
"    border-color  : #00FF00;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QTextEdit[style=\"console\"]\n"
"{\n"
"    background : black;\n"
"    color      : white;\n"
"}\n"
"\n"
"QPushButton[style=\"completed\"]\n"
"{\n"
"    background    : #00C080;\n"
"    color         : white;\n"
"    padding       : 8px;\n"
"    border-color  : white;\n"
"    border-width  : 1px;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QPushButton[style=\"cancel\"]\n"
"{\n"
"    background    : #C00000;\n"
"    color         : white;\n"
"    padding       : 8px;\n"
"    border-color  : white;\n"
"    border-width  : 1px;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QMenuBar\n"
"{\n"
"    background-color : #0070B0;\n"
"    color            : white;\n"
"    border-width     : 1px;\n"
"    border-style     : transparent;\n"
"    border-color     : black;\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background-color : #0080C0;\n"
"    color            : white;\n"
"    border-width     : 1px;\n"
"    border-style     : solid;\n"
"    border-color     : transparent;\n"
"    border-radius    : 8px;\n"
"    padding          : 2px;\n"
"    margin           : 2px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    background-color : #0070B0;\n"
"    color            : white;\n"
"    border-width     : 1px;\n"
"    border-style     : transparent;\n"
"    border-color     : black;\n"
"    border-radius    : 8px;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    background-color : #0080C0;\n"
"    color            : white;\n"
"    border-width     : 1px;\n"
"    border-style     : transparent;\n"
"    border-color     : black;\n"
"    border-radius    : 8px;\n"
"    padding          : 8px;\n"
"    padding-left     : 32px;\n"
"    margin           : 1px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    background-color : #00C080;\n"
"}\n"
"\n"
"QToolButton[style=\"listbutton\"]\n"
"{\n"
"background: #40C0FF;\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-color: transparent;\n"
"}\n"
"\n"
"QToolButton[style=\"listbutton\"]::hover\n"
"{\n"
"background: #B0D5E8;\n"
"border-color: blue;\n"
"}\n"
"\n"
"QToolButton[style=\"listbutton\"]::pressed\n"
"{\n"
"background: #0040C0;\n"
"border-style: inset;\n"
"}\n"
"\n"
"QPushButton[checkable=\"true\"]:hover,QToolButton[checkable=\"true\"]:hover\n"
"{\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"background: #0060C0\n"
"}\n"
"\n"
"QPushButton[checkable=\"true\"]:hover:checked,QToolButton[checkable=\"true\"]:hover:checked\n"
"{\n"
"background: #00C040\n"
"}\n"
"\n"
"QPushButton:checked,QToolButton:checked\n"
"{\n"
"    background : #00C000;\n"
"}\n"
"\n"
"QScrollBar\n"
"{\n"
"background: #E0E0E0;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"    width: 8px;\n"
"}\n"
"\n"
"QScrollBar:horizontal\n"
"{\n"
"    height: 8px;\n"
"}\n"
"\n"
"QScrollBar::handle\n"
"{\n"
"background: #90C0D0;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"min-width: 8px;\n"
"margin: 8px 0px 8px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"min-height: 8px;\n"
"margin: 0px 8px 0px 8px;\n"
"}\n"
"\n"
"QScrollBar:up-arrow, QScrollBar::down-arrow, QScrollBar::left-arrow, QScrollBar::right-arrow\n"
"{\n"
"border-size: 1px;\n"
"border-radius: 4px;\n"
"width: 8px;\n"
"height: 8px;\n"
"background: #0080C0;\n"
"}\n"
"\n"
"QScrollBar::sub-line, QScrollBar::add-line\n"
"{\n"
"background: #C0C0C0;\n"
"}\n"
"\n"
"QRadioButton::indicator,QCheckBox::indicator\n"
"{\n"
"background: #0080C0;\n"
"width: 16px;\n"
"height: 16px;\n"
"}\n"
"\n"
"QCheckBox::indicator\n"
"{\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"border-radius: 8px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked,QCheckBox::indicator:checked\n"
"{\n"
"background: #00C080;\n"
"image: url(:/check_yes.svg);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked,QCheckBox::indicator:unchecked\n"
"{\n"
"image: none;\n"
"}\n"
"\n"
"QRadioButton::indicator:indeterminate,QCheckBox::indicator:indeterminate\n"
"{\n"
"image: url(:/check_indeterminate.svg);\n"
"}\n"
"\n"
"QLabel[style=\"icon\"]\n"
"{\n"
"    background: #808080;\n"
"    border-radius: 8px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LBL_PLUGIN_ICON = QtWidgets.QLabel(Dialog)
        self.LBL_PLUGIN_ICON.setMaximumSize(QtCore.QSize(40, 40))
        self.LBL_PLUGIN_ICON.setText("")
        self.LBL_PLUGIN_ICON.setPixmap(QtGui.QPixmap(":/app.svg"))
        self.LBL_PLUGIN_ICON.setScaledContents(True)
        self.LBL_PLUGIN_ICON.setObjectName("LBL_PLUGIN_ICON")
        self.horizontalLayout_2.addWidget(self.LBL_PLUGIN_ICON)
        self.LBL_PLUGIN_NAME = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LBL_PLUGIN_NAME.sizePolicy().hasHeightForWidth())
        self.LBL_PLUGIN_NAME.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.LBL_PLUGIN_NAME.setFont(font)
        self.LBL_PLUGIN_NAME.setObjectName("LBL_PLUGIN_NAME")
        self.horizontalLayout_2.addWidget(self.LBL_PLUGIN_NAME)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.GRID_ARGS_OWNER = QtWidgets.QWidget()
        self.GRID_ARGS_OWNER.setGeometry(QtCore.QRect(0, 0, 1095, 872))
        self.GRID_ARGS_OWNER.setObjectName("GRID_ARGS_OWNER")
        self.GRID_ARGS = QtWidgets.QGridLayout(self.GRID_ARGS_OWNER)
        self.GRID_ARGS.setContentsMargins(0, 0, 0, 0)
        self.GRID_ARGS.setObjectName("GRID_ARGS")
        self.scrollArea.setWidget(self.GRID_ARGS_OWNER)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CHK_HELP = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CHK_HELP.sizePolicy().hasHeightForWidth())
        self.CHK_HELP.setSizePolicy(sizePolicy)
        self.CHK_HELP.setCheckable(True)
        self.CHK_HELP.setObjectName("CHK_HELP")
        self.horizontalLayout.addWidget(self.CHK_HELP)
        self.CHK_DONT_ASK_AGAIN = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CHK_DONT_ASK_AGAIN.sizePolicy().hasHeightForWidth())
        self.CHK_DONT_ASK_AGAIN.setSizePolicy(sizePolicy)
        self.CHK_DONT_ASK_AGAIN.setCheckable(True)
        self.CHK_DONT_ASK_AGAIN.setObjectName("CHK_DONT_ASK_AGAIN")
        self.horizontalLayout.addWidget(self.CHK_DONT_ASK_AGAIN)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/resource_files/app.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.LBL_PLUGIN_ICON.setProperty("style", _translate("Dialog", "icon"))
        self.LBL_PLUGIN_NAME.setText(_translate("Dialog", "TextLabel"))
        self.CHK_HELP.setText(_translate("Dialog", "Help"))
        self.CHK_DONT_ASK_AGAIN.setText(_translate("Dialog", "Don\'t ask again"))
        self.pushButton.setText(_translate("Dialog", "Execute"))


