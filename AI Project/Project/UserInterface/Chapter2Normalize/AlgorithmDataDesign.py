# Python Imports
import pickle

# Third party imports
import numpy as np

# PyQt imports
# from PyQt5.QtCore import
from PyQt5.QtWidgets import QDialog, QMessageBox
# from PyQt5.QtGui import *

# My imports
from ...PyUi.Chapter2Normalize.Ui_AlgorithmDataDesign import Ui_AlgorithmDataDesign
from ...UserInterface.Chapter2Normalize.NormalizeInput import NormalizeInput
from ...AI.Chapter2Normalize import NormalizeData
from ...Utilities.FileUtiles import FileUtiles
from ..Plugins.Widgets.MyQtEnumComboBox import MyQtEnumComboBox
from ..Parameter import Parameter


class AlgorithmDataDesign(QDialog, Ui_AlgorithmDataDesign):
    """
    AlgorithmDataDesign

    The AlgorithmDataDesign is handeling the input of the
    parameters for an algorithm implementation

    -   The dialog is composed from a grid.
    -   Each grid row contains a definition for one field

    The normalize dialog is composed from a grid.
    Each row in the grid holds the widgets of one NormalizeInput object
    The NormalizeInput object handles the input for the normalizing for one
    parameter

     """

    def __init__(self, parent, dataMatrix: np.ndarray, filename: str = None):
        """
        Initialize The AlgorithmDataDesign

        Args:
            parent          : The parent window
            dataMatrix      : The algorithm input values
            filename        : The data file name
        """
        QDialog.__init__(self, parent)

        # member assigning
        self.setupUi(self)
        self.dataMatrix = dataMatrix

        # Loading the last normalize data from a file
        # The file name is based on the name of the file of the data
        # There is an attempt to load the normalize data file.
        # If failed - a default normalize data is created
        self.designFilename = self.createNormalizeDataFilename(filename)
        result, self.normalizeData, self.dataMatrix = self.loadNormalizeData(
            dataMatrix)
        if not result:
            self.normalizeData = [
                NormalizeData(idx, dataMatrix[0, idx])
                for idx in range(dataMatrix.shape[1])
            ]

        # Init the grid which contains the widgets for setting the normalize data
        self.initNormalizeInput()

        # Connections for buttons
        self.pushButton_addField.clicked.connect(
            self.pushButton_addField_clicked)
        self.pushButton_removeField.clicked.connect(
            self.pushButton_removeField_clicked)
        self.pushButton_up.clicked.connect(self.pushButton_up_clicked)
        self.pushButton_down.clicked.connect(self.pushButton_down_clicked)
        self.pushButton_OK.clicked.connect(self.accept)
        self.pushButton_Cancel.clicked.connect(self.reject)

    def createNormalizeDataFilename(self, filename):
        """
        Create the normalize data file name from the data file name

        The construction : add "normalizeData at the end of the file name

        """
        insertionIndex = filename.index(".csv")
        return filename[:insertionIndex] + "_normalizeData" + ".csv"

    def loadNormalizeData(self, rowDataMatrix):
        """
        Load normalize data from a file and fit the data matrix to the normalize data

        -   Each row in the normalize data represent a column in the data matrix
        -   there are 2 possibilities for a column
            -#  The column is representing a column in the data matrix : In this case
                the column will be copied from the row data matrix to the target data matrix
                according to the column number in the normalize data
            -#  The column is not part of the data matrix : In this case the column number in the
                normalize data will be -1 and the method will add an empty column to the data matrix
        
        Args :
            rowDataMatrix : ndarray with 2 dimensions (this parameter is for use of multipile activation
                            of the method for different arrays (specifically algorithm data and test data))

        Returns:
            bool            : if the load from the file succeeded
            normalizeData   : the normalize data matrix
            ndarray 2d      : the converted data matrix
        """
        dataMatrix = []
        try:
            normalizeData = Parameter.from_csv(self.designFilename)
        except Exception as e:
            QMessageBox.information(self, "AlgorithmDataDesign dialog",
                                    "Failed to load from file error is : \n" +
                                    str(e) + "\nGenerating new")
            return False, None, rowDataMatrix

        for nd in normalizeData:
            if (nd["indexInDataFile"] == -1):
                newCol = np.full(
                    rowDataMatrix.shape[0], "0", dtype=np.dtype(('U100', 1)))
                newCol[0] = nd["fieldName"]
                dataMatrix.append(newCol)
            else:
                dataMatrix.append(rowDataMatrix[:, nd["indexInDataFile"]])
        dataMatrix = np.stack(dataMatrix, axis=-1)

        return True, normalizeData, dataMatrix

    def saveNormalizeData(self):
        """
        Save the normalize data to a file upon exit
        """
        Parameter.to_csv(self.normalizeData, self.designFilename)

    def initNormalizeInput(self):
        """
        Initialize The fields input

        -   Each field is represented by a NormalizeInput
        -   The fields are arranged in GridLayout
        -   The dialog dimensions are set


        """
        insertIndex = 0
        self.normalizeInputList = []
        for normalizeData in self.normalizeData:
            normalizeInput = NormalizeInput(
                self, self.dataMatrix, normalizeData, self.gridLayout_fields,
                insertIndex)
            insertIndex += 1
            self.normalizeInputList.append(normalizeInput)
        self.setSelected(0)
        self.setDialogSize()

    def pushButton_addField_clicked(self):
        """
        Add a field to the normalize data
        """

        # Add column to the end of the data matrix
        newColumn = [["name"]]
        newColumn.extend(
            [["0"] for idx in range(self.dataMatrix.shape[0] - 1)])
        self.dataMatrix = np.hstack((self.dataMatrix, newColumn))

        # add a new line of controls in the grid
        insertionIndex = len(self.normalizeInputList)
        normalizeInput = NormalizeInput(self, self.dataMatrix,
                                        NormalizeData(-1, "Name"),
                                        self.gridLayout_fields, insertionIndex)
        self.normalizeInputList.append(normalizeInput)

        # set the last control as selected
        self.setSelected(len(self.normalizeInputList) - 1)

        # Update the rowIndex variable and the data matrix in the NormalizeInput
        # self.updateNormalizeInput()

        self.scrollArea_fields.horizontalScrollBar().setPageStep(1)
        self.scrollArea_fields.horizontalScrollBar().setValue(
            self.scrollArea_fields.horizontalScrollBar().maximum() + 100)

    def pushButton_removeField_clicked(self):
        """
        Remove a field from the list
        """

        # find the selected row
        selectedRow = self.selectedIndex()

        # delete from grid
        self.normalizeInputList[selectedRow].deleteWidgetsFromDialog()

        # delete the row from the lists (the dataMatrix and the normalizeInput matrix
        del self.normalizeInputList[selectedRow]
        self.dataMatrix = np.delete(self.dataMatrix, selectedRow, 1)

        # Update the rowIndex variable and the matrix in the NormalizeInput
        self.updateNormalizeInput()

        # set the selected row to one above the deleted row (if it is not already 0)
        if selectedRow == 0:
            self.setSelected(0)
        else:
            self.setSelected(selectedRow - 1)

    def updateNormalizeInput(self):
        """
        Update the normalize input with the following (after change like add, remove up down)

        Update the following fields:
        -   rowIndex
        -   dialogIndex
        -   dataMatrix

        Args:
            parent          : The parent window
            inputMatrix     : The algorithm input values
            filename        : The data file name
        """
        for row_idx in range(len(self.normalizeInputList)):
            self.normalizeInputList[row_idx].setColIndex(row_idx)
            self.normalizeInputList[row_idx].dataMatrix = self.dataMatrix

    def selectedIndex(self) -> int:
        """
        Returns the selected row

        Returns:
            The selected row index
        """
        for row_idx in range(len(self.normalizeInputList)):
            if self.normalizeInputList[
                    row_idx].radioButton_selected.isChecked():
                return row_idx
        QMessageBox.warning(self, "Create AlgorithmData dialog",
                            "No row selected")
        return -1

    def setDialogSize(self):
        """
        Sets the dialog size :
        -   height = sum of the heights of the NormalizeInputs
        -   width - max of the width of the NormalizeInput
        """
        #self.label_selected.setFixedHeight(self.normalizeInputList[0].radioButton_selected.size().height() + 20)
        #self.label_name.setFixedHeight(self.normalizeInputList[0].lineEdit_name.size().height() + 10)
        #self.label_fieldRoll.setFixedHeight(self.normalizeInputList[0].MyQtEnumComboBox_fieldRoll.size().height() + 10)
        #self.label_fieldType.setFixedHeight(self.normalizeInputList[0].MyQtEnumComboBox_fieldsTypes.size().height() + 10)
        #self.label_normalizedRange.setFixedHeight(self.normalizeInputList[0].MyQtEnumComboBox_range.size().height() + 10)
        # The height is the sum of the height of the fields
        # The width is the max of the width of the fields
        #height = 0
        #width = 0
        #for row_idx in range(len(self.normalizeInputList)):
        #    height += self.normalizeInputList[row_idx].height()
        #    width += self.normalizeInputList[row_idx].width()
        self.gridLayout_fields.setColumnMinimumWidth(100, 100)
        #self.setFixedSize(700, height + 1000)

    def setSelected(self, selectedRow):
        """
        Set the selected row
        """
        self.normalizeInputList[selectedRow].radioButton_selected.setChecked(
            True)
        self.selectedRow = selectedRow

    def pushButton_up_clicked(self):
        """
        Move the selected row one line up
        """

        # get the selected index
        selectedRow = self.selectedIndex()

        # swap the selected row with the one before (if the index of the selected row is not 0)
        if selectedRow == 0:
            QMessageBox.warning(
                self, "AlgorithmData creating",
                "Cannot move this field up because it is on the top location")
        else:
            self.swapRows(selectedRow, selectedRow - 1)

    def pushButton_down_clicked(self):
        """
        Move the selected row one line down
        """
        selectedRow = self.selectedIndex()
        if selectedRow == len(self.normalizeInputList) - 1:
            QMessageBox.warning(
                self, "AlgorithmData creating",
                "Cannot move this field down because it is on the bottom location"
            )
        else:
            self.swapRows(selectedRow, selectedRow + 1)

    def swapRows(self, firstRow: int, secondRow: int):
        """
        Swap between 2 rows (used in Up and Down)
        """

        # Create 2 temp Normalize input
        firstTemp = NormalizeInput(self, self.dataMatrix,
                                   NormalizeData(-1, "Temp"),
                                   self.gridLayout_fields, -1)
        secondTemp = NormalizeInput(self, self.dataMatrix,
                                    NormalizeData(-1, "Temp"),
                                    self.gridLayout_fields, -1)

        # Replace the existing rows with the temp rows
        self.normalizeInputList[firstRow].replaceInGrid(firstTemp, False)
        self.normalizeInputList[secondRow].replaceInGrid(secondTemp, False)

        # Replace the temp rows with the existing rows (in reverse order)
        firstTemp.replaceInGrid(self.normalizeInputList[secondRow], True)
        secondTemp.replaceInGrid(self.normalizeInputList[firstRow], True)

        # swap the rows in the NormalizedInputList
        self.normalizeInputList[firstRow], self.normalizeInputList[secondRow] = \
            self.normalizeInputList[secondRow], self.normalizeInputList[firstRow]

        # Update the rowIndex variable and the matrix in the NormalizeInput
        self.updateNormalizeInput()

        # swap the columns in the dataMatrix
        self.dataMatrix[:, [firstRow, secondRow
                            ]] = self.dataMatrix[:, [secondRow, firstRow]]

    def accept(self):
        """
        Accepts the normalize parameters

        Composed from 3 stages:
        1. Check the legality of inputs (each NormalizeInput)
        2. Collect the NormalizeData
        3. Save the normalize data in a file
        """
        if self.checkLegality():
            self.buildNormalizeData()
            self.saveNormalizeData()
            super(AlgorithmDataDesign, self).accept()

    def buildNormalizeData(self):
        """
        Build normalize data

        build the normalizedData from by calling to the
        buildNormalizeData of the NormalizeInput for each field
        """
        self.normalizeData = []
        for normalizeInput in self.normalizeInputList:
            self.normalizeData.append(normalizeInput.normalizeData())

    def checkLegality(self) -> bool:
        """
         Check normalize data

        Check the normalizedData from by calling to the
        checkLegality of the NormalizeInput for each field
        """
        for normalizeInput in self.normalizeInputList:
            if not normalizeInput.checkLegality():
                return False
        return True
