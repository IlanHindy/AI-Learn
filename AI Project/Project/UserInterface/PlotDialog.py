# Python Imports
# Third party imports
# PyQt imports
from PyQt5.QtWidgets import QDialog

# My imports
from ..UserInterface.Plugins.Widgets.MyQtPlotContainer import MyQtPlotContainer, PlotHandlerExample
from ..PyUi.Ui_PlotDialog import Ui_PlotDialog


class PlotDialog(QDialog, Ui_PlotDialog):
    """description of class"""

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        #self.myQtPlotContainer.init(PlotHandlerExample())
