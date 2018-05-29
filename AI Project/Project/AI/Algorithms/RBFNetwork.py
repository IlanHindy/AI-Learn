"""
Implement the RBFNetwork algorithm
"""
# python imports
from typing import List, Tuple
import math

# Third party imports
import numpy as np

# My imports
from .BaseAlgorithm import BaseAlgorithm
from .BaseAlgorithm import DistanceMetrics
from .BaseAlgorithm import FieldRolls
from .BaseAlgorithm import LongTermMemory
from .BaseAlgorithm import RowNames, AlgorithmData
from .BaseAlgorithm import ParametersList, StdPrm, StdPrmInput
from .BaseAlgorithm import QWidget


class RBFNetwork(BaseAlgorithm):
    """
    this class implements the RBF network algorithm
    
    # Algorithm Description
    
    ## Perpose
        To implement clustering
    
    ## Algorithm parameters
        -   The number of RBF methods to use
    
    ## Algorithm principals:    
    ### Network building:
    #### Network layers
    -   The first layer is the layer of the parameters
    -   The secod leyer is the layer of the RBF function
    -   The thired layer is the layer of the sums

    #### Network build
    -   There is a connection between each entry from one layer
            to the next
    -   Each such a connection has a coefficient 
    -   The coefficient between the first layer to the second are the b coefficient and 
            a center vector which is called the c coefficient
    -   The coefficient between the second layer to the thired are the a coefficient
    \image html RBFNetwork.jpg

    #### The network formula
    -   The cluster selected is the cluster that has the maximum  \f$\sum_{i=1}^{n} a_ip \|b_i X- c_i \|\f$
        -   X - The input (an observation)
        -   n - The input size
        -   p - An RBF method working on the distance between bX and c \f$p =  e^{ -\|b_iX -c_i  \| } \f$
    
    ## Attributes
    -   algorithm_data  (AlgorithmData)     : holds all the data for processing an algorithm
    -   num_funcs       (int)               : The number of RBF networks
    -   num_groups      (int)               : The number of groups to devide to
    -   num_fields      (int)               : The observation size
    -   ltm             (LongTermMemory)    : All the coefficients 

    
    Args:
        parameters      (ParametersList)    : a list of parameters to the algorithm
        algorithm_data   (AlgorithmData)    : a normalized AlgorithmData
    """

    def __init__(self, parameters: ParametersList, algorithm_data: AlgorithmData):
        super(RBFNetwork, self).__init__(parameters, algorithm_data)

        # Get the number of groups which is the number of possible results
        self.num_groups = len(algorithm_data.resultValues)

        # Get the number of parameters
        self.num_fields = self.algorithm_data[RowNames.Roll, FieldRolls.Parameter].shape[0]

        # Create the long term memory
        self.num_funcs = self.parameters["Number of networks"]["value"]
        self.ltm = LongTermMemory(("a", np.zeros(
            (self.num_funcs, self.num_fields))), ("b", np.zeros((self.num_funcs, self.num_fields))),
                                  ("c", np.zeros((self.num_funcs, self.num_fields))))

        # Create an instance of distance metrix
        self.dist_met = DistanceMetrics()

        #initialize the number of misses to the number of results
        self.num_miss = self.algorithm_data.shape[0]

    @staticmethod
    def prms(widget: QWidget) -> List:
        """Generate parameters list of the algorithm

        The prms method returns the parameters used for the algorithm
    
        This method adds the following parameters:
        -   The number of RBF methods

        Args:
            widget: (QWidget) - The ParametersWidget that will handle the parameters

        Retrns:
            List of parameters to the algorithm
        """
        parameters = []
        parameters.append(
            StdPrm("Number of networks", "", False, StdPrmInput.spinBox, [1], widget.spinValueChanged, []))
        return parameters

    def init(self) -> Tuple[bool, str]:
        """Initialize the algorithm

        Empty init method

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        return True, ""

    def step(self, algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """Perform one step in the algorithm 

        This method implement one step fo the algorithm

        -#  For each observation
            -#  Activate the RBF method on the observation
            -#  The selected group is the one with the maximum result of the RBF   

        Returns:
            bool:   Whether the method succeeded
            str:    Result message
        """
        for input_idx in range(algorithm_data.shape[0]):
            prms = algorithm_data[input_idx, FieldRolls.Parameter]
            rbf_results = np.zeros(self.num_funcs)
            for rbf_idx in range(self.num_funcs):
                rbf_results[rbf_idx] = self.rbf(prms, rbf_idx)
            algorithm_data[input_idx, FieldRolls.StepResult] = rbf_results.argmax()
        return True, ""

    def rbf(self, prms: np.ndarray, rbf_idx: int) -> float:
        """RBF function implementation
        
        The RBF method formula is :\f$\sum_{i=1}^{n} a_ip \|b_i X- c_i \|\f$
        
        Args:
            prms: (np.ndarray) - The observation
            rbf_idx: (int) - The index of the RBF 
        
        Returns:
            float: The result of the RBF 
        """

        r = self.dist_met.euclidean(prms * self.ltm["b"][rbf_idx, :], self.ltm["c"][rbf_idx, :])
        exp = math.expm1(-r**2)
        return np.sum(self.ltm["a"] * exp + 1)
