# Python Imports
import sys

# Third party imports
# PyQt imports

import qdarkstyle
from PyQt5.QtWidgets import QApplication

# My imports
from Project.Paths import *
from Project.UserInterface.MainWindow import MainWindow
from Project.Utilities.PythonTools import PythonTools

#if __name__ == "__main__":
try:
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    #mainWindow.print()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow.show()
    sys.exit(app.exec_())
except:
    PythonTools.printException("")
