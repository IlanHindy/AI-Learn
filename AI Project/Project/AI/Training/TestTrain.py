"""
Test training class for training perposes
"""
from .SupervisedTrain import List
from .SupervisedTrain import SupervisedTrain
from .SupervisedTrain import FieldRolls
from .SupervisedTrain import ParametersList
from .SupervisedTrain import AlgorithmData
from .SupervisedTrain import StdPrm, StdPrmInput, ParameterInput, Parameter
from .SupervisedTrain import QWidget
from .SupervisedTrain import DATA_PATH
from .SupervisedTrain import PythonUtilities
from .SupervisedTrain import PlotHandler

class TestTrain(SupervisedTrain):
    """
    Test training class for training perposes
    """
    def __init__(self, parameters, algorithm, algorithm_data):
        super(TestTrain, self).__init__(parameters, algorithm, algorithm_data)

    @staticmethod
    def prms(widget: QWidget):
        """
        Default prms method

        The prms method returns tha parameters used for the algorithm the default
        behavior is to return empty list - There are no parameters

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters
        """
        parameters = SupervisedTrain.prms(widget)
        parameters.append(
            StdPrm("TA Algorithm def file", "", False, ParameterInput.button,
                              ["Select algorithm def file"], widget.fileInput, ["Select definitions file",DATA_PATH, "csv file (*.csv)"]))
        plotHandlers = [
            plotHandler.__name__
            for plotHandler in PythonUtilities.inheritors(PlotHandler)
        ]
        parameters.append(
            StdPrm("TA Left Plot Handler", plotHandlers[0],False,
                              ParameterInput.comboBox, [plotHandlers], widget.selectionChanged, []))
        parameters.append(
            StdPrm("TA Right Plot Handler", plotHandlers[0],False,
                              ParameterInput.comboBox, [plotHandlers], widget.selectionChanged, []))

        return parameters

    def init(self):
        """
        Activate the init method of the algorithm
        """
        return self.algorithm.init()

    def score(self):
        """
        """
        return True, "", 0

    def finished(self, score):
        """
        """
        return True, "", True