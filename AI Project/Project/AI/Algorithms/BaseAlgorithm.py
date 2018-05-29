"""
Hold Base class for algorithms
"""
# Python imports
from typing import List, Tuple
import math

# PyQt imports
# from PyQt5.QtCore import
from PyQt5.QtWidgets import QWidget

# My imports
from ..Chapter3DistanceMetrics import DistanceMetrics
from ...Infrastructure.Enums import FieldRolls, FieldsTypes
from ...Infrastructure.AlgorithmData import RowNames, AlgorithmData, ufunc
from ...Infrastructure.LongTermMemory import LongTermMemory
from ...UserInterface.Parameter import StdPrm, StdPrmInput
from ...UserInterface.Plugins.Widgets.ParametersWidget import ParametersList


class BaseAlgorithm(object):
    """
    Base class for all the algorithms  

    -   holds common methods for all the algorithms  
    -   holds common attributes for all the algorithms

    Args:
        parameters: (ParametersList) - A list of parameters to be used by the algorithm
        algorithm_data: (AlgorithmData) - The algorithm data
    """

    def __init__(self, parameters: ParametersList, algorithm_data: AlgorithmData):
        self.parameters = parameters
        self.algorithm_data = algorithm_data
        self.ltm = LongTermMemory()
        self.alg_finished = False

    @staticmethod
    def prms(widget: QWidget) -> List:
        """Generate parameters list of the algorithm

        Default prms method

        The prms method returns the parameters used for the algorithm the default
        behavior is to return empty list - There are no parameters

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters

        Retrns:
            List of parameters to the algorithm
        """
        return []

    def init(self) -> Tuple[bool, str]:
        """Initialize the algorithm

        Default init method

        If this method is not implemented by the algorithm a message will appear

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        return False, "The init method of the algorithm should be implemented"

    def step(self, algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """Perform one step in the algorithm

        Default step method

        If this method is not implemented by the algorithm a message will apeare

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        return False, "The step method of the algorithm should be implemented"

    def finished(self, score: float) -> Tuple[bool, str, bool]:
        """Check if the algorithm finished

        Default finish method

        If this method is not implemented by the algorithm a message will apear       
               
        Args:
            score: (float) - The score of the last step
        
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   If the algorithm finished
        """

        return False, "The finish method of the algorithm should be implemented", False

    def score(self) -> Tuple[bool, str, float]:
        """Score the last step results

        Default score method

        If this method is not implemented by the algorithm a message will apear           
               
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            float:  The score of the last step
        """

        return False, "The score method of the algorithm should be implemented", 0

    def check(self) -> Tuple[bool, str, bool]:
        """Checks the results of a test

        Default score method

        If this method is not implemented by the algorithm a message will apear  
        
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   The results of the test
        """
        return False, "The check method of the algorithm should be implemented", False

    def test(self, test_algorithm_data) -> Tuple[bool, str, bool]:
        """Tests the results of the algorithm

        Default test method

        If this method is not implemented by the algorithm a message will appear

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   The results of testing the operation
        """
        return False, "The test method of the algorithm should be implemented", False

    @staticmethod
    def scipy(algorithm_data, test_algorithm_data) -> Tuple[bool, str, bool]:
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
        return False, "The scipy method of the algorithm is not implemented", False

    @staticmethod
    def scikitLearn(algorithm_data, test_algorithm_data) -> Tuple[bool, str]:
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
        return False, False, "The scikitLearn method of the algorithm is not implemented"
