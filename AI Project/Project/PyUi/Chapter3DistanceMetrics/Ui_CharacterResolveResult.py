# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\Chapter 3 - Distance Metrics\CharacterResolveResult.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CharacterResolveResult(object):
    def setupUi(self, CharacterResolveResult):
        CharacterResolveResult.setObjectName("CharacterResolveResult")
        CharacterResolveResult.resize(569, 223)
        self.horizontalLayout = QtWidgets.QHBoxLayout(CharacterResolveResult)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_characterToResolve = QtWidgets.QVBoxLayout()
        self.verticalLayout_characterToResolve.setObjectName("verticalLayout_characterToResolve")
        self.graphicsView_characterToResolve = QtWidgets.QGraphicsView(CharacterResolveResult)
        self.graphicsView_characterToResolve.setObjectName("graphicsView_characterToResolve")
        self.verticalLayout_characterToResolve.addWidget(self.graphicsView_characterToResolve)
        self.label = QtWidgets.QLabel(CharacterResolveResult)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_characterToResolve.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout_characterToResolve)
        self.verticalLayout_selectedCharacter = QtWidgets.QVBoxLayout()
        self.verticalLayout_selectedCharacter.setObjectName("verticalLayout_selectedCharacter")
        self.graphicsView_selectedCharacter = QtWidgets.QGraphicsView(CharacterResolveResult)
        self.graphicsView_selectedCharacter.setObjectName("graphicsView_selectedCharacter")
        self.verticalLayout_selectedCharacter.addWidget(self.graphicsView_selectedCharacter)
        self.label_selectedCharacter = QtWidgets.QLabel(CharacterResolveResult)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_selectedCharacter.setFont(font)
        self.label_selectedCharacter.setAlignment(QtCore.Qt.AlignCenter)
        self.label_selectedCharacter.setObjectName("label_selectedCharacter")
        self.verticalLayout_selectedCharacter.addWidget(self.label_selectedCharacter)
        self.horizontalLayout.addLayout(self.verticalLayout_selectedCharacter)

        self.retranslateUi(CharacterResolveResult)
        QtCore.QMetaObject.connectSlotsByName(CharacterResolveResult)

    def retranslateUi(self, CharacterResolveResult):
        _translate = QtCore.QCoreApplication.translate
        CharacterResolveResult.setWindowTitle(_translate("CharacterResolveResult", "Dialog"))
        self.label.setText(_translate("CharacterResolveResult", "Character to Resolve"))
        self.label_selectedCharacter.setText(
            _translate("CharacterResolveResult", "Selected Character"))
