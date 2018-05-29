# Python Imports
# Thired party imports
# PyQt imports
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QDialog, QAbstractItemView
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, QItemSelectionModel

# My imports
from ..PyUi.Ui_SelectDialog import Ui_SelectDialog


class SelectDialog(QDialog, Ui_SelectDialog):
    """description of class"""

    def __init__(self, parent, title, text, options, enabledOptions=None, headerOptions=[], singleSelectionMode=True):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.label_text.setText(text)
        self.headerOptions = headerOptions
        self.singleSelectionMode = singleSelectionMode
        self.options = options
        self.initUi(options, enabledOptions, headerOptions, singleSelectionMode)
        self.pushButton_sellectAll.clicked.connect(self.pushButton_selectAll_clicked)
        self.pushButton_deSellectAll.clicked.connect(self.pushButton_deSelectAll_clicked)
        self.listView_options.clicked.connect(self.listView_options_clicked)

    def initUi(self, options, enabledOptions, headerOptions, singleSelectionMode):
        boldFont = QFont()
        boldFont.setBold(True)

        # set the selection mode
        if not singleSelectionMode:
            self.listView_options.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # create enableItems if none
        if enabledOptions is None:
            enabledOptions = [True for idx in range(len(options))]

        # Insert the choices
        self.standaredItemModel = QStandardItemModel(self.listView_options)
        self.standaredItemModel.itemChanged.connect(self.onItemChanged)
        for idx in range(len(options)):
            standaredItem = QStandardItem(options[idx])
            standaredItem.setSelectable(enabledOptions[idx])
            if idx in headerOptions:
                standaredItem.setFont(boldFont)
            self.standaredItemModel.appendRow(standaredItem)

        self.listView_options.setModel(self.standaredItemModel)

        # disable select all / de select all buttons if in single selection
        # mode
        if singleSelectionMode:
            self.pushButton_sellectAll.setDisabled(True)
            self.pushButton_deSellectAll.setDisabled(True)

    def onItemChanged(self, item):
        QMessageBox.information(self, "Selec Dialog Message", "Selected Item :" + item.text())

    def selection(self):
        return [index.row() for index in self.listView_options.selectionModel().selectedIndexes()]

    def pushButton_selectAll_clicked(self):
        selectIndexes = [idx for idx in range(self.standaredItemModel.rowCount())]
        self.setSelected(selectIndexes, QItemSelectionModel.Select)

    def pushButton_deSelectAll_clicked(self):
        selectIndexes = [idx for idx in range(self.standaredItemModel.rowCount())]
        self.setSelected(selectIndexes, QItemSelectionModel.Deselect)

    def setSelected(self, selectIndexes, newStatus):
        modelIndexes = [self.standaredItemModel.createIndex(rowIndex, 0) for rowIndex in selectIndexes]
        selectionModel = self.listView_options.selectionModel()
        for modelIndex in modelIndexes:
            selectionModel.select(modelIndex, newStatus)

    @pyqtSlot("QModelIndex")
    def listView_options_clicked(self, modelIndex):
        if self.singleSelectionMode:
            return

        row = modelIndex.row()
        if row in self.headerOptions:
            indexInHeaderOptions = self.headerOptions.index(row)
            if indexInHeaderOptions == len(self.headerOptions) - 1:
                selectedIndexes = [idx for idx in range(row, len(self.options))]
            else:
                selectedIndexes = [idx for idx in range(row, self.headerOptions[indexInHeaderOptions + 1])]
            selectionModel = self.listView_options.selectionModel()
            if modelIndex in selectionModel.selectedIndexes():
                newStatus = QItemSelectionModel.Select
            else:
                newStatus = QItemSelectionModel.Deselect
            self.setSelected(selectedIndexes, newStatus)
