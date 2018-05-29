#!/usr/bin/env python
# Python Imports
import sys
import os
import pprint

# Third party imports
import numpy as np

# PyQt imports
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.QtGui import QFontMetrics

# My imports
try:
    pass
except:
    if not "paths" in sys.modules:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        sys.path.append(os.path.join(dir_path, "..", "..", ".."))
        import Paths


class MyQtEnumComboBox(QComboBox):
    """
        ComboBox that is based on enum
    """

    def __init__(self, parent=None):
        """
        Initialize the MyQtEnumComboBox
        """
        super(MyQtEnumComboBox, self).__init__(parent)
        self.enum = None

    def fillValues(self, enum, indexes=None):
        """
        Fill the values of the enum in the combo box

        Args:
            enum    : (Enum)    - The enum that this ComboBox presents
            indexes : (List[int]] - If not all the values has to be presented -
                                    The indexes of the values to present
        """
        self.enum = enum
        self.clear()
        if indexes is None:
            indexes = [idx for idx in range(len(enum))]
        for member in enum:
            if member.value in indexes:
                self.addItem(str(member.name))
        self.setCurrentIndex(0)

    def minWidth(self):
        """
        Set the min width of the combo box to the maximum of the width of the values

        Returns:
            double  : The min width
        """
        font = self.font()
        fontMetrics = QFontMetrics(font)
        width = 0
        for member in self.enum:
            width = max([width, fontMetrics.width(str(member.name))])
        return width + 35

    def selection(self):
        """
        Returns the member of the enum that was selected
        """
        selectedText = self.currentText()
        for member in self.enum:
            if str(member.name) == selectedText:
                return member

    def setIndexFromValue(self, value):
        """
        Gets a member of the enum and set it selected in the combo box
        """
        self.setCurrentIndex(self.findText(str(value.name)))

    #QSize sizeHint() const override        { return minimumSizeHint(); }
    #QSize minimumSizeHint() const override { return QSize(50, QComboBox::minimumSizeHint().height()); }

    # if __name__ == "__main__":

    #     import sys

    #     app = QApplication(sys.argv)
    #     clock = MyQtEnumComboBox()
    #     clock.show()
    #     sys.exit(app.exec_())
