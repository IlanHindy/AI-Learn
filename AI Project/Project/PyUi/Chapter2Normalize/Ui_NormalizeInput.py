# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\Chapter 2 - Normalize\NormalizeInput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from MyQtEnumComboBox import MyQtEnumComboBox


class Ui_NormalizeInput(object):

    def setupUi(self, NormalizeInput):
        NormalizeInput.setObjectName("NormalizeInput")
        NormalizeInput.resize(192, 274)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NormalizeInput.sizePolicy().hasHeightForWidth())
        NormalizeInput.setSizePolicy(sizePolicy)
        self.MyQtEnumComboBox_fieldsTypes = MyQtEnumComboBox(NormalizeInput)
        self.MyQtEnumComboBox_fieldsTypes.setGeometry(QtCore.QRect(11, 185, 73, 22))
        self.MyQtEnumComboBox_fieldsTypes.setObjectName("MyQtEnumComboBox_fieldsTypes")
        self.MyQtEnumComboBox_range = MyQtEnumComboBox(NormalizeInput)
        self.MyQtEnumComboBox_range.setGeometry(QtCore.QRect(11, 156, 73, 22))
        self.MyQtEnumComboBox_range.setObjectName("MyQtEnumComboBox_range")
        self.MyQtEnumComboBox_normalizeMethod = MyQtEnumComboBox(NormalizeInput)
        self.MyQtEnumComboBox_normalizeMethod.setGeometry(QtCore.QRect(11, 127, 73, 22))
        self.MyQtEnumComboBox_normalizeMethod.setObjectName("MyQtEnumComboBox_normalizeMethod")
        self.MyQtEnumComboBox_fieldRoll = MyQtEnumComboBox(NormalizeInput)
        self.MyQtEnumComboBox_fieldRoll.setGeometry(QtCore.QRect(11, 98, 73, 22))
        self.MyQtEnumComboBox_fieldRoll.setObjectName("MyQtEnumComboBox_fieldRoll")
        self.lineEdit_name = QtWidgets.QLineEdit(NormalizeInput)
        self.lineEdit_name.setGeometry(QtCore.QRect(11, 11, 137, 22))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.radioButton_selected = QtWidgets.QRadioButton(NormalizeInput)
        self.radioButton_selected.setGeometry(QtCore.QRect(11, 247, 16, 16))
        self.radioButton_selected.setText("")
        self.radioButton_selected.setObjectName("radioButton_selected")
        self.pushButton_changeOrder = QtWidgets.QPushButton(NormalizeInput)
        self.pushButton_changeOrder.setGeometry(QtCore.QRect(10, 220, 111, 28))
        self.pushButton_changeOrder.setObjectName("pushButton_changeOrder")
        self.lineEdit_max = QtWidgets.QLineEdit(NormalizeInput)
        self.lineEdit_max.setGeometry(QtCore.QRect(10, 40, 113, 22))
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.lineEdit_min = QtWidgets.QLineEdit(NormalizeInput)
        self.lineEdit_min.setGeometry(QtCore.QRect(10, 70, 113, 22))
        self.lineEdit_min.setObjectName("lineEdit_min")

        self.retranslateUi(NormalizeInput)
        QtCore.QMetaObject.connectSlotsByName(NormalizeInput)

    def retranslateUi(self, NormalizeInput):
        _translate = QtCore.QCoreApplication.translate
        NormalizeInput.setWindowTitle(_translate("NormalizeInput", "Form"))
        self.MyQtEnumComboBox_fieldsTypes.setToolTip(_translate("NormalizeInput", "The current time"))
        self.MyQtEnumComboBox_fieldsTypes.setWhatsThis(_translate("NormalizeInput", "Enum combo box time."))
        self.MyQtEnumComboBox_range.setToolTip(_translate("NormalizeInput", "The current time"))
        self.MyQtEnumComboBox_range.setWhatsThis(_translate("NormalizeInput", "Enum combo box time."))
        self.MyQtEnumComboBox_normalizeMethod.setToolTip(_translate("NormalizeInput", "The current time"))
        self.MyQtEnumComboBox_normalizeMethod.setWhatsThis(_translate("NormalizeInput", "Enum combo box time."))
        self.MyQtEnumComboBox_fieldRoll.setToolTip(_translate("NormalizeInput", "The current time"))
        self.MyQtEnumComboBox_fieldRoll.setWhatsThis(
            _translate("NormalizeInput", "The analog clock widget displays the current time."))
        self.pushButton_changeOrder.setText(_translate("NormalizeInput", "Values Order"))
