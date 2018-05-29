"""
Implement the KMeansClustering algorithm
"""
# python imports
from typing import List, Tuple

# Third party imports
import numpy as np
from scipy.cluster.vq import kmeans2
from sklearn.cluster import KMeans

# My imports
from .BaseAlgorithm import BaseAlgorithm
from .BaseAlgorithm import DistanceMetrics
from .BaseAlgorithm import FieldRolls
from .BaseAlgorithm import AlgorithmData, RowNames, ufunc
from .BaseAlgorithm import ParametersList


class KMeansClustering(BaseAlgorithm):
    """
    This class implements the KMeansClustering algorithm

    # Algorithm Description
    ## Perpose:
        To divide observations to groups
    
    ## Algorithm parameters
        -   The number of groups to divide the observations to
        -   The observations

    ## Algorithm principals:
        -   Each group has a centroid the centroid is a vector with the size of the
            number of the input fields fields
        -   The initiation is to put one observation (randomly selected) as a centroid of each group
        -   The algorithm works in iterations. in each iteration there are 2 steps:
            -   Put each observation at the group which it's centroid is the nearest to 
            -   Calculate the new centroid as the avarage of the members in the group
        -   The algorithm finishes when there are no transfers of observations from one group to another

    ## Attributes
        -   algorithm_data  (AlgorithmData)    : holds all the data for processing an algorithm
        -   finished_alg    (bool)             : whether the algorithm ended
        -   num_groups      (int)              : the number of groups 
        -   numFields       (int)              : the number of fields in each observation
        -   centroids       (num_groups X numFields float matrix)

    Args:
        parameters      (ParametersList)    : a list of parameters to the algorithm
        algorithm_data   (AlgorithmData)    : a normalized AlgorithmData
    """

    def __init__(self, parameters: ParametersList, algorithm_data: AlgorithmData):
        super(KMeansClustering, self).__init__(parameters, algorithm_data)

        # Get the number of groups which is the number of possible results
        self.num_groups = len(algorithm_data.resultValues)

        # Get the number of parameters
        self.num_fields = self.algorithm_data[RowNames.Roll, FieldRolls.Parameter].shape[0]

        # Allocate the centroids
        self.centroids = np.zeros((self.num_groups, self.num_fields))

        # Initialize finished flag
        self.alg_finished = False

    def init(self) -> Tuple[bool, str]:
        """
        Init phase of the algorithm

        Randomly select observations and put them in the centroids  

        Returns:
            bool - Whether the operation succeeded  
            string - A result message string    
       
        """
        # Int the step results column in the algorithm data
        ufunc.fill(self.algorithm_data, FieldRolls.StepResult, -1)

        # Select and fill the centroids
        centroid_idxs = np.random.randint(0, self.algorithm_data.shape[0], self.num_groups).tolist()

        # Create the centroids
        self.centroids = self.algorithm_data[centroid_idxs, FieldRolls.Parameter]

        return True, ""

    def step(self, algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """
        Process a step in the algorithm

        -#   Put each observation in the correct group (The group which it's centroid is neerest to the observation)  
        -#   Calc the new centroid for each group as the avarage of the observations  

        Returns:
            bool - Whether the operation succeeded  
            string - A result message string  
        """
        self.alg_finished = KMeansClustering.find_centroid(self.num_groups, algorithm_data, self.centroids)
        self.calcCentroids()
        return True, ""

    def finished(self, score) -> Tuple[bool, str, bool]:
        """Check if the algorithm finished

        returns the finished_alg flag
       
        Args:
            score: (float) - The score of the last step
        
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            bool:   If the algorithm finished
        """
        return True, "", self.alg_finished

    def score(self) -> Tuple[bool, str, float]:
        """Score the last step results

        Returns the last 
               
        Returns:
            bool:   Whether the method succeeded
            str:    Result message
            float:  The score of the last step
        """
        return True, "", self.evaluation

    @staticmethod
    def find_centroid(num_groups: int, algorithm_data: AlgorithmData, centroids: List[List[int]]) -> bool:
        """
        Find and put each observation in the new group

        This method is used in 2 cases
        -#   At the learning (clustering) phase    
        -#   At the testing phase    

        In each case a different algorithm_data is used  

        Args:  
            num_groups       : (int) - The number of groups in the algorithm  
            algorithm_data	 : (AlgorithmData) - The algorithm_data to process  
            centroids        : (ndarray matrix of float) - The centroids  

        Returns:  
            bool : whether there was a change in the groups   
                
        """
        dist_met = DistanceMetrics()
        finished = True

        # from each observation find the neerest centroid
        for row_idx in range(algorithm_data.shape[0]):
            selected_centroid = -1
            min_dist = float('inf')
            parameters = algorithm_data[row_idx, FieldRolls.Parameter]

            # for each group
            for group_idx in range(num_groups):

                # calc the distance between the observation and the centroid
                dist = dist_met.euclidean(centroids[group_idx], parameters)

                # if the distance is smaller then the previous one set the group
                if (dist < min_dist):
                    min_dist = dist
                    selected_centroid = group_idx

            # After there is a dissition for the observation update set the group and update
            # the finished flag
            if (selected_centroid != algorithm_data[row_idx, FieldRolls.StepResult]):
                finished = False
                algorithm_data[row_idx, FieldRolls.StepResult] = selected_centroid

        return finished

    def calcCentroids(self):
        """
        Calculate the new centroid after each step  

        This method does 2 things:  
        -#   After the groups where constructed calc the new centroid as the avarage of the
            observations in the group  
        -#   Calc the avarage of the distance between the observations and the new centroid
            for presentation perposes         
        """
        dist_met = DistanceMetrics()
        self.evaluation = 0

        # calc the centroid
        for group_idx in range(self.num_groups):

            # Generate a list of rows bellongs to the group
            members = np.where(self.algorithm_data[:, FieldRolls.StepResult] == group_idx)[0]

            # generate a matrix of members X the members parameters
            members_parameters = self.algorithm_data[members.tolist(), FieldRolls.Parameter]

            # calculate the avarage of each parameters and put it in the centroid
            for parameter_idx in range(self.num_fields):
                self.centroids[group_idx, parameter_idx] = np.average(members_parameters[:, parameter_idx])

            # Create a vector holds the distances between the observations and the new centroid
            members_dist = np.zeros(members.shape[0])
            for member_idx in range(members.shape[0]):
                members_dist[member_idx] = dist_met.euclidean(members_parameters[member_idx], self.centroids[group_idx])

            # Calc the avarage of the distances and add it to the evaluation
            self.evaluation += np.average(members_dist)

    @staticmethod
    def create_test_conv(num_groups: int, algorithm_data: AlgorithmData) -> np.ndarray:
        """
        Create conversion between the groups as found in the algorithm and the groups that are in the expected result 

        In order to see if the algorithm is working we have to convert between the groups
        that where used in the algorithm (which where randomly created in the init phase) 
        and the groups used in the result

        The method of the conversion is to see for each group generated by the algorithm, which
        is the group from the result groups that has the largest number of members in the algorithm group

        Args:
            num_groups   : (int) - The number of groups 
            algorithm_data   : (AlgorithmData)   -   The algorithm data

        Returns:
            numpy vector : The convertion method
        
        """

        # The test conv is converting between the number of the group in the centroid
        # (The location in the vector) and the group in the result (the value in the vector)
        test_conv = np.zeros(num_groups)
        for step_group_idx in range(num_groups):

            # Get all the rows with the step_group_idx in the stepResult column
            rows_of_step_group = np.argwhere(
                algorithm_data[:, FieldRolls.StepResult] == step_group_idx).flatten().tolist()

            # Extract from the matrix with the rows with the step_group_idx the column with the result group
            step_group_data = algorithm_data[rows_of_step_group, FieldRolls.ResultPresentation]

            result_group_size = 0

            # Find the result group with the largest number of entries in the vectors
            # This result group is the group that the algorithm claims that is the step group
            for result_group_Idx in range(num_groups):
                num_result_in_group = np.where(step_group_data == result_group_Idx)[0].shape[0]
                if num_result_in_group > result_group_size:
                    result_group_size = num_result_in_group
                    test_conv[step_group_idx] = result_group_Idx

        return test_conv

    def test(self, test_algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """

        test the algorithm results on test data

        -#  Create a conversion table between the groups that the algorithm discovered  
            and the groups in the result  
        -#  Run one cycle of the step of the algorithm to set a group to each one of the observations  
        -#  Convert the groups identified by the previous step to result groups  
        -#  Increase counters according to whether the group discovered by the algorithm is equal  
            to the group in the expected result of the algorithm data  
        
        Args:
            test_algorithm_data	: (AlgorithmData) - an algorithm data with the test data  
        
        Returns:
            success : Wether the operation succeeded  
            string  : A string holds the test results
            bool    : The result of the test    
        
        """
        test_conv = KMeansClustering.create_test_conv(self.num_groups, self.algorithm_data)
        KMeansClustering.find_centroid(self.num_groups, test_algorithm_data, self.centroids)
        return self.test_results(test_conv, test_algorithm_data)

    @staticmethod
    def test_results(test_conv, algorithm_data: AlgorithmData) -> Tuple[bool, str, bool]:
        """
        Generate a test results

        -   For each observation find if the result of the algorithm is equal to the expected result  
        -   Generate and return a result message

        Returns:
            True  
            string  : A string holds the test results      
        """
        # for each row in the test data increase a counter according to whether
        # the result calculated by the algorithm is equal to the expected result
        num_success = 0
        num_field = 0
        for row_idx in range(algorithm_data.shape[0]):
            test_result = test_conv[int(algorithm_data[row_idx, FieldRolls.StepResult])]
            expected_result = algorithm_data[row_idx, FieldRolls.ResultPresentation]
            if test_result == expected_result:
                num_success += 1
            else:
                num_field += 1

        # Generate output message
        num_test = num_field + num_success
        s = "Failed num is " + str(num_field) + " out of " + str(num_test) + " (" + str(
            num_field * 100 / num_test) + "%)\n"
        s += "Success num is " + str(num_success) + " out of " + str(num_test) + " (" + str(
            num_success * 100 / num_test) + "%)"
        return True, s, True

    @staticmethod
    def scipy(algorithm_data: AlgorithmData, test_algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """
        Activate the scipy version of the algorithm

        -#  Extract the parameters from the algorithm_data  
        -#  Calculate the number of the groups  
        -#  The scipy kmeans2 method generates :  
            -#  Centroids  
            -#  A label list (a list of the selected group)    
        -#  The labels are inserted to the algorithm_data  
        -#  Create a conversion between the result of the scipy method and 
            the expected results  
        -#  Calculate the results  

        Args:
            algorithm_data: (AlgorithmData) - The data for learning
            test_algorithm_data: (AlgorithmData) - The data for testing

        Returns:
            success : Wether the operation succeeded  
            string  : A string holds the test results    
        """

        # Create input to the scipy method
        parameters = algorithm_data[:, FieldRolls.Parameter]
        num_groups = len(algorithm_data.resultValues)

        # Activate the scipy method
        centroids, labels = kmeans2(parameters, num_groups)

        # Insert the results to the algorithm_data
        for row_idx in range(labels.shape[0]):
            algorithm_data[row_idx, FieldRolls.StepResult] = labels[row_idx]

        # Create a conversion vector
        test_conv = KMeansClustering.create_test_conv(num_groups, algorithm_data)

        # Perform one step of the algorithm to decide to which group each
        # result belongs
        ufunc.fill(test_algorithm_data, FieldRolls.StepResult, -1)
        KMeansClustering.find_centroid(num_groups, test_algorithm_data, centroids)

        # Test the results
        return KMeansClustering.test_results(test_conv, test_algorithm_data)

    @staticmethod
    def scikitLearn(algorithm_data: AlgorithmData, test_algorithm_data: AlgorithmData) -> Tuple[bool, str]:
        """
        Activate the scikit version of the algorithm

        -#  Extract the parameters from the algorithm_data  
        -#  Calculate the number of the groups  
        -#  The scikitLearn KMeans class has the following attributes :  
            -#  cluster_centers_  
            -#  labels_ a list of the selected group    
        -#  The labels are inserted to the algorithm_data  
        -#  Create a conversion between the result of the scipy method and 
            the expected results  
        -#  Calculate the results  

        Args:
            algorithm_data: (AlgorithmData) - The data for learning
            test_algorithm_data: (AlgorithmData) - The data for testing

        Returns:
            success : Wether the operation succeeded  
            string  : A string holds the test results    
        """

        # Create input to the scipy method
        parameters = algorithm_data[:, FieldRolls.Parameter]
        num_groups = len(algorithm_data.resultValues)

        # Activate the scikit - Learn method
        kmeans = KMeans(n_clusters=num_groups, random_state=0).fit(parameters)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        # Insert the results to the algorithm_data
        for row_idx in range(labels.shape[0]):
            algorithm_data[row_idx, FieldRolls.StepResult] = labels[row_idx]

        # Create a conversion vector
        test_conv = KMeansClustering.create_test_conv(num_groups, algorithm_data)

        # Perform one step of the algorithm to decide to which group each
        # result belongs
        ufunc.fill(test_algorithm_data, FieldRolls.StepResult, -1)
        KMeansClustering.find_centroid(num_groups, test_algorithm_data, centroids)

        # Test the results
        return KMeansClustering.test_results(test_conv, test_algorithm_data)
