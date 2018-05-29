print ("In artificial line 1")
print ("In artificial line 2")
print ("In artificial line 3")
# Python Imports
#import sys

# Thired party imports
# PyQt imports

import qdarkstyle
from PyQt5.QtWidgets import QApplication

# My imports
from .Paths import *
from .UserInterface.MainWindow import MainWindow
from .Utilities.PythonTools import PythonTools

#if __name__ == "__main__":
try:
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow.show()
    sys.exit(app.exec_())
except:
    PythonTools.printException("")
