# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\SelectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectDialog(object):
    def setupUi(self, SelectDialog):
        SelectDialog.setObjectName("SelectDialog")
        SelectDialog.resize(446, 300)
        self.layoutWidget = QtWidgets.QWidget(SelectDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 397, 259))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.label_text = QtWidgets.QLabel(self.layoutWidget)
        self.label_text.setObjectName("label_text")
        self.verticalLayout_main.addWidget(self.label_text)
        self.listView_options = QtWidgets.QListView(self.layoutWidget)
        self.listView_options.setObjectName("listView_options")
        self.verticalLayout_main.addWidget(self.listView_options)
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.pushButton_OK = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.horizontalLayout_buttons.addWidget(self.pushButton_OK)
        self.pushButton_sellectAll = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_sellectAll.setObjectName("pushButton_sellectAll")
        self.horizontalLayout_buttons.addWidget(self.pushButton_sellectAll)
        self.pushButton_deSellectAll = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_deSellectAll.setObjectName("pushButton_deSellectAll")
        self.horizontalLayout_buttons.addWidget(self.pushButton_deSellectAll)
        self.pushButton_cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_buttons.addWidget(self.pushButton_cancel)
        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)

        self.retranslateUi(SelectDialog)
        self.pushButton_OK.clicked.connect(SelectDialog.accept)
        self.pushButton_cancel.clicked.connect(SelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectDialog)

    def retranslateUi(self, SelectDialog):
        _translate = QtCore.QCoreApplication.translate
        SelectDialog.setWindowTitle(_translate("SelectDialog", "Dialog"))
        self.label_text.setText(
            _translate(
                "SelectDialog",
                "<html><head/><body><p><span style=\" font-size:10pt;\">Select Items</span></p></body></html>"
            ))
        self.pushButton_OK.setText(_translate("SelectDialog", "OK"))
        self.pushButton_sellectAll.setText(_translate("SelectDialog", "Select All"))
        self.pushButton_deSellectAll.setText(_translate("SelectDialog", "DeSelect All"))
        self.pushButton_cancel.setText(_translate("SelectDialog", "Cancel"))
