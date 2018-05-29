# Python Imports

# Thired party imports

# PyQt imports
from PyQt5.QtWidgets import QWidget

# My imports
from ..Utilities.FileUtiles import FileUtiles
from ..UserInterface.Chapter2Normalize.AlgorithmDataDesign import AlgorithmDataDesign
from ..AI.Chapter2Normalize import Normalize
from ..Infrastructure.AlgorithmData import AlgorithmDataInterface


class AlgorithmInput(object):
    """description of class"""

    @staticmethod
    def loadAndNormalize(parentWidget: QWidget, fileName: str, normalizeData: list=None):
        dataMatrix = FileUtiles.load_algorithm_data_from_csv(fileName)
        algorithmDataDesign = AlgorithmDataDesign(parentWidget, dataMatrix, fileName)
        algorithmDataDesign.exec_()
        normalizeData = algorithmDataDesign.normalizeData
        dataMatrix = algorithmDataDesign.dataMatrix
        normalizeDataAsMatrix = []
        for parameterData in normalizeData:
            normalizeDataAsMatrix.append(parameterData.list())
        normalize = Normalize(dataMatrix, normalizeData)
        return normalizeDataAsMatrix, normalizeData, AlgorithmDataInterface(normalize.normalize())
