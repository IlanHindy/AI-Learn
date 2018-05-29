# Python Imports
import sys
import os
import threading
import time
import importlib

# Thired party imports
import numpy as np
import numpy.core.defchararray as npc

# PyQt imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox
from PyQt5.QtGui import QTextCharFormat, QFont

# My imports
from ..Utilities.FileUtiles import FileUtiles
from .PlotDialog import PlotDialog
from .RunningDialog import RunningDialog
from ..config import dataDir
from ..PyUi.Ui_MainWindow import Ui_MainWindow
from ..Infrastructure.AlgorithmData import AlgorithmData
from ..UserInterface.SelectDialog import SelectDialog
from ..Utilities.PythonTools import PythonTools
from ..UserInterface.MyQt import MyQtTableModel
from ..Infrastructure.AlgorithmData import AlgorithmData, AlgorithmDataInterface
from ..Infrastructure.AlgorithmInput import AlgorithmInput
from ..AI.Chapter2Normalize import NormalizeData
from ..UserInterface.Chapter3DistanceMetrics.CharacterIdentifier import CharacterIdentifier


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        matrix1 = npc.array([["abc" for i in range(5)] for j in range(2)])
        matrix2 = np.array([[i for i in range(5)] for j in range(3)])
        self.tablemodel_inputMatrix = MyQtTableModel(matrix1)
        self.tableView_inputMatrix.setModel(self.tablemodel_inputMatrix)
        self.tablemodel_outputMatrix = MyQtTableModel(matrix2)
        self.tableView_outputMatrix.setModel(self.tablemodel_outputMatrix)
        self.action_init.triggered.connect(self.action_init_triggered)
        self.action_test.triggered.connect(self.action_test_triggered)
        self.action_numPy.triggered.connect(self.action_numPy_triggered)
        self.action_algorithmData.triggered.connect(self.action_algorithmData_triggered)
        self.action_algorithmInput.triggered.connect(self.action_algorithmInput_triggered)
        self.action_charInput.triggered.connect(self.action_charInput_triggered)
        self.action_plot.triggered.connect(self.action_plot_triggered)
        self.initTests()
        self.normailzeData = None

    def action_plot_triggered(self):
        runningDialog = RunningDialog(self)
        runningDialog.exec_()

    def action_init_triggered(self):
        self.count = 0
        #timerThread = QThread(self)
        #timer = QTimer()
        #timer.setInterval(1000)
        #timer.moveToThread(timerThread)
        #timer.timeout.connect(self.timeout)
        #timerThread.start()
        #self.timer = threading.Timer(1,self.timeout)
        #timer = QTimer(self)
        #timer.timeout.connect(self.timeout)
        #self.connect(timer, SIGNAL("timeout()"), self.update)
        e = threading.Event()
        t1 = threading.Thread(name='block', target=self.timeout, args=(e,))
        t1.start()

        parentCount = 0
        for i in range(1000):
            parentCount += 1
            time.sleep(0.1)
            print("parent thread count = " + str(parentCount))
        #timerThread.exit()
        e.set()

    def timeout(self, e):
        while not e.isSet():
            self.count += 1
            print(" in timeout count = " + str(self.count))
            time.sleep(1)
        #standaredMatrix = StandaredMatrix(10,5)
        #self.tablemodel_inputMatrix.arraydata = StandaredMatrix(10,5)
        #self.tablemodel_OutputMatrix.arraydata = StandaredMatrix(10,5)

    def action_numPy_triggered(self):
        array = np.arange(15).reshape(3, 5)
        self.tablemodel_inputMatrix.setData(array)

    def action_algorithmData_triggered(self):
        x = np.matrix([[1, 2], [3, 4]])
        names = np.array(["First", "Second"])
        types = np.array([9, 10])
        min = np.array([0, 0])
        max = np.array([100, 100])
        y = AlgorithmData(x, names, types, min, max)
        array = AlgorithmDataInterface(y)
        self.tablemodel_inputMatrix.setData(array)

    def action_algorithmInput_triggered(self):
        try:
            normalizeDataAsMatrix, self.normailzeData, normalizedInput = AlgorithmInput.loadAndNormalize(
                self, os.path.join(dataDir, "Chapter 2 - Normalize", "iris.csv"), self.normailzeData)
            self.tablemodel_inputMatrix.setData(normalizeDataAsMatrix)
            self.tablemodel_outputMatrix.setData(normalizedInput)
        except:
            PythonTools.printException("")

    def initTests(self):
        self.testClass = None

    def action_test_triggered(self):
        try:
            if self.testClass is None:
                self.plainTextEdit_methodResults.clear()

                # select the test module
                testDir = os.path.dirname(os.path.abspath(__file__))
                testDir = os.path.join(testDir, "..", "Tests")
                testFiles = FileUtiles.GetAllFilesInFolder(testDir)
                selectDialog = SelectDialog(self, "Select the test file", "Select test", testFiles)
                if not selectDialog.exec_():
                    return
                else:
                    # Importing the module
                    self.testModule = importlib.import_module(".Tests." + testFiles[selectDialog.selection()[0]],
                                                              "Project")

                    # Getting the class instance
                    self.testClass = getattr(self.testModule, testFiles[selectDialog.selection()[0]])
                    self.testClass = self.testClass(self)

                # select the checks to perform
                selectDialog = SelectDialog(self, "Select the checks to perform", "Checks selection",
                                            self.testClass.getAllChecksToList(), None,
                                            self.testClass.headerIndexes(), False)
                if not selectDialog.exec_():
                    self.testClass = None
                    return
                else:
                    self.checksSelected = selectDialog.selection()

            # perform the check
            self.testClass.checkStage = self.checksSelected[0]
            self.addTestResult(self.testClass.check())
            if not (self.testClass.inputMatrix is None):
                self.tablemodel_inputMatrix.setData(self.testClass.inputMatrix)
                self.tablemodel_outputMatrix.setData(self.testClass.outputMatrix)
            del self.checksSelected[:1]
            if self.checksSelected == []:
                QMessageBox.information(self, "MainWindow Message", "Test Ended")
                self.testClass = None
        except Exception as e:
            PythonTools.printException("Error while testing matrix")
            self.testClass = None

    def addTestResult(self, results):
        textCharFormat = QTextCharFormat()
        if results[0]:
            textCharFormat.setFontWeight(QFont.Bold)
        elif results[1] == False:
            textCharFormat.setForeground(Qt.yellow)
        self.plainTextEdit_methodResults.textCursor().insertText(results[2] + "\n", textCharFormat)
        self.plainTextEdit_methodResults.verticalScrollBar().setValue(
            self.plainTextEdit_methodResults.verticalScrollBar().maximum())

    def action_charInput_triggered(self):
        characterIdentifier = CharacterIdentifier(self)
        if characterIdentifier.initResult:
            characterIdentifier.exec_()
