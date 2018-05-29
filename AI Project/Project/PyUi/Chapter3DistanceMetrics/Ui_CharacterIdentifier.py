# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\Chapter 3 - Distance Metrics\CharacterIdentifier.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CharacterIdentifier(object):
    def setupUi(self, CharacterIdentifier):
        CharacterIdentifier.setObjectName("CharacterIdentifier")
        CharacterIdentifier.resize(500, 428)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        CharacterIdentifier.setFont(font)
        CharacterIdentifier.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.verticalLayout_main = QtWidgets.QVBoxLayout(CharacterIdentifier)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.graphicsView = QtWidgets.QGraphicsView(CharacterIdentifier)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_main.addWidget(self.graphicsView)
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.pushButton_reload = QtWidgets.QPushButton(CharacterIdentifier)
        self.pushButton_reload.setObjectName("pushButton_reload")
        self.horizontalLayout_buttons.addWidget(self.pushButton_reload)
        self.pushButton_add = QtWidgets.QPushButton(CharacterIdentifier)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout_buttons.addWidget(self.pushButton_add)
        self.pushButton_remove = QtWidgets.QPushButton(CharacterIdentifier)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.horizontalLayout_buttons.addWidget(self.pushButton_remove)
        self.pushButton_edit = QtWidgets.QPushButton(CharacterIdentifier)
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.horizontalLayout_buttons.addWidget(self.pushButton_edit)
        self.pushButton_resolve = QtWidgets.QPushButton(CharacterIdentifier)
        self.pushButton_resolve.setObjectName("pushButton_resolve")
        self.horizontalLayout_buttons.addWidget(self.pushButton_resolve)
        self.pushButton_exit = QtWidgets.QPushButton(CharacterIdentifier)
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.horizontalLayout_buttons.addWidget(self.pushButton_exit)
        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)

        self.retranslateUi(CharacterIdentifier)
        QtCore.QMetaObject.connectSlotsByName(CharacterIdentifier)

    def retranslateUi(self, CharacterIdentifier):
        _translate = QtCore.QCoreApplication.translate
        CharacterIdentifier.setWindowTitle(_translate("CharacterIdentifier", "Dialog"))
        self.pushButton_reload.setText(_translate("CharacterIdentifier", "Reload"))
        self.pushButton_add.setText(_translate("CharacterIdentifier", "Add "))
        self.pushButton_remove.setText(_translate("CharacterIdentifier", "Remove"))
        self.pushButton_edit.setText(_translate("CharacterIdentifier", "Edit"))
        self.pushButton_resolve.setText(_translate("CharacterIdentifier", "Resolve"))
        self.pushButton_exit.setText(_translate("CharacterIdentifier", "Exit"))
