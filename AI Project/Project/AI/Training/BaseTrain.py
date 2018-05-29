"""
Hold Base class for training

"""

# Python imports
from typing import ClassVar, Tuple, List
import numpy as np

# PyQt imports
from PyQt5.QtWidgets import QWidget

# My imports
from ..Algorithms.BaseAlgorithm import BaseAlgorithm
from ...UserInterface.Parameter import StdPrm, StdPrmInput, Parameter, ParameterInput
from ...UserInterface.Plugins.Widgets.ParametersWidget import ParametersList
from ...Infrastructure.AlgorithmData import AlgorithmData
from ...Infrastructure.Enums import FieldRolls
from ...Utilities.PythonUtilities import PythonUtilities
from ...UserInterface.Plugins.Widgets.MyQtPlotContainer import PlotHandler
from ...Paths import DATA_PATH


class BaseTrain(object):
    """
    Base class for all the training  

    -   holds common methods for all the trainings  
    -   holds common attributes for all the trainings

    Args:
        parameters: (ParametersList) - A list of parameters to be used by the algorithm
        algorithm:  (ClassVar) - The algorithm object
        algorithm_data: (AlgorithmData) - The algorithm data
    """

    def __init__(self, parameters: ParametersList, algorithm: ClassVar, algorithm_data: AlgorithmData):
        self.algorithm = algorithm
        self.parameters = parameters
        self.algorithm_data = algorithm_data

    @staticmethod
    def prms(widget: QWidget) -> List:
        """Generate parameters list of the trainings

        Default prms method

        The prms method returns the parameters used for the algorithm the default
        behavior is to return empty list - There are no parameters

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters
        """
        return []

    def init(self) -> Tuple[bool, str]:
        """Initialize the training

        Default init method

        If this method is not implemented by the training a message will appear

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        return False, "The init method of the training class should be implemented"

    def step(self) -> Tuple[bool, str, bool, bool]:
        """Perform one step in the training

        Default step method

        If this method is not implemented by the training a message will apeare

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   If the algorithm generated a new (better) score
            bool:   If the algorithm finished
        """       
        return True, "The step method of the training class should be implemented", False, False

    def test(self, test_algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """Tests the results of the algorithm

        Default test method

        If this method is not implemented by the training a message will appear

        Args:
            test_algorithm_data (AlgorithmData) - The data for the test

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   The results of testing the operation
        """
        return False, "The test method of the training class should be implemented", False

    @staticmethod
    def scipy(algorithm, algorithm_data: AlgorithmData, test_algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """Activate the scipy version of the algorithm

        Default scipy method

        If this method is not implemented by the algorithm a message will appear

        Args:
            algorithm_data: (AlgorithmData) - The data for learning
            test_algorithm_data: (AlgorithmData) - The data for testing

        Returns:
             bool:   Whether the method succeeded
             str:    Result message
             bool:   The results of testing the operation
        """
        return False, "The scipy method of the training class should be implemented", False

    @staticmethod
    def scikitLearn(algorithm, algorithm_data: AlgorithmData, test_algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """Activate the scikitLear implementation of the algorithm

        Default scikit method

        If this method is not implemented by the algorithm a message will appear

        Args:
            algorithm_data: (AlgorithmData) - The data for learning
            test_algorithm_data: (AlgorithmData) - The data for testing

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   The results of testing the operation
        """
        return False, "The scikitLearn method of the training class should be implemented", False

    