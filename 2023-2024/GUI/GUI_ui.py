# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLCDNumber, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTextBrowser, QWidget)

class Ui_TMUHyperloopGUI(object):
    def setupUi(self, TMUHyperloopGUI):
        if not TMUHyperloopGUI.objectName():
            TMUHyperloopGUI.setObjectName(u"TMUHyperloopGUI")
        TMUHyperloopGUI.resize(800, 600)
        self.centralwidget = QWidget(TMUHyperloopGUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lcdNumber = QLCDNumber(self.centralwidget)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(50, 50, 64, 23))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 30, 47, 13))
        self.lcdNumber_2 = QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setObjectName(u"lcdNumber_2")
        self.lcdNumber_2.setGeometry(QRect(130, 50, 64, 23))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(140, 30, 47, 13))
        self.lcdNumber_3 = QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setObjectName(u"lcdNumber_3")
        self.lcdNumber_3.setGeometry(QRect(130, 80, 64, 23))
        self.lcdNumber_4 = QLCDNumber(self.centralwidget)
        self.lcdNumber_4.setObjectName(u"lcdNumber_4")
        self.lcdNumber_4.setGeometry(QRect(130, 110, 64, 23))
        self.lcdNumber_5 = QLCDNumber(self.centralwidget)
        self.lcdNumber_5.setObjectName(u"lcdNumber_5")
        self.lcdNumber_5.setGeometry(QRect(220, 50, 64, 23))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(230, 30, 47, 13))
        self.lcdNumber_6 = QLCDNumber(self.centralwidget)
        self.lcdNumber_6.setObjectName(u"lcdNumber_6")
        self.lcdNumber_6.setGeometry(QRect(220, 80, 64, 23))
        self.lcdNumber_7 = QLCDNumber(self.centralwidget)
        self.lcdNumber_7.setObjectName(u"lcdNumber_7")
        self.lcdNumber_7.setGeometry(QRect(220, 110, 64, 23))
        self.lcdNumber_8 = QLCDNumber(self.centralwidget)
        self.lcdNumber_8.setObjectName(u"lcdNumber_8")
        self.lcdNumber_8.setGeometry(QRect(310, 80, 64, 23))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(310, 30, 61, 16))
        self.lcdNumber_9 = QLCDNumber(self.centralwidget)
        self.lcdNumber_9.setObjectName(u"lcdNumber_9")
        self.lcdNumber_9.setGeometry(QRect(310, 50, 64, 23))
        self.lcdNumber_10 = QLCDNumber(self.centralwidget)
        self.lcdNumber_10.setObjectName(u"lcdNumber_10")
        self.lcdNumber_10.setGeometry(QRect(310, 110, 64, 23))
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(470, 40, 256, 192))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(560, 10, 71, 16))
        TMUHyperloopGUI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(TMUHyperloopGUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuTMU_Hyperloop_GUI = QMenu(self.menubar)
        self.menuTMU_Hyperloop_GUI.setObjectName(u"menuTMU_Hyperloop_GUI")
        TMUHyperloopGUI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(TMUHyperloopGUI)
        self.statusbar.setObjectName(u"statusbar")
        TMUHyperloopGUI.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuTMU_Hyperloop_GUI.menuAction())

        self.retranslateUi(TMUHyperloopGUI)

        QMetaObject.connectSlotsByName(TMUHyperloopGUI)
    # setupUi

    def retranslateUi(self, TMUHyperloopGUI):
        TMUHyperloopGUI.setWindowTitle(QCoreApplication.translate("TMUHyperloopGUI", u"TMU Hyperloop GUI", None))
        self.label.setText(QCoreApplication.translate("TMUHyperloopGUI", u"Velocity", None))
        self.label_2.setText(QCoreApplication.translate("TMUHyperloopGUI", u"Voltage", None))
        self.label_3.setText(QCoreApplication.translate("TMUHyperloopGUI", u"Current", None))
        self.label_4.setText(QCoreApplication.translate("TMUHyperloopGUI", u"Temperature", None))
        self.textBrowser.setHtml(QCoreApplication.translate("TMUHyperloopGUI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("TMUHyperloopGUI", u"Current State", None))
        self.menuTMU_Hyperloop_GUI.setTitle(QCoreApplication.translate("TMUHyperloopGUI", u"TMU Hyperloop GUI", None))
    # retranslateUi

