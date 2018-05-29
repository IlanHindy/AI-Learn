""" Distance Metrics

    This module implements distance metrics methods between
    2 vectors
"""
# Python Imports
import math
from typing import List, Union

# Third party imports
import numpy as np

# PyQt imports

# My imports
from ..Infrastructure.AlgorithmData import AlgorithmData
from ..AI.Chapter2Normalize import NormalizeData, Normalize
from ..Infrastructure.Enums import FieldsTypes, NormalizeRange, NormalizeMethod


class DistanceMetrics(object):
    """ Distance Metrics 

        This class implements 3 types of distance metrics between 2 vectors:
        -#  Euclidean distance metrics
        -#  Manhattan distance metrics
        -#  Chebyshave distance metrics

        The distance metrics is done between 2 AlgorithmData. at the beginning of the distance
        metrics methods there is a conversion to AlgorithmData

    """

    def euclidean(self, p, q):
        """ Euclidean distance metrics

            The calculation formula is:
            \f$\sqrt{\sum_{i=0}^n (p_i-q_i)^2}\f$.

        """
        p = AlgorithmData(p)
        q = AlgorithmData(q)

        sum = 0
        for i in range(p.shape[0]):
            sum += math.pow((p[i, 0] - q[i, 0]), 2)
        sum = math.sqrt(sum)
        return sum

    def manhattan(self, p: Union[AlgorithmData, List[float]], q: Union[AlgorithmData, List[float]]):
        """ Manhatten distance metrics

            The calculation formula is:
            \f$\sum_{i=0}^n |(p_i-q_i|\f$.
        """
        p = AlgorithmData(p)
        q = AlgorithmData(q)
        sum = 0
        for i in range(p.shape[0]):
            sum += abs(p[i, 0] - q[i, 0])
        return sum

    def chebyshave(self, p: Union[AlgorithmData, List[float]], q: Union[AlgorithmData, List[float]]):
        """ Chevichase distance metrics

            The calculation formula is:
             \f$ max|p_i-q_i|\f$.
        """

        p = AlgorithmData(p)
        q = AlgorithmData(q)
        sum = 0
        for i in range(p.shape[0]):
            sum = max(sum, abs(p[i, 0] - q[i, 0]))
        return sum

    def select(self, prmOptions: List[List[str]], options: List[List[int]], itemToFind: List):

        # Create the normalize data matrix
        normalizeDataMatrix = []
        for prmIdx in range(len(prmOptions)):
            normalizeData = NormalizeData(prmIdx, "Prm" + str(prmIdx))
            normalizeData["fieldName"] = "Prm" + str(prmIdx)
            normalizeData["fieldType"] = FieldsTypes.NominalData
            normalizeData["normalizeMethod"] = NormalizeMethod.EquilateralEncoding
            normalizeData["max"] = len(prmOptions[prmIdx])
            normalizeData["min"] = 0
            normalizeData["normalizeRange"] = NormalizeRange.ZeroToOne
            normalizeData["valuesOrder"] = [value for value in prmOptions[prmIdx]]
            normalizeData["indexInDataFile"] = prmIdx
            normalizeDataMatrix.append(normalizeData)

        # In order to use the normalize method we have to simulate like it came from
        # a file which means :
        # 1. each field has a header
        # 2. The values are strings

        # Handle the options matrix
        options = [[str(entry) for entry in row] for row in options]
        prmNameRow = ["prm" + str(idx) for idx in range(len(options[0]))]
        options.insert(0, prmNameRow)
        options = np.array(options)

        # Convert the itemToFind to a matrix with name row
        itemToFind = [str(entry) for entry in itemToFind]
        itemToFind = [prmNameRow, itemToFind]
        itemToFind = np.array(itemToFind)

        normalizeObject = Normalize(options, normalizeDataMatrix)
        optionsNormalized = normalizeObject.normalize()

        normalizeObject = Normalize(itemToFind, normalizeDataMatrix)
        itemNormalized = normalizeObject.normalize()

        bestDist = float("inf")
        for optionIdx in range(len(optionsNormalized)):
            option = optionsNormalized.rows([optionIdx])
            dist = self.euclidean(option, itemNormalized)
            if dist < bestDist:
                selectedOption = optionIdx
                bestDist = dist

        return selectedOption
