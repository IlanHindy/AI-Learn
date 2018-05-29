# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 502)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_inputMatrix = QtWidgets.QLabel(self.centralwidget)
        self.label_inputMatrix.setObjectName("label_inputMatrix")
        self.verticalLayout.addWidget(self.label_inputMatrix)
        self.tableView_inputMatrix = QtWidgets.QTableView(self.centralwidget)
        self.tableView_inputMatrix.setObjectName("tableView_inputMatrix")
        self.verticalLayout.addWidget(self.tableView_inputMatrix)
        self.label_outputMatrix = QtWidgets.QLabel(self.centralwidget)
        self.label_outputMatrix.setObjectName("label_outputMatrix")
        self.verticalLayout.addWidget(self.label_outputMatrix)
        self.tableView_outputMatrix = QtWidgets.QTableView(self.centralwidget)
        self.tableView_outputMatrix.setObjectName("tableView_outputMatrix")
        self.verticalLayout.addWidget(self.tableView_outputMatrix)
        self.label_methodResults = QtWidgets.QLabel(self.centralwidget)
        self.label_methodResults.setObjectName("label_methodResults")
        self.verticalLayout.addWidget(self.label_methodResults)
        self.plainTextEdit_methodResults = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_methodResults.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_methodResults.setObjectName("plainTextEdit_methodResults")
        self.verticalLayout.addWidget(self.plainTextEdit_methodResults)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar_Main = QtWidgets.QMenuBar(MainWindow)
        self.menubar_Main.setGeometry(QtCore.QRect(0, 0, 570, 21))
        self.menubar_Main.setObjectName("menubar_Main")
        self.menuTests = QtWidgets.QMenu(self.menubar_Main)
        self.menuTests.setObjectName("menuTests")
        MainWindow.setMenuBar(self.menubar_Main)
        self.statusbar_Main = QtWidgets.QStatusBar(MainWindow)
        self.statusbar_Main.setObjectName("statusbar_Main")
        MainWindow.setStatusBar(self.statusbar_Main)
        self.toolBar_Main = QtWidgets.QToolBar(MainWindow)
        self.toolBar_Main.setObjectName("toolBar_Main")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_Main)
        self.action_test = QtWidgets.QAction(MainWindow)
        self.action_test.setObjectName("action_test")
        self.action_init = QtWidgets.QAction(MainWindow)
        self.action_init.setObjectName("action_init")
        self.action_numPy = QtWidgets.QAction(MainWindow)
        self.action_numPy.setObjectName("action_numPy")
        self.action_algorithmData = QtWidgets.QAction(MainWindow)
        self.action_algorithmData.setObjectName("action_algorithmData")
        self.action_algorithmInput = QtWidgets.QAction(MainWindow)
        self.action_algorithmInput.setObjectName("action_algorithmInput")
        self.action_charInput = QtWidgets.QAction(MainWindow)
        self.action_charInput.setObjectName("action_charInput")
        self.action_plot = QtWidgets.QAction(MainWindow)
        self.action_plot.setObjectName("action_plot")
        self.menuTests.addAction(self.action_init)
        self.menuTests.addAction(self.action_test)
        self.menuTests.addAction(self.action_numPy)
        self.menuTests.addAction(self.action_algorithmData)
        self.menuTests.addAction(self.action_algorithmInput)
        self.menuTests.addAction(self.action_charInput)
        self.menuTests.addAction(self.action_plot)
        self.menubar_Main.addAction(self.menuTests.menuAction())
        self.toolBar_Main.addAction(self.action_init)
        self.toolBar_Main.addAction(self.action_test)
        self.toolBar_Main.addAction(self.action_numPy)
        self.toolBar_Main.addAction(self.action_algorithmData)
        self.toolBar_Main.addAction(self.action_charInput)
        self.toolBar_Main.addAction(self.action_algorithmInput)
        self.toolBar_Main.addAction(self.action_plot)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_inputMatrix.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Input Matrix</span></p></body></html>"
            ))
        self.label_outputMatrix.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Output Matrix</span></p></body></html>"
            ))
        self.label_methodResults.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Method Results</span></p></body></html>"
            ))
        self.menuTests.setTitle(_translate("MainWindow", "tests"))
        self.toolBar_Main.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_test.setText(_translate("MainWindow", "Test"))
        self.action_test.setToolTip(_translate("MainWindow", "Perform class tests"))
        self.action_init.setText(_translate("MainWindow", "Init"))
        self.action_numPy.setText(_translate("MainWindow", "NumPy"))
        self.action_algorithmData.setText(_translate("MainWindow", "AlgorithmData"))
        self.action_algorithmInput.setText(_translate("MainWindow", "AlgorithmInput"))
        self.action_charInput.setText(_translate("MainWindow", "Char input"))
        self.action_plot.setText(_translate("MainWindow", "plot"))
