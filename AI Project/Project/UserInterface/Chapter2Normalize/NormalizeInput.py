# Python Imports

# Third party imports
import numpy as np

# PyQt imports
# import PyQt5 import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy, QMessageBox, QDialog
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import pyqtSlot, Qt

# My imports
from ..Plugins.Widgets.MyQtEnumComboBox import MyQtEnumComboBox
from ...PyUi.Chapter2Normalize.Ui_NormalizeInput import Ui_NormalizeInput
from ...UserInterface.Chapter2Normalize.OrderItemsDialog import OrderItemsDialog
from ...AI.Chapter2Normalize import NormalizeData
from ...Infrastructure.Enums import FieldRolls, FieldsTypes, NormalizeRange, NormalizeMethod


class NormalizeInput(QWidget, Ui_NormalizeInput):
    """
    NormalizeInput

    Holds the widgets for getting the normalize parameters
    for one algorithm parameter

    The widget are arranged in one row of the grid of the containing dialog
     """

    def __init__(self,
                 parent,
                 dataMatrix: np.ndarray,
                 normalizeData: NormalizeData,
                 gridLayout: QGridLayout,
                 dialogRowIndex: int):
        """
        Initialize The NormalizeInput

        Args:
            parent          : The parent window
            dataMatrix      : The data matrix
            normalizeData   : A record of AlgorithmInput.NormalizeData for initialize
            panelLayout     : The grid to insert the widgets
            rowIndex        : The index in the grid

        """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        # Members setting
        self.setColIndex(dialogRowIndex)
        self.dataMatrix = dataMatrix
        self.valuesOrder = normalizeData["valuesOrder"]
        self.min = normalizeData["min"]
        self.max = normalizeData["max"]
        self.gridLayout = gridLayout
        self.indexInDataFile = normalizeData["indexInDataFile"]

        # fill the name line edit
        # if this is a temp row - set a temp name
        if self.colIndex == -1:
            self.lineEdit_name.setText("temp")
        else:
            self.lineEdit_name.setText(normalizeData["fieldName"])

        # Add the widgets to the grid layout of the AlgorithmDataDesign that host this class
        # if this is a temp object (for swap operations) - do not add the widgets to the grid
        if self.colIndex != -1:
            self.addWidgetsToPanel()

        # fill the values of the comboboxes
        self.MyQtEnumComboBox_fieldRoll.fillValues(FieldRolls)
        self.MyQtEnumComboBox_fieldsTypes.fillValues(FieldsTypes)
        self.MyQtEnumComboBox_range.fillValues(NormalizeRange)

        # Set the initial values of the min max line edits
        self.lineEdit_min.setText(str(normalizeData["min"]))
        self.lineEdit_max.setText(str(normalizeData["max"]))

        # Set the selections of the comboboxes
        # Field type:
        #   Set the index to the field type combo box
        #   Fill the NormalizeMethod combo box
        #   Set the enable attribute of the button
        self.MyQtEnumComboBox_fieldsTypes.setIndexFromValue(normalizeData["fieldType"])
        self.MyQtEnumComboBox_fieldTypes_currentIndexChanged(self.MyQtEnumComboBox_fieldsTypes.currentIndex())

        # Set the roll enum
        self.MyQtEnumComboBox_fieldRoll.setIndexFromValue(normalizeData["roll"])

        # Normalize method
        #   Set the index of the normalize method combo box
        #   Set the initial values of the min/max line edits
        #   Set the enable attribute of the line edits
        self.MyQtEnumComboBox_normalizeMethod.setIndexFromValue(normalizeData["normalizeMethod"])
        self.MyQtEnumComboBox_normalizeMethod_currentIndexChanged(self.MyQtEnumComboBox_normalizeMethod.currentIndex())
        self.MyQtEnumComboBox_fieldRoll_currentIndexChanged(self.MyQtEnumComboBox_fieldRoll.currentIndex())

        # Set the index or the normalize range
        self.MyQtEnumComboBox_range.setIndexFromValue(normalizeData["normalizeRange"])

        # Signals and slots connection
        self.MyQtEnumComboBox_fieldsTypes.currentIndexChanged.connect(
            self.MyQtEnumComboBox_fieldTypes_currentIndexChanged)
        self.MyQtEnumComboBox_normalizeMethod.currentIndexChanged.connect(
            self.MyQtEnumComboBox_normalizeMethod_currentIndexChanged)
        self.MyQtEnumComboBox_fieldRoll.currentIndexChanged.connect(self.MyQtEnumComboBox_fieldRoll_currentIndexChanged)

        # Button connect
        self.pushButton_changeOrder.clicked.connect(self.pushButton_changeOrder_clicked)

        # Set the width of the column
        self.lineEdit_name.setMinimumWidth(self.width())

    def setColIndex(self, dialogRowIndex: int):
        """
        Set the indexes :
        -   rowIndex : index of the row in the grid
        -   dialogRowIndex : index or the row in the dataMatrix

        Args:
            dialogRowIndex  (int) : The row in the lists and matrixes in the dialog           
        """

        # Note that the rowIndex of the NormalizedInput is the row in the grid
        # and because the grid has a header line the index in the rowIndex in the grid is
        # one larger than the row index in the data matrix
        if (dialogRowIndex == -1):
            self.colIndex = -1
        else:
            self.colIndex = dialogRowIndex + 1
        self.dialogRowIndex = dialogRowIndex

    def addWidgetsToPanel(self):
        """
        Adds the widgets of the NormalizeInput to the containing grid

        Args:
            parent          : The parent window
            inputMatrix     : The algorithm input values
            filename        : The data file name
        """
        self.gridLayout.addWidget(self.radioButton_selected, 1, self.colIndex, Qt.AlignCenter)
        self.gridLayout.addWidget(self.lineEdit_name, 2, self.colIndex)
        self.gridLayout.addWidget(self.MyQtEnumComboBox_fieldRoll, 3, self.colIndex)
        self.gridLayout.addWidget(self.MyQtEnumComboBox_fieldsTypes, 4, self.colIndex)
        self.gridLayout.addWidget(self.MyQtEnumComboBox_range, 5, self.colIndex)
        self.gridLayout.addWidget(self.MyQtEnumComboBox_normalizeMethod, 6, self.colIndex)
        self.gridLayout.addWidget(self.pushButton_changeOrder, 7, self.colIndex)
        self.gridLayout.addWidget(self.lineEdit_min, 8, self.colIndex)
        self.gridLayout.addWidget(self.lineEdit_max, 9, self.colIndex)

    def replaceInGrid(self, replacing, deleteWidgets: bool):
        """
        Replace a row with another a NormalizeInput

        Args:
            replacing (NormalizeInput)  : The replacing widgets
            deleteWidgets   (bool)      : Wether to delete the widgets of the replaced NormalizeInput
            
        """
        self.gridLayout.replaceWidget(self.radioButton_selected, replacing.radioButton_selected)
        self.gridLayout.replaceWidget(self.lineEdit_name, replacing.lineEdit_name)
        self.gridLayout.replaceWidget(self.MyQtEnumComboBox_fieldRoll, replacing.MyQtEnumComboBox_fieldRoll)
        self.gridLayout.replaceWidget(self.MyQtEnumComboBox_fieldsTypes, replacing.MyQtEnumComboBox_fieldsTypes)
        self.gridLayout.replaceWidget(self.MyQtEnumComboBox_range, replacing.MyQtEnumComboBox_range)
        self.gridLayout.replaceWidget(self.MyQtEnumComboBox_normalizeMethod, replacing.MyQtEnumComboBox_normalizeMethod)
        self.gridLayout.replaceWidget(self.pushButton_changeOrder, replacing.pushButton_changeOrder)
        #self.pushButton_changeOrder.resize(widgetWidth, widgetHeight)
        self.gridLayout.replaceWidget(self.lineEdit_min, replacing.lineEdit_min)
        #self.line_edit_min.resize(widgetWidth, widgetHeight)
        self.gridLayout.replaceWidget(self.lineEdit_max, replacing.lineEdit_max)
        if deleteWidgets:
            self.deleteWidgetsFromDialog()

    def deleteWidgetsFromDialog(self):
        """
        Delete the widgets of the NormalizeInput
        """
        self.radioButton_selected.deleteLater()
        self.lineEdit_name.deleteLater()
        self.MyQtEnumComboBox_fieldRoll.deleteLater()
        self.MyQtEnumComboBox_fieldsTypes.deleteLater()
        self.MyQtEnumComboBox_range.deleteLater()
        self.MyQtEnumComboBox_normalizeMethod.deleteLater()
        self.pushButton_changeOrder.deleteLater()
        self.lineEdit_min.deleteLater()
        self.lineEdit_max.deleteLater()

    def width(self) -> int:
        """
            Calculate the width of the AlgorithmDataDesign needed for the widgets
        """
        font = self.lineEdit_name.font()
        fontMetrics = QFontMetrics(font)
        return max([self.radioButton_selected.size().width() ,\
            fontMetrics.width(self.lineEdit_name.text())  , \
            self.MyQtEnumComboBox_fieldRoll.minWidth() , \
            self.MyQtEnumComboBox_fieldsTypes.minWidth() , \
            self.pushButton_changeOrder.size().width() , \
            self.MyQtEnumComboBox_range.minWidth() , \
            self.MyQtEnumComboBox_normalizeMethod.minWidth()])

    def height(self):
        return 45

    def setButtonSize(self):
        """
        Set the size of the changeOrder button
        """
        font = self.pushButton_changeOrder.font()
        fontMetrics = QFontMetrics(font)
        width = fontMetrics.width(self.pushButton_changeOrder.text()) + 25
        self.pushButton_changeOrder.setMinimumWidth(width)
        self.pushButton_changeOrder.setMaximumWidth(width)
        self.pushButton_changeOrder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

    @pyqtSlot(int)
    def MyQtEnumComboBox_fieldTypes_currentIndexChanged(self, index: int):
        """
            Slot that is activated when the field type is changed

            When the field type is changed the options for the normalize method
            change and there is a need to disable or enable the dialog for changing
            the values order

            Args:
                index           : The index of the selection in the field type combo box

        """
        # Set the NormalizeMethod enum and the button for the setting the order of the values
        # If the field type is qualitative
        #   Set the Normalize method enum
        #   Enable the button
        #   If the valuesOrder list is empty - create it
        if index in [FieldsTypes.NominalData.value, FieldsTypes.OrdinalData.value]:
            indexes = [
                NormalizeMethod.OneOfN.value, NormalizeMethod.QualitativeToRange.value,
                NormalizeMethod.EquilateralEncoding.value
            ]
            self.MyQtEnumComboBox_normalizeMethod.fillValues(NormalizeMethod, indexes)
            self.pushButton_changeOrder.setEnabled(True)
            if len(self.valuesOrder) == 0:
                self.valuesOrder = list(
                    set([self.dataMatrix[row, self.dialogRowIndex] for row in range(1, len(self.dataMatrix))]))

        # If the field type is quantitative
        #    Set the Normalize methods
        #    Disable the Values order buttons
        else:
            indexes = [NormalizeMethod.NormalizeToRange.value, NormalizeMethod.ReciprocalNormalization.value]
            self.MyQtEnumComboBox_normalizeMethod.fillValues(NormalizeMethod, indexes)
            self.pushButton_changeOrder.setEnabled(False)

    @pyqtSlot(int)
    def MyQtEnumComboBox_normalizeMethod_currentIndexChanged(self, index: int):
        """
        Slot that is activated when the normalize method is changed

        When the normalize method is changed the The min/max line edits
        has to be updated

        Args:
            index  : The index of the selection in the normalize method combo box
        """

        # Set the values of the min max line edit
        # If the new normalized method is equilateralEncoding:
        #   Set the min/max to [-1, 1]
        #   Set the fields disabled (Impossible to change)
        #   Set the color to white to indicate that the value was changed
        if self.MyQtEnumComboBox_normalizeMethod.selection() == NormalizeMethod.EquilateralEncoding:
            self.min = -1
            self.max = 1
            self.lineEdit_min.setText(str(self.min))
            self.lineEdit_min.setEnabled(False)
            self.lineEdit_min.setStyleSheet("color: White")
            self.lineEdit_max.setText(str(self.max))
            self.lineEdit_max.setEnabled(False)
            self.lineEdit_max.setStyleSheet("color: White")

        # If the new normalized method is QualitativeToRange:
        #   Set the min/max to [0, number of values]
        #   Set the fields disabled (Impossible to change)
        #   Set the color to white to indicate that the value was changed
        elif self.MyQtEnumComboBox_normalizeMethod.selection() == NormalizeMethod.QualitativeToRange:
            self.min = 0
            self.max = len(self.valuesOrder) - 1
            self.lineEdit_min.setText(str(self.min))
            self.lineEdit_min.setEnabled(False)
            self.lineEdit_min.setStyleSheet("color: White")
            self.lineEdit_max.setText(str(self.max))
            self.lineEdit_max.setEnabled(False)
            self.lineEdit_max.setStyleSheet("color: White")

        # If the new normalized method is OneOfN:
        # Set min/max to [0,0]
        # Disable the field
        elif self.MyQtEnumComboBox_normalizeMethod.selection() == NormalizeMethod.OneOfN:
            self.min = 0
            self.max = 0
            self.lineEdit_min.setText(str(self.min))
            self.lineEdit_min.setEnabled(False)
            self.lineEdit_min.setStyleSheet("color: Gray")
            self.lineEdit_max.setText(str(self.max))
            self.lineEdit_max.setEnabled(False)
            self.lineEdit_max.setStyleSheet("color: Gray")

        # If the field type is quantitative
        # If the max is 0 set the min and the max to the lower higher of the values
        # Enable the fields
        else:
            if float(self.lineEdit_max.text()) == 0.0:
                try:
                    colData = self.dataMatrix[1:, self.dialogRowIndex].astype(float)
                    self.min = np.min(colData)
                    self.max = np.max(colData)
                    self.lineEdit_min.setText(str(self.min))
                    self.lineEdit_max.setText(str(self.max))
                except:
                    pass
            self.lineEdit_min.setEnabled(True)
            self.lineEdit_min.setStyleSheet("color: White")
            self.lineEdit_max.setEnabled(True)
            self.lineEdit_max.setStyleSheet("color: White")

    @pyqtSlot(int)
    def MyQtEnumComboBox_fieldRoll_currentIndexChanged(self, index: int):
        """
        Slot for disable/enable the controls according to if
        the roll is a roll of parameters/results
        """
        if self.MyQtEnumComboBox_fieldRoll.selection() in (FieldRolls.Parameter, FieldRolls.Result):
            self.MyQtEnumComboBox_fieldsTypes.setEnabled(True)
            self.MyQtEnumComboBox_range.setEnabled(True)
            self.MyQtEnumComboBox_normalizeMethod.setEnabled(True)
            self.pushButton_changeOrder.setEnabled(True)
            self.lineEdit_min.setEnabled(True)
            self.lineEdit_max.setEnabled(True)
            self.MyQtEnumComboBox_fieldTypes_currentIndexChanged(self.MyQtEnumComboBox_fieldsTypes.currentIndex())
        else:
            self.MyQtEnumComboBox_fieldsTypes.setEnabled(False)
            self.MyQtEnumComboBox_range.setEnabled(False)
            self.MyQtEnumComboBox_normalizeMethod.setEnabled(False)
            self.pushButton_changeOrder.setEnabled(False)
            self.lineEdit_min.setEnabled(False)
            self.lineEdit_max.setEnabled(False)

    def pushButton_changeOrder_clicked(self):
        """
         Slot that is activating the values order setting dialog
        """
        orderItemsDialog = OrderItemsDialog(self, self.valuesOrder)
        if orderItemsDialog.exec_() == QDialog.Accepted:
            self.valuesOrder = orderItemsDialog.listToOrder

    def normalizeData(self) -> NormalizeData:
        """
        Collect the results of the dialog to AlgorithmInput.NormalizeData and return it
        """
        normalizeData = NormalizeData(self.indexInDataFile, "")
        normalizeData["fieldName"] = self.lineEdit_name.text()
        normalizeData["roll"] = self.MyQtEnumComboBox_fieldRoll.selection()
        normalizeData["fieldType"] = self.MyQtEnumComboBox_fieldsTypes.selection()
        normalizeData["normalizeRange"] = self.MyQtEnumComboBox_range.selection()
        normalizeData["normalizeMethod"] = self.MyQtEnumComboBox_normalizeMethod.selection()
        normalizeData["valuesOrder"] = self.valuesOrder
        normalizeData["min"] = float(self.lineEdit_min.text())
        normalizeData["max"] = float(self.lineEdit_max.text())
        return normalizeData

    def checkLegality(self) -> bool:
        """
        Check the legality of the normalize data parameters that where set.
        This method is activated when the OK button of the dialog is pressed
        The following are the checks:
        1. If the normalize method is of float all the values has to be numbers
        2. If the normalize method is of float the minimum has to be less or equal to the
           minimum of the values
        3. If the normalize method is of float the maximum has to be more or equal to the
           maximum of the values
        """
        # All the following checks are for field type that are numeric
        normalizeMethod = self.MyQtEnumComboBox_normalizeMethod.selection()
        name = self.lineEdit_name.text()

        if  normalizeMethod == NormalizeMethod.NormalizeToRange or \
                normalizeMethod == NormalizeMethod.ReciprocalNormalization:

            # All the data in the data fields are numeric
            try:
                colData = self.dataMatrix[1:, self.dialogRowIndex].astype(float)
            except:
                QMessageBox.critical(self, "AlgorithmDataDesign Error", "Error in column : " + \
                    name + " :\n" + \
                    "The field type is numeric but the data is not")
                return False

            # The value in the min max fields is numeric
            try:
                insertedMin = float(self.lineEdit_min.text())
                insertedMax = float(self.lineEdit_max.text())
            except:
                QMessageBox.critical(self, "AlgorithmDataDesign Error", "Error in column : " + \
                    name + " :\n" + \
                    "The value in the min or max fields is not float")
                return False

            # check the value in the min field is less than the min of the column
            colMin = np.min(colData)
            if insertedMin > colMin:
                QMessageBox.critical(self, "AlgorithmDataDesign Error", "Error in column : " + \
                    name + " :\n" + \
                    "The minimum of the data which is :" + str(colMin) + " :\n" + \
                    " Should be more than the inserted minimum which is : " + str(insertedMin))
                return False

            # check the value in the min field is less than the min of the column
            colMax = np.max(colData)
            if insertedMax < colMax:
                QMessageBox.critical(self, "AlgorithmDataDesign Error", "Error in column : " + \
                    name + " :\n" + \
                    "The maximum of the data which is :" + str(colMax) + " :\n" +\
                    " Should be less than the inserted maximum which is : " + str(insertedMax))
                return False
        return True
