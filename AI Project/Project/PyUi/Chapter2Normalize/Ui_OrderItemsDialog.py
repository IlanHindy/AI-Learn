# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\Chapter 2 - Normalize\OrderItemsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OrderItemsDialog(object):
    def setupUi(self, OrderItemsDialog):
        OrderItemsDialog.setObjectName("OrderItemsDialog")
        OrderItemsDialog.resize(374, 391)
        self.verticalLayout = QtWidgets.QVBoxLayout(OrderItemsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listView_items = QtWidgets.QListView(OrderItemsDialog)
        self.listView_items.setObjectName("listView_items")
        self.verticalLayout.addWidget(self.listView_items)
        self.gridLayout_buttons = QtWidgets.QGridLayout()
        self.gridLayout_buttons.setObjectName("gridLayout_buttons")
        self.pushButton_up = QtWidgets.QPushButton(OrderItemsDialog)
        self.pushButton_up.setObjectName("pushButton_up")
        self.gridLayout_buttons.addWidget(self.pushButton_up, 0, 0, 1, 1)
        self.pushButton_down = QtWidgets.QPushButton(OrderItemsDialog)
        self.pushButton_down.setObjectName("pushButton_down")
        self.gridLayout_buttons.addWidget(self.pushButton_down, 0, 1, 1, 1)
        self.pushButton_OK = QtWidgets.QPushButton(OrderItemsDialog)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.gridLayout_buttons.addWidget(self.pushButton_OK, 1, 0, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(OrderItemsDialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout_buttons.addWidget(self.pushButton_cancel, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_buttons)

        self.retranslateUi(OrderItemsDialog)
        self.pushButton_OK.clicked.connect(OrderItemsDialog.accept)
        self.pushButton_cancel.clicked.connect(OrderItemsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OrderItemsDialog)

    def retranslateUi(self, OrderItemsDialog):
        _translate = QtCore.QCoreApplication.translate
        OrderItemsDialog.setWindowTitle(_translate("OrderItemsDialog", "Dialog"))
        self.pushButton_up.setText(_translate("OrderItemsDialog", "Up"))
        self.pushButton_down.setText(_translate("OrderItemsDialog", "Down"))
        self.pushButton_OK.setText(_translate("OrderItemsDialog", "OK"))
        self.pushButton_cancel.setText(_translate("OrderItemsDialog", "Cancel"))
