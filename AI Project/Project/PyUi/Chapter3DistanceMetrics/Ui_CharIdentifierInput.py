# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\Chapter 3 - Distance Metrics\CharIdentifierInput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CharIdentifierInput(object):
    def setupUi(self, CharIdentifierInput):
        CharIdentifierInput.setObjectName("CharIdentifierInput")
        CharIdentifierInput.resize(717, 437)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CharIdentifierInput.sizePolicy().hasHeightForWidth())
        CharIdentifierInput.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(CharIdentifierInput)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(CharIdentifierInput)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.pushButton_OK = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.horizontalLayout_buttons.addWidget(self.pushButton_OK)
        self.pushButton_set = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_set.setObjectName("pushButton_set")
        self.horizontalLayout_buttons.addWidget(self.pushButton_set)
        self.pushButton_revertSet = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_revertSet.setObjectName("pushButton_revertSet")
        self.horizontalLayout_buttons.addWidget(self.pushButton_revertSet)
        self.pushButton_reset = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout_buttons.addWidget(self.pushButton_reset)
        self.pushButton_save = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_buttons.addWidget(self.pushButton_save)
        self.pushButton_load = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_load.setObjectName("pushButton_load")
        self.horizontalLayout_buttons.addWidget(self.pushButton_load)
        self.pushButton_cancel = QtWidgets.QPushButton(CharIdentifierInput)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_buttons.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_buttons)

        self.retranslateUi(CharIdentifierInput)
        QtCore.QMetaObject.connectSlotsByName(CharIdentifierInput)

    def retranslateUi(self, CharIdentifierInput):
        _translate = QtCore.QCoreApplication.translate
        CharIdentifierInput.setWindowTitle(_translate("CharIdentifierInput", "Dialog"))
        self.pushButton_OK.setText(_translate("CharIdentifierInput", "OK"))
        self.pushButton_set.setText(_translate("CharIdentifierInput", "Set"))
        self.pushButton_revertSet.setText(_translate("CharIdentifierInput", "Revert Set"))
        self.pushButton_reset.setText(_translate("CharIdentifierInput", "Reset"))
        self.pushButton_save.setText(_translate("CharIdentifierInput", "Save"))
        self.pushButton_load.setText(_translate("CharIdentifierInput", "Load"))
        self.pushButton_cancel.setText(_translate("CharIdentifierInput", "Cancel"))
