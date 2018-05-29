"""
Test algorithm for test perposes
"""
from typing import List, Tuple
from .BaseAlgorithm import BaseAlgorithm, QWidget, StdPrm, StdPrmInput
from .BaseAlgorithm import AlgorithmData
from ...Utilities.PythonUtilities import PythonUtilities
from ...UserInterface.Plugins.Widgets.MyQtPlotContainer import PlotHandler
from ...Paths import DATA_PATH


class TestAlgorithm(BaseAlgorithm):
    """
    Test algorithm for test perposes
    """

    def __init__(self, parameters, algorithm_data):
        super(TestAlgorithm, self).__init__(parameters, algorithm_data)
        pass

    @staticmethod
    def prms(widget: QWidget) -> List[StdPrm]:
        """
        Default prms method

        The prms method returns tha parameters used for the algorithm the default
        behavior is to return empty list - There are no parameters

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters
        """
        parameters = []
        parameters.append(
            StdPrm("TA Algorithm def file", "", False, StdPrmInput.button, ["Select algorithm def file"],
                   widget.fileInput, ["Select definitions file", DATA_PATH, "csv file (*.csv)"]))
        plotHandlers = [plotHandler.__name__ for plotHandler in PythonUtilities.inheritors(PlotHandler)]
        parameters.append(
            StdPrm("TA Left Plot Handler", plotHandlers[0], False, StdPrmInput.comboBox, [plotHandlers],
                   widget.selectionChanged, []))
        parameters.append(
            StdPrm("TA Right Plot Handler", plotHandlers[0], False, StdPrmInput.comboBox, [plotHandlers],
                   widget.selectionChanged, []))

        return parameters

    def init(self) -> Tuple[bool, str]:
        """Initialize the algorithm

        Empty init method

        If this method is not implemented by the algorithm a message will appear

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        return True, ""

    def step(self, algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """Perform one step in the algorithm

        Empty step method

        If this method is not implemented by the algorithm a message will apeare

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        return True, ""