"""
Class for un supervised training

Basically in unsupervised training there are the same steps as supervised
training but all the work is done by the algorithm
"""
# My imports
from ..Algorithms import BaseAlgorithm
from .BaseTrain import BaseTrain, Tuple, ClassVar, AlgorithmData, ParametersList


class UnSupervisedTrain(BaseTrain):
    """
    Class for unsupervised training

    Basically in unsupervised training there are the same steps as supervised
    training but all the work is done by the algorithm
   
    Args:
        parameters: (ParametersList) - A list of parameters to be used by the training
        algorithm: (Algorithm Object) - An object of the algorithm to run
        algorithm_data: (AlgorithmData) - The data of the algorithm
    """
    def __init__(self, parameters: ParametersList, algorithm: ClassVar, algorithm_data: AlgorithmData):
        super(UnSupervisedTrain, self).__init__(parameters, algorithm,
                                                algorithm_data)

    def init(self) -> Tuple[bool, str]:
        """
        Activate the init method of the algorithm

        Returns:
            bool - Whether the method succeeded
            str  - Error message
        """
        return self.algorithm.init()

    def step(self) -> Tuple[bool, str, bool, bool]:
        """ Perform a step of the algorithm
        
        -   Step :
            -   Perform a step of the algorithm
            -   Score the results of the step using the algorithm's method
            -   Check if the algorithm finished using the algorithm's method
        
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   If the algorithm generated a new (better) score
            bool:   If the algorithm finished
        """
        success, message = self.algorithm.step(self.algorithm_data)
        if not success:
            return False, message, 0, False

        success, message, score = self.algorithm.score()
        if not success:
            return False, message, 0, False

        self.algorithm_data.evaluations.append(score)

        success, message, finished = self.algorithm.finished(score)
        if not success:
            return False, message, 0, False
        
        return True, "Score is " + str(score), True, finished

        
    def check(self) -> Tuple[bool, str]:
        """
        Activate the check method of the algorithm

        Returns:
            bool - Whether the method succeeded
            str  - Error message
        """
        return self.algorithm.check()

    def test(self, test_algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """
        Activate the test method of the algorithm

        Args:
            algorithm_data: (AlgorithmData) - The data for learning

        Returns:
            bool - Whether the method succeeded
            str  - Error message
        """
        return self.algorithm.test(test_algorithm_data)

    @staticmethod
    def scipy(algorithm, algorithm_data, test_algorithm_data) -> Tuple[bool, str]:
        """
        Activate the scipy method of the algorithm

        Args:
            algorithm_data: (AlgorithmData) - The data for learning
            test_algorithm_data: (AlgorithmData) - The data for testing

        Returns:
            bool - Whether the method succeeded
            str  - Error message
        """
        try:
            return algorithm.scipy(algorithm_data, test_algorithm_data)
        except Exception as e:
            return False, "The scipy version of the algorithm failed. \nThe error message is: " + str(
                e), False

    @staticmethod
    def scikitLearn(algorithm, algorithm_data, test_algorithm_data) -> Tuple[bool, str]:
        """
        Activate the scikitLearn method of the algorithm

        Args:
            algorithm_data: (AlgorithmData) - The data for learning
            test_algorithm_data: (AlgorithmData) - The data for testing

        Returns:
            bool - Whether the method succeeded
            str  - Error message
        """
        try:
            return algorithm.scikitLearn(algorithm_data, test_algorithm_data)
        except Exception as e:
            return False, "The scilit-Learn vertion of the algorithm failed. \nThe error message is: " + str(
                e), False
