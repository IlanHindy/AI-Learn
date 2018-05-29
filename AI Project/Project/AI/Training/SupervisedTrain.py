"""Supervised train base

Supervised train base

"""

#Python imports
from typing import ClassVar, Tuple, List
import numpy as np

# PyQt imports
from PyQt5.QtWidgets import QWidget

# My imports
from .BaseTrain import BaseTrain
from .BaseTrain import FieldRolls
from .BaseTrain import ParametersList, ParameterInput
from .BaseTrain import AlgorithmData
from .BaseTrain import StdPrm, StdPrmInput, Parameter, ParameterInput
from .BaseTrain import QWidget
from .BaseTrain import DATA_PATH
from .BaseTrain import PythonUtilities
from .BaseTrain import PlotHandler


class SupervisedTrain(BaseTrain):
    """
    Supervised Train base class
    
    # Algorithm Description
    
    ## Perpose
    Perform supervised train.
    
    ## Parameters
    
    ## Principals:
    -   A supervised train is an environment for a study of an algorithm
    -   The training works in the following algorithm
        -   Init - activate the init method of the algorithm
        -   Step :
            -   Change the long term memory according to the policy of the train
            -   Perform a step of the algorithm
            -   Score the results of the step
            -   Check if the algorithm finished
    -   Test the result on another data   
    
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
        
        Calls the __init__ method of BaseTrain
        """

        super(SupervisedTrain, self).__init__(parameters, algorithm, algorithm_data)
        self.best_score = np.inf

    @staticmethod
    def prms(widget: QWidget) -> List:
        """Generate parameters list of the trainings

        Gets the parameters of BaseTrain

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters
        """
        parameters = BaseTrain.prms(widget)
        return parameters

    def step(self) -> Tuple[bool, str, bool, bool]:
        """ Perform a step of the algorithm
        
        -   Step :
            -   Change the long term memory according to the policy of the train
            -   Perform a step of the algorithm
            -   Score the results of the step
            -   Check if the algorithm finished
        
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   If the algorithm generated a new (better) score
            bool:   If the algorithm finished
        """

        self.algorithm.ltm.clone()
        self.change_ltm()

        success, message = self.algorithm.step(self.algorithm_data)
        if not success:
            return False, message, 0, False

        success, message, score = self.score()
        if not success:
            return False, message, 0, False

        if score < self.best_score:
            success, message, finished = self.finished(score)
            if not success:
                return False, message, 0, False

            message = "Score changed from " + str(self.best_score) + " to " + str(score)
            self.best_score = score
            self.algorithm_data.evaluations.append(score)
            return True, message, True, finished
        else:
            message = "The score did not change it is " + str(self.best_score) + " The step score is " + str(score)
            self.algorithm.ltm.reverse()
            score = self.best_score
            self.algorithm_data.evaluations.append(score)
            return True, message, False, False

    def test(self, test_algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """Tests the results of the algorithm

        Perform a test on test data with the long term memory achived in the
        srudy and check if it received the requested results

        If this method is not implemented by the training a message will appear

        Args:
            test_algorithm_data (AlgorithmData) - The data for the test

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   The results of testing the operation
        """
        success, message = self.algorithm.step(test_algorithm_data)
        if not success:
            return False, message, False, False

        success, message, result = self.check(test_algorithm_data)
        if not success:
            return False, message, False, False

        return True, message, result

    def check(self, algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """Check if the test passed
        
        This method has to be implemented by the inherrited class
        
        Args:
            algorithm_data (AlgorithmData): the test algorithm data
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
            bool:   Whether the test succeeded
        """

        return False, False, "The check method of the training class has to be implemented"

    def change_ltm(self) -> Tuple[bool, str]:
        """Create a new long term memory
        
        This method has to be created by the inheritted class

        This method actually implement the plolicy of the training
        (how new long term memory is generated)
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
        """

        return False, "The change_ltm method of the training class has to be implemented"

    def score(self) -> Tuple[bool, str, float]:
        """Scores the result of a step performed by the algorithm
        
        This method has to be created by the inheritted class
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
            float:  The score
        """
        return False, "The score method of the training class has to be implemented", 0

    def finished(self, score: float) -> Tuple[bool, str, bool]:
        """Check if the algorithm study ended
        
        This method has to be created by the inheritted class
        
        Args:
            score (float): [description]
        
        Returns:
            bool:   If the method succeeded
            str:    The finish message
            bool:   If the study finished
        """

        return False, "The finished method of the training class has to be implemented", False
