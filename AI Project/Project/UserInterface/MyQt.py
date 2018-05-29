# Python Imports

# Thired party imports

# PyQt imports
from PyQt5.QtCore import Qt, QVariant, QAbstractTableModel
from PyQt5.QtWidgets import QPushButton, QSizePolicy
#from PyQt5.QtGui import

# My imports
# import ArtificialIntelligence
from ..Infrastructure.AlgorithmData import AlgorithmData


class MyQtTableModel(QAbstractTableModel):
    """ Q table model that supports AlgorithmDataInterface """

    def __init__(self, matrix, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.matrix = matrix

    def setData(self, matrix):
        # self.checkMatrixes(matrixes)
        self.matrix = matrix
        self.dataChanged.emit(
            self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)), [Qt.EditRole])
        self.layoutChanged.emit()
        return True

    def rowCount(self, parent):
        # if isinstance(self.matrix, AlgorithmDataInterface):
        #    return self.matrix.rowCount()
        # else:
        return len(self.matrix)

    def columnCount(self, parent):
        # if isinstance(self.matrix, AlgorithmDataInterface):
        #    return self.matrix.columnCount()
        # else:
        return len(self.matrix[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        return QVariant(str(self.matrix[index.row()][index.column()]))


class MyQtAlignButton(QPushButton):
    #def __init__(self, parent, setMethod, alignment, text):
    def __init__(self, parent, text):
        super(MyQtAlignButton, self).__init__(parent)
        #self.alignment = alignment
        #self.parent = parent
        self.setText(text)
        #setMethod(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #    self.clicked.connect(self.button_clicked)
    #    self.label()

    #def button_clicked(self):
    #    self.alignment = Qt.AlignCenter
    #    self.parent.layout().setAlignment(self, self.alignment)
    #    self.label()

    #def label(self):
    #    self.setText("Alignmrnt = " + str(self.alignment))

    #app = QApplication(sys.argv)
    #window = QWidget()
    #layout = QGridLayout(window)
    #layout.addWidget(MyQtAlignButton(window, Qt.AlignCenter), 0, 0);
    #layout.addWidget(MyQtAlignButton(window, Qt.AlignCenter), 1, 0, Qt.AlignCenter);
    #window.setMinimumSize(500, 200);
    #window.show();
    #app.exec();
