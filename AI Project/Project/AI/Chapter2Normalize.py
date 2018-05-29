"""
This module generates a normalized algorithm data
"""
# Python Imports
import math

# Third party imports
import numpy as np

# PyQt imports

# My imports
from ..Infrastructure.AlgorithmData import AlgorithmData, ufunc, RowNames
from ..Infrastructure.Enums import FieldRolls, FieldsTypes, NormalizeRange, NormalizeMethod
from ..UserInterface.Parameter import Parameter


class NormalizeData(Parameter):
    """
    This class holds the data needed to normalize a parameter
    """

    def __init__(self, idx, name):
        super(NormalizeData,
              self).__init__(("fieldName", name), ("roll", FieldRolls.Parameter), ("fieldType", FieldsTypes.RatioData),
                             ("normalizeRange", NormalizeRange.ZeroToOne), ("normalizeMethod",
                                                                            NormalizeMethod.NormalizeToRange),
                             ("valuesOrder", []), ("min", 0), ("max", 0), ("indexInDataFile", idx))




class Normalize(object):
    """
    This class implements normalization
    """

    def __init__(self, inputMatrix, normalizeData):
        """
        Initialize The Normalize class

        Args,
            inputMatrix     , (list)                - the data as read from the file
                                                      Note that the first row should be the name
                                                      of the prms and is not normalized
            normalizeData   , (List(NormalizeData]) - the normalize data for the matrix
        """
        self.inputMatrix = inputMatrix
        self.normalizeData = normalizeData
        self.equilateralEncodingMatrixes = {}

    def normalize(self):
        """
        Normalize a matrix (each column with it's normalize data)

        - For each column call the normalizePrm method which returns AlgorithmData
            - hstack (concatenate horizontally) all the AlgorithmData's

        Returns,
            AlgorithmData , The normalized matrix
        """
        normalizedCol = []
        resultCol = -1
        for col_idx in range(len(self.inputMatrix[0])):
            if self.normalizeData[col_idx]["roll"] == FieldRolls.Result:
                resultCol = col_idx
            col = self.inputMatrix[:, col_idx]
            if self.normalizeData[col_idx]["roll"] in [FieldRolls.Parameter, FieldRolls.Result]:
                normalizedCol.append(self.normalizePrm(col, self.normalizeData[col_idx]))
            else:
                normalizedCol.append(self.createCol(col, self.normalizeData[col_idx]))
        algorithm_data = ufunc.hstack(normalizedCol)

        ufunc.parameters_reduction(algorithm_data)

        if resultCol != -1:
            originalResultsCol = [self.inputMatrix[row_idx][resultCol] for row_idx in range(1, len(self.inputMatrix))]
            ufunc.result_presentation(algorithm_data, originalResultsCol, self.normalizeData[resultCol]["valuesOrder"])
        return algorithm_data

    def createCol(self, col, normalizeData):
        name = np.char.array([normalizeData["fieldName"]])
        data = np.array(col[1:]).astype(float)
        return AlgorithmData(data, name, *self.createHeader(normalizeData, 1))

    def normalizePrm(self, col, normalizeData):
        """
        Normalize one parameter

        For each parameter call the method for normalizing according to
        Normalize method of the parameter

        Args,
            col             , (list)            - The parameter column (data)
            normalizeData   , (NormalizeData)   - holds the data needed for the normalizing

        Returns,
            AlgorithmData   , The normalized column
        """
        if normalizeData["normalizeMethod"] == NormalizeMethod.OneOfN:
            return self.normalize_oneToN(col, normalizeData)
        elif normalizeData["normalizeMethod"] == NormalizeMethod.QualitativeToRange:
            return self. normalize_qualitativeToRange(col, normalizeData)
        elif normalizeData["normalizeMethod"] == NormalizeMethod.EquilateralEncoding:
            return self.normalize_equilateralEncoding(col, normalizeData)
        elif normalizeData["normalizeMethod"] == NormalizeMethod.NormalizeToRange:
            return self.normalize_normalizeToRange(col, normalizeData)
        # NormalizeMethod.ReciprocalNormalization
        return self.normalize_reciprocalNormalization(col, normalizeData)

    def createHeader(self, normalizeData, numCols):
        """
        Creates the header of the AlgorithmData of the column
        """
        rolls = np.array([normalizeData["roll"] for idx in range(numCols)])
        types = np.array([normalizeData["fieldType"] for idx in range(numCols)])
        normalizeMethods = np.array([normalizeData["normalizeMethod"] for idx in range(numCols)])
        if normalizeData["normalizeRange"] == NormalizeRange.ZeroToOne:
            targetMin = np.array([0 for idx in range(numCols)])
        else:
            targetMin = np.array([-1 for idx in range(numCols)])
        targetMax = np.array([1 for idx in range(numCols)])
        mins = np.array([normalizeData["min"] for idx in range(numCols)])
        maxs = np.array([normalizeData["max"] for idx in range(numCols)])
        return rolls, types, normalizeMethods, targetMin, targetMax, mins, maxs

    def resultColumn(self, col, normalizeData):
        return AlgorithmData(col, np.char.array([normalizeData["fieldName"]]), *self.createHeader(normalizeData, 1))

    def normalize_oneToN(self, col, normalizeData):
        """
        Normalize on to N

        Normalize for qualitative parameters

        The input for the normalizing is the value order in which the possible values
        are ordered . For each value we create a list with the length of the values
        order which is filled with 0 ( or -1) and in the location of the value
        we put 1

        Args,
            col             , (list)            - The parameter column (data)
            normalizeData   , (NormalizeData)   - holds the data needed for the normalizing

        Returns,
            AlgorithmData   , The normalized column

        Examples,
            If the values order is ['a','b','c'] and the value is 'b'
            The row for the parameter will be [0,1,0]
        """
        numCols = len(normalizeData["valuesOrder"])
        names = np.char.array(["Is " + valueName for valueName in normalizeData["valuesOrder"]])
        if normalizeData["normalizeRange"] == NormalizeRange.ZeroToOne:
            initData = [0 for idx in range(numCols)]
        else:
            initData = [-1 for idx in range(numCols)]
        data = []
        for prm in col[1:]:
            row = list(initData)
            row[normalizeData["valuesOrder"].index(prm)] = 1
            data.append(row)
        return AlgorithmData(np.array(data), names, *self.createHeader(normalizeData, numCols))

    def normalize_equilateralEncoding(self, col, normalizeData):
        """
        Normalize equilateral encoding

        Normalize for qualitative encoding

        In order to create equilateral encoding one has to create
        a matrix size (num of possible values X num of possible values - 1)
        This is done using the createEquilateralMatrix method

        Then for each parameter in the column the following is done
        -# Get the index of the value in the values order list
        -# Add the line in the matrix with the row index equal to the index of the value

        In order to avoid recalculating the matrixes, the matrixes are kept in a dictionary
        in which the key is the number of possible values and the value is the matrix.
        Only if the matrix from the rank was not calculated it is calculated else it is
        taken from the dictionary

        Args,
            col             , (list)            - The parameter column (data)
            normalizeData   , (NormalizeData)   - holds the data needed for the normalizing

        Returns,
            AlgorithmData   , The normalized column
        """
        numCols = len(normalizeData["valuesOrder"]) - 1
        names = np.char.array([normalizeData["fieldName"] + "#" + str(idx) for idx in range(numCols)])
        if numCols not in self.equilateralEncodingMatrixes.keys():
            #     equilateralEncodingMatrix = self.equilateralEncodingMatrixes[numCols]
            # else,
            self.equilateralEncodingMatrixes[numCols + 1] = self.createEquilateralMatrix(numCols + 1)

        data = []
        for prm in col[1:]:            
            row = self.equilateralEncodingMatrixes[numCols + 1][ufunc.index(normalizeData["valuesOrder"], prm)]                
            data.append(row)
           
        return AlgorithmData(np.array(data), names, *self.createHeader(normalizeData, numCols))

    def  normalize_qualitativeToRange(self, col, normalizeData):
        """
        Normalize qualitative to range

        Normalize to qualitative encoding  

        -# Give a integer for each value according to it's index in the values order
        -# Normalize from the range [0, number of values - 1] to the range [0,1] or [-1,1]

        Args,
            col             , (list)            - The parameter column (data)
            normalizeData   , (NormalizeData)   - holds the data needed for the normalizing

        Returns,
            AlgorithmData   , The normalized column
        """
        name = np.char.array([normalizeData["fieldName"]])
        data = np.array([float(normalizeData["valuesOrder"].index(col[idx])) for idx in range(1, len(col))])
        algorithm_data = AlgorithmData(data, name, *self.createHeader(normalizeData, 1))
        return self.transferToRange(algorithm_data)

    def normalize_normalizeToRange(self, col, normalizeData):
        """
        Normalize from real world range to [0,1] or [-1,1]

        Normalize for quantitative values

        -#  Create an AlgorithmData
        -# Normalize the values

        Args,
            col             , (list)            - The parameter column (data)
            normalizeData   , (NormalizeData)   - holds the data needed for the normalizing

        Returns,
            AlgorithmData   , The normalized column
        """
        name = np.char.array([normalizeData["fieldName"]])
        data = np.array([float(col[idx]) for idx in range(1, len(col))])
        algorithm_data = AlgorithmData(data, name, *self.createHeader(normalizeData, 1))
        return self.transferToRange(algorithm_data)

    def normalize_reciprocalNormalization(self, col, normalizeData):
        """
        Reciprocal Normalization

        Normalize for qualitative values

        -# The normalized value is 1/value
        Args,
            col             , (list)            - The parameter column (data)
            normalizeData   , (NormalizeData)   - holds the data needed for the normalizing

        Returns,
            AlgorithmData   , The normalized column
        """
        name = np.char.array([normalizeData[normalizeData["fieldName"]]])
        data = np.array([1 / float(col[idx]) for idx in range(1, len(col))])
        return AlgorithmData(data, name, *self.createHeader(normalizeData, 1))

    def transferToRange(self, algorithm_data):
        """
        Transfer value from real world range to normalized range

        The ranges are specified in the NormalizedData and inserted to the AlgorithmData which is
        the parameter for this method

        Args,
            algorithm_data    , (AlgorithmData)   - The algorithm_data to normalize

        Returns,
            AlgorithmData   , The normalized column
        """
        for col_idx in range(algorithm_data.shape[1]):
            colMin = algorithm_data[RowNames.Min, col_idx]
            colMax = algorithm_data[RowNames.Max, col_idx]
            targetMin = algorithm_data[RowNames.MinTarget, col_idx]
            targetMax = algorithm_data[RowNames.MaxTarget, col_idx]
            if colMin == colMax:
                for row_idx in range(len(algorithm_data)):
                    algorithm_data[row_idx, col_idx] = targetMin
            else:
                for row_idx in range(len(algorithm_data)):
                    algorithm_data[row_idx, col_idx] = (
                        (targetMax - targetMin) *
                        (algorithm_data[row_idx, col_idx] - colMin)) / (colMax - colMin) + targetMin
        return algorithm_data

    def createEquilateralMatrix(self, n):
        """
        Create an Equilateral matrix
        Args,
            n , (int)  - The number of values that the matrix is for

        Returns,
            List[List{float]]   , The equilateral matrix
        """

        result = [[0 for i in range(n - 1)] for j in range(n)]
        result[0][0] = -1
        result[1][0] = 1.0
        for k in range(2, n):
            r = k
            f = math.sqrt(r * r - 1.0) / r
            for i in range(k):
                for j in range(k - 1):
                    result[i][j] *= f

            r = -1.0 / r
            for i in range(k):
                result[i][k - 1] = r

            result[k][k - 1] = 1.0

        return result
