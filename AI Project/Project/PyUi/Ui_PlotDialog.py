# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\PlotDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlotDialog(object):
    def setupUi(self, PlotDialog):
        PlotDialog.setObjectName("PlotDialog")
        PlotDialog.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PlotDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.myQtPlotContainer = MyQtPlotContainer(PlotDialog)
        self.myQtPlotContainer.setObjectName("myQtPlotContainer")
        self.horizontalLayout.addWidget(self.myQtPlotContainer)
        self.buttonBox = QtWidgets.QDialogButtonBox(PlotDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PlotDialog)
        self.buttonBox.accepted.connect(PlotDialog.accept)
        self.buttonBox.rejected.connect(PlotDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PlotDialog)

    def retranslateUi(self, PlotDialog):
        _translate = QtCore.QCoreApplication.translate
        PlotDialog.setWindowTitle(_translate("PlotDialog", "Dialog"))
        self.myQtPlotContainer.setToolTip(_translate("PlotDialog", "The current time"))
        self.myQtPlotContainer.setWhatsThis(_translate("PlotDialog", "The analog clock widget displays the current time."))

from MyQtPlotContainer import MyQtPlotContainer
