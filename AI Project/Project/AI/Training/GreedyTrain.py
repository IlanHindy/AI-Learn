"""
Hold Base class for greedy training

"""
# Python imports
import math
from typing import ClassVar, Tuple
import numpy as np
from .SupervisedTrain import List
from .SupervisedTrain import SupervisedTrain
from .SupervisedTrain import FieldRolls
from .SupervisedTrain import ParametersList
from .SupervisedTrain import AlgorithmData
from .SupervisedTrain import StdPrmInput, StdPrm
from .SupervisedTrain import QWidget
from .SupervisedTrain import DATA_PATH
from .SupervisedTrain import PythonUtilities
from .SupervisedTrain import PlotHandler



class GreedyTrain(SupervisedTrain):
    """
    Greedy train
    
    # Algorithm Description
    
    ## Perpose
    To activate greedy train on algorithms
    
    ## Algorithm parameters
    -   Allowed percent of wrong answers

    
    ## Algorithm principals:
    -   At the beginning of each step a insert random values to all the 
        Long term memory
    -   Perform a step get the score. if the score is better keep
        the long term memory. Else stay with the previouse Long Term Memory
    
    ## Attributes
    -   algorithm   (Inherits from BaseAlgorithm) - The algorithm object
    -   algorithm_data  (AlgorithmData) - The data of the algorithm
    -   parameters  (ParametersList) - A list of parameters for the train
    -   best_score  (float) - The best score achived so far
    
    Args:
        parameters: (ParametersList) - A list of parameters to be used by the algorithm
        algorithm:  (ClassVar) - The algorithm object
        algorithm_data: (AlgorithmData) - The algorithm data
    """

    def __init__(self, parameters: ParametersList, algorithm: ClassVar, algorithm_data: AlgorithmData):
        """ __init__ method
        
        Calls the __init__ method of SupervisedTrain
        """
        super(GreedyTrain, self).__init__(parameters, algorithm, algorithm_data)

    @staticmethod
    def prms(widget: QWidget) -> List:
        """Generate parameters list of the trainings

        Gets the parameters of SupervisedTrain

        Add to these parameters the max miss parameter

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters
        """
        parameters = SupervisedTrain.prms(widget)

        parameters.append(
            StdPrm("max miss", "", False, StdPrmInput.spinBox, [10],
                   widget.spinValueChanged, []))
        return parameters

    def init(self) -> Tuple[bool, str]:
        """Initialize the training

        Set the long term memory and call the init method of the algorithm

        If this method is not implemented by the training a message will appear

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        self.change_ltm()
        return self.algorithm.init()

    def change_ltm(self) -> Tuple[bool, str]:
        """Create a new long term memory
        The policy of the greedy train is to create a random values to all 
        the Long Term Memory

        The Long Term Memory is a dictionary of np.ndarrys
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
        """
        for key in self.algorithm.ltm.keys():
            self.algorithm.ltm[key] = np.random.rand(*self.algorithm.ltm[key].shape)
        return True, ""
        
    def score(self) -> Tuple[bool, str, float]:
        """Scores the result of a step performed by the algorithm
        
        -   Compare the StepResults and the ResultPresentation and get the number of wrong values
        -   Get the percent of these values
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
            float:  The score
        """

        num_miss = np.sum(self.algorithm_data[:,FieldRolls.StepResult] != self.algorithm_data[:,FieldRolls.ResultPresentation])
        num_miss_perc = num_miss * 100/self.algorithm_data.shape[0]
        return True, "", num_miss_perc

    def finished(self, score) -> Tuple[bool, str, bool]:
        """Check if the algorithm study ended
        Decide if the study finished

        The study finished if the score (which is the percent of missed) is less then the 
        the algorithm parameter
        
        Args:
            score (float): The percent of the wrong results
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
            bool:   If the study finished
        """
        finish_level = self.parameters["max miss"]["value"]
        return True,  "", score < finish_level

    def check(self, algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """Check if the test passed
        
        The test passed if the percent of wrong answers is less the parameter
        of the algorithm
        
        Args:
            algorithm_data (AlgorithmData): the test algorithm data
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
            bool:   Whether the test succeeded
        """

        num_miss = np.sum(self.algorithm_data[:,FieldRolls.StepResult] != self.algorithm_data[:,FieldRolls.ResultPresentation])
        num_miss_perc = num_miss * 100/algorithm_data.shape[0]
        finish_level = self.parameters["max miss"]["value"]
        result_str = str(num_miss) + " out of " + str(algorithm_data.shape[0]) + " (" + str(num_miss_perc) + "% < " + str(finish_level) + "%)"
        return True, result_str, num_miss_perc < finish_level
    