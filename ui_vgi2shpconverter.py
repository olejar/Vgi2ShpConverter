# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Documents and Settings\Olejar\.qgis2\python\plugins\Vgi2ShpConverter\ui_vgi2shpconverter.ui'
#
# Created: Fri Jun 20 13:58:41 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Vgi2ShpConverter(object):
    def setupUi(self, Vgi2ShpConverter):
        Vgi2ShpConverter.setObjectName(_fromUtf8("Vgi2ShpConverter"))
        Vgi2ShpConverter.resize(250, 221)
        self.pushButton = QtGui.QPushButton(Vgi2ShpConverter)
        self.pushButton.setGeometry(QtCore.QRect(5, 190, 238, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(Vgi2ShpConverter)
        self.label.setGeometry(QtCore.QRect(0, 0, 248, 184))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/vgi2shpconverter/vgi2shp_96.bmp")))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Vgi2ShpConverter)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("pressed()")), Vgi2ShpConverter.accept)
        QtCore.QMetaObject.connectSlotsByName(Vgi2ShpConverter)

    def retranslateUi(self, Vgi2ShpConverter):
        Vgi2ShpConverter.setWindowTitle(_translate("Vgi2ShpConverter", "Vgi2Shp", None))
        self.pushButton.setText(_translate("Vgi2ShpConverter", "Prevod súborov VGI formátu do SHP formátu", None))

import resources_rc
