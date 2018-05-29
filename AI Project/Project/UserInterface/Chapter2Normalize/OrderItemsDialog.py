# Python Imports

# Third party imports

# PyQt imports
from PyQt5.QtCore import QPoint, QStringListModel
from PyQt5.QtWidgets import QDialog

# My imports
from ...PyUi.Chapter2Normalize.Ui_OrderItemsDialog import Ui_OrderItemsDialog


class OrderItemsDialog(QDialog, Ui_OrderItemsDialog):
    """
    This class is a dialog for changing the order of qualitative parameter's values

    The dialog lists the values and allow changing the order using Up and Down buttons
    which replace the selected value with the one before/after it in the list
    """

    def __init__(self, parent, listToOrder: list):
        """
        Initialize the change order dialog

        Args:
            parent : (QDialog) - The parent dialog
            listToOrder : (list) - The list to set the order for
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.listToOrder = listToOrder
        self.model = QStringListModel(self)
        self.model.setStringList(listToOrder)
        self.listView_items.setModel(self.model)
        self.pushButton_up.clicked.connect(self.pushButton_up_clicked)
        self.pushButton_down.clicked.connect(self.pushButton_down_clicked)

    def pushButton_up_clicked(self):
        """
        Replace the selected item with the one before it
        """
        selectedIndex = self.listView_items.currentIndex().row()
        self.replaceItems(selectedIndex, selectedIndex - 1)

    def pushButton_down_clicked(self):
        """
        Replace the selected item with the one after it
        """
        selectedIndex = self.listView_items.currentIndex().row()
        self.replaceItems(selectedIndex, selectedIndex + 1)

    def replaceItems(self, fromIndex, toIndex):
        """
        Replace 2 items

        Args:
            fromIndex   : (int) - the index of the selected item
            toIndex     : (int) - the target index of the selected item
        """
        if toIndex in range(len(self.listToOrder)):
            temp = self.listToOrder[toIndex]
            self.listToOrder[toIndex] = self.listToOrder[fromIndex]
            self.listToOrder[fromIndex] = temp
            self.model.setStringList(self.listToOrder)
            self.model.dataChanged.emit(
                self.listView_items.indexAt(QPoint(0, 0)),
                self.listView_items.indexAt(QPoint(len(self.listToOrder), 0)))
            index = self.model.createIndex(toIndex, 0)
            self.listView_items.setCurrentIndex(index)
