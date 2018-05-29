# Python Imports

# Thired party imports

# PyQt imports
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# My imports
from Ui_NormalizeDialog import Ui_NormalizeDialog
from NormalizeInput import NormalizeInput
import AlgorithmInput


class NormalizeDialog(QDialog, Ui_NormalizeDialog):
    """
    Does nothing more than demonstrate syntax.

    This is an example of how a Pythonic human-readable docstring can
    get parsed by doxypypy and marked up with Doxygen commands as a
    regular input filter to Doxygen.

    Args:
        arg1:   A positional argument.
        arg2:   Another positional argument.

    Kwargs:
        kwarg:  A keyword argument.

    Returns:
        A string holding the result.

    Raises:
        ZeroDivisionError, AssertionError, & ValueError.

    Examples:
        >>> myfunction(2, 3)
        '5 - 0, whatever.'
        >>> myfunction(5, 0, 'oops.')
        Traceback (most recent call last):
            ...
        ZeroDivisionError: integer division or modulo by zero
        >>> myfunction(4, 1, 'got it.')
        '5 - 4, got it.'
        >>> myfunction(23.5, 23, 'oh well.')
        Traceback (most recent call last):
            ...
        AssertionError
        >>> myfunction(5, 50, 'too big.')
        Traceback (most recent call last):
            ...
        ValueError
     """

    def __init__(self, parent, inputMatrix, normalizeData = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.inputMatrix = inputMatrix
        if normalizeData == None:
            self.normalizeData = [AlgorithmInput.NormalizeData() for idx in range(len(inputMatrix))]
        else:
            self.normalizeData = normalizeData
        self.setFixedSize(self.initNormilizeInput())

    def initNormilizeInput(self):
        height = 0
        insertIndex = 0
        width = 0
        self.normalizeInputList = []
        for fieldName in self.inputMatrix[0]:
            normalizeInput = NormalizeInput(self, self.inputMatrix, self.normalizeData, self.gridLayout_fields, insertIndex)
            size = normalizeInput.size()
            height += size.height()
            insertIndex += 1
            width = max([width, normalizeInput.sumWidth()])
            self.normalizeInputList.append(normalizeInput)
        return QSize(width, height + 100)

    def accept(self):
        self.buildNormalizeData()
        super(NormalizeDialog, self).accept()
        #self.setResult(QDialog.Accepted)
        #self.close()

    def reject(self):
        self.setResult(QDialog.Rejected)
        self.close()

    def buildNormalizeData(self):
        self.normalizeData = []
        for normalizeInput in self.normalizeInputList:
            self.normalizeData.append(normalizeInput.normalizeData())
            









