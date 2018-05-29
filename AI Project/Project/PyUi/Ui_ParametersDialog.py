# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\ParametersDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ParametersDialog(object):
    def setupUi(self, ParametersDialog):
        ParametersDialog.setObjectName("ParametersDialog")
        ParametersDialog.resize(700, 919)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParametersDialog.sizePolicy().hasHeightForWidth())
        ParametersDialog.setSizePolicy(sizePolicy)
        ParametersDialog.setMinimumSize(QtCore.QSize(700, 0))
        ParametersDialog.setMaximumSize(QtCore.QSize(700, 1500))
        self.verticalLayout = QtWidgets.QVBoxLayout(ParametersDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ParametersDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.parametersWidget_dialog = ParametersWidget(ParametersDialog)
        self.parametersWidget_dialog.setObjectName("parametersWidget_dialog")
        self.verticalLayout.addWidget(self.parametersWidget_dialog)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.parametersWidget_train = ParametersWidget(ParametersDialog)
        self.parametersWidget_train.setObjectName("parametersWidget_train")
        self.verticalLayout.addWidget(self.parametersWidget_train)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.ParametersWidget_algorithm = ParametersWidget(ParametersDialog)
        self.ParametersWidget_algorithm.setObjectName("ParametersWidget_algorithm")
        self.verticalLayout.addWidget(self.ParametersWidget_algorithm)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_quit = QtWidgets.QPushButton(ParametersDialog)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.horizontalLayout.addWidget(self.pushButton_quit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_exit = QtWidgets.QPushButton(ParametersDialog)
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.horizontalLayout.addWidget(self.pushButton_exit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ParametersDialog)
        self.pushButton_quit.clicked.connect(ParametersDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ParametersDialog)

    def retranslateUi(self, ParametersDialog):
        _translate = QtCore.QCoreApplication.translate
        ParametersDialog.setWindowTitle(_translate("ParametersDialog", "Dialog"))
        self.label.setText(_translate("ParametersDialog", "TextLabel"))
        self.parametersWidget_dialog.setToolTip(_translate("ParametersDialog", "The current time"))
        self.parametersWidget_dialog.setWhatsThis(_translate("ParametersDialog", "The analog clock widget displays the current time."))
        self.parametersWidget_train.setToolTip(_translate("ParametersDialog", "The current time"))
        self.parametersWidget_train.setWhatsThis(_translate("ParametersDialog", "The analog clock widget displays the current time."))
        self.ParametersWidget_algorithm.setToolTip(_translate("ParametersDialog", "The current time"))
        self.ParametersWidget_algorithm.setWhatsThis(_translate("ParametersDialog", "The analog clock widget displays the current time."))
        self.pushButton_quit.setText(_translate("ParametersDialog", "Quit"))
        self.pushButton_exit.setText(_translate("ParametersDialog", "Exit"))

from ParametersWidget import ParametersWidget
