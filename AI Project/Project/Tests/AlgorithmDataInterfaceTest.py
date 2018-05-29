# Python Imports
import sys
import os

# Third party imports
import numpy as np

# PyQt imports

# My imports
from ..Infrastructure.AlgorithmData import AlgorithmData, AlgorithmDataInterface, ufunc, RowNames
from ..Infrastructure.Enums import FieldRolls, FieldsTypes, NormalizeMethod
from ..Tests.TestBase import TestBase


class AlgorithmDataInterfaceTest(TestBase):
    """description of class"""

    def __init__(self, parentWindow):
        super(AlgorithmDataInterfaceTest, self).__init__(parentWindow)
        self.addTest("Check __init__")
        self.addTest(self.check_init_from_np)
        self.addTest(self.check_init_with_none_header)
        self.addTest(self.check_init_vector)
        self.addTest(self.check_init_from_np_matrix)
        self.addTest(self.check_init_from_np_ndarray_2_dim)
        self.addTest(self.check_init_from_np_ndarray_1_dim)
        self.addTest(self.check_init_from_list_2_dim)
        self.addTest(self.check_init_from_list_1_dim)
        self.addTest(self.check_init_from_list_mixed_dim)
        self.addTest("Check __getItem__")
        self.addTest(self.check_getitem_roll)
        self.addTest(self.check_getitem_row)
        self.addTest(self.check_getitem_header_row)
        self.addTest("Check __setitem__")
        self.addTest(self.check_setitem_in_header_and_data_success)
        self.addTest(self.check_setitem_in_header_and_data_failure)
        self.addTest(self.check_setitem_in_header_and_index_failure)
        self.addTest(self.check_setitem_in_vectors)
        self.addTest(self.check_setitem_in_names_col_failure)
        self.addTest("Check ufuncs")
        self.addTest(self.check_hstack_2_matrix)
        self.addTest(self.check_hstack_2_arrays)
        self.addTest(self.check_hstack_array_and_matrix)
        self.addTest("Check cols, rows")
        self.addTest(self.check_cols_one_index)
        self.addTest(self.check_cols_one_name)
        self.addTest(self.check_cols_some_indexes)
        self.addTest(self.check_cols_some_names)
        self.addTest(self.check_cols_mixed_indexes_and_names)
        self.addTest(self.check_cols_one_roll)
        self.addTest(self.check_cols_some_roll)
        self.addTest(self.check_rows)

    def initConstants(self):
        self.dataRowsCount = 10
        self.dataColCount = 10

    def compareMatrix(self, regularMatrix, algorithmDataInterface, checkName):
        self.inputMatrix = regularMatrix
        self.outputMatrix = algorithmDataInterface
        if len(regularMatrix) != len(algorithmDataInterface):
            error = "The len of the regular matrix is : " + str(len(regularMatrix)) + \
                " And the len of the algorithmDataInterface is : " + \
                    str(len(algorithmDataInterface))
            return self.createFailedResult(checkName, error)
        for idx in range(len(regularMatrix)):
            result, error = self.compareRows(idx, regularMatrix[idx], algorithmDataInterface[idx], checkName)
            if not result:
                return self.createFailedResult(checkName, error)
        return self.createOKResult(checkName)

    def compareRows(self, row_idx, regularMatrixRow, algorithmDataRowInterface, checkName):
        if len(regularMatrixRow) != len(algorithmDataRowInterface):
            error = "The len of the regular matrix row num : " + str(row_idx) + "is : " + str(
                len(regularMatrixRow)) + " And the len of the algorithmDataRowInterface is : " + str(
                    len(algorithmDataRowInterface))
            return self.createFailedResult(checkName, error)
        for idx in range(len(regularMatrixRow)):
            if regularMatrixRow[idx] != algorithmDataRowInterface[idx]:
                index = "[" + str(row_idx) + "][" + str(idx) + "]"
                error = "The element in regularMatrix" + index + " = " + str(regularMatrixRow[idx]) + \
                    " And the element in algorithmDataInterface" + \
                        index + " = " + str(algorithmDataRowInterface[idx])
                return self.createFailedResult(checkName, error)
        return True, ""

    def createDefaultRegularMatrix(self, data=None):
        regularMatrix = [["Name" for idx in range(self.dataColCount)], [
            FieldRolls.Parameter for idx in range(self.dataColCount)
        ], [FieldsTypes.RatioData for idx in range(self.dataColCount)], [
            NormalizeMethod.NormalizeToRange for idx in range(self.dataColCount)
        ], [0 for idx in range(self.dataColCount)], [1 for idx in range(self.dataColCount)],
                         [0 for idx in range(self.dataColCount)], [0 for idx in range(self.dataColCount)]]
        for row_idx in range(len(regularMatrix)):
            regularMatrix[row_idx].insert(0, str(RowNames(row_idx)))

        if data is None:
            regularMatrix.extend([[i * j for i in range(self.dataColCount)] for j in range(self.dataRowsCount)])
        else:
            if isinstance(data[0], list):
                regularMatrix.extend([[data[j] for i in range(self.dataColCount)] for j in range(self.dataRowsCount)])
            else:
                regularMatrix.extend([[data[i]] for i in range(self.dataRowsCount)])

        for row_idx in range(len(regularMatrix) - len(RowNames)):
            regularMatrix[len(RowNames) + row_idx].insert(0, "Data " + str(row_idx))

        return regularMatrix

    def dataOfRegularMatrix(self, regularMatrix):
        """
        Return the regular matrix without the header (The header rows) and the first column
        which contains the row names
        """
        return [regularMatrix[idx][1:] for idx in range(len(RowNames), len(regularMatrix))]

    def extractCols(self, regularMatrix, colsToInclude):
        """
        extract cols from regular matrix with addition of the name col
        """
        colsToIncludeFromMatrix = colsToInclude[:]
        if 0 not in colsToIncludeFromMatrix:
            colsToIncludeFromMatrix.insert(0, 0)
        return [[regularMatrix[row][col] for col in colsToIncludeFromMatrix] for row in range(len(regularMatrix))]

    def extractRows(self, regularMatrix, rowsToInclude):
        """
        extract rows while keeping the header rows 
        and regenerating the names of the data rows
        """

        # The regular matrix should be composed from:
        # The header
        # All the rows in the regularMatrix that are not in the header

        # Compose the header
        rowsToIncludeFromMatrix = [idx for idx in range(len(RowNames))]

        # Compose all the rows that are not in the header
        rowsToInclude = [rowsToInclude[idx] for idx in range(len(rowsToInclude)) if rowsToInclude[idx] > len(RowNames)]

        # Join the 2 lists
        rowsToIncludeFromMatrix.extend(rowsToInclude)

        # Extract from the regular matrix
        result = [regularMatrix[idx] for idx in rowsToIncludeFromMatrix]

        # fix the data row header it should be Data i when i is the data row index
        for idx in range(len(RowNames), len(result)):
            result[idx][0] = "Data " + str(idx - len(RowNames))

        return result

    def createDefaultAlgorithmData(self, data=None):
        if data is None:
            dataMatrix = np.matrix([[i * j for i in range(self.dataColCount)] for j in range(self.dataRowsCount)])
        else:
            dataMatrix = np.array(data)
        #    dataMatrix = np.matrix([[data for i in range(self.dataColCount)] for j in range(self.dataRowsCount)])
        nameRow = np.char.array(["Name" for idx in range(self.dataColCount)])
        rollRow = np.array([FieldRolls.Parameter for idx in range(self.dataColCount)])
        typeRow = np.array([FieldsTypes.RatioData for idx in range(self.dataColCount)])
        normalizeMethodRow = np.array([NormalizeMethod.NormalizeToRange for idx in range(self.dataColCount)])
        targetMinRow = np.array([0 for idx in range(self.dataColCount)])
        targetMaxRow = np.array([1 for idx in range(self.dataColCount)])
        minRow = np.array([0 for idx in range(self.dataColCount)])
        maxRow = np.array([0 for idx in range(self.dataColCount)])
        algorithm_data = AlgorithmData(dataMatrix, nameRow, rollRow, typeRow, normalizeMethodRow, targetMinRow,
                                      targetMaxRow, minRow, maxRow)
        algorithmDataInterface = AlgorithmDataInterface(algorithm_data)
        return algorithmDataInterface

    def check_init_from_np(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_from_np")

    def check_init_with_none_header(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        dataMatrix = np.matrix([[i * j for i in range(self.dataColCount)] for j in range(self.dataRowsCount)])
        algorithm_data = AlgorithmData(dataMatrix)
        algorithmDataInterface = AlgorithmDataInterface(algorithm_data)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_with_none_header")

    def check_init_vector(self):
        self.dataColCount = 1
        self.dataRowsCount = 10
        data = [i for i in range(self.dataRowsCount)]
        regularMatrix = self.createDefaultRegularMatrix(data)
        algorithmDataInterface = self.createDefaultAlgorithmData(data)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_vector")

    def check_init_from_np_matrix(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        np_matrix = np.matrix(self.dataOfRegularMatrix(regularMatrix))
        algorithmDataInterface = AlgorithmDataInterface(AlgorithmData(np_matrix))
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_from_np_matrix")

    def check_init_from_np_ndarray_2_dim(self):
        regularMatrix = self.createDefaultRegularMatrix()
        temp = [regularMatrix[idx][1:] for idx in range(len(RowNames), len(regularMatrix))]
        np_ndarray = np.array(self.dataOfRegularMatrix(regularMatrix))
        algorithmDataInterface = AlgorithmDataInterface(AlgorithmData(np_ndarray))
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_from_np_ndarray_2_dim")

    def check_init_from_np_ndarray_1_dim(self):
        self.dataColCount = 1
        self.dataRowsCount = 10
        data = [i for i in range(self.dataRowsCount)]
        regularMatrix = self.createDefaultRegularMatrix(data)
        np_ndarray = np.array(self.dataOfRegularMatrix(regularMatrix))
        algorithmDataInterface = AlgorithmDataInterface(AlgorithmData(np_ndarray))
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_from_np_ndarray_1_dim")

    def check_init_from_list_2_dim(self):
        regularMatrix = self.createDefaultRegularMatrix()
        list_matrix = self.dataOfRegularMatrix(regularMatrix)
        algorithmDataInterface = AlgorithmDataInterface(AlgorithmData(list_matrix))
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_from_list_2_dim")

    def check_init_from_list_1_dim(self):
        self.dataColCount = 1
        self.dataRowsCount = 10
        data = [i for i in range(self.dataRowsCount)]
        regularMatrix = self.createDefaultRegularMatrix(data)
        list_vector = np.array(self.dataOfRegularMatrix(regularMatrix))
        algorithmDataInterface = AlgorithmDataInterface(AlgorithmData(list_vector))
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_init_from_list_1_dim")

    def check_init_from_list_mixed_dim(self):
        regularMatrix = self.createDefaultRegularMatrix()
        regularMatrix[9][1] = [1, 2, 3, 4, 5]
        list_matrix = self.dataOfRegularMatrix(regularMatrix)
        try:
            algorithmDataInterface = AlgorithmDataInterface(AlgorithmData(list_matrix))
            return self.createFailedResult(
                "check_init_from_list_mixed_dim",
                "Should have Raised exception because the structure of the input is not matrix")
        except:
            return self.createOKResult("check_init_from_list_mixed_dim",
                                       "Raised exception because the structure of the input is not matrix")

    def check_getitem_roll(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        regularMatrix[1][2] = FieldRolls.Result
        algorithmDataInterface = self.createDefaultAlgorithmData()
        algorithmDataInterface[1][2] = FieldRolls.Result
        regularMatrix[10][2] = 1000
        algorithmDataInterface[10][FieldRolls.Result] = 1000
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_getitem_roll")

    def check_getitem_row(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()
        regularMatrixRow = regularMatrix[10]
        algorithmDataRow = algorithmDataInterface[10]
        if np.array_equal(regularMatrixRow, algorithmDataRow):
            return self.createOKResult("check_getitem_row")
        else:
            return self.createFailedResult("check_getitem_row", "The rows retrieved are not identical")

    def check_getitem_header_row(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()
        regularMatrixRow = regularMatrix[1]
        algorithmDataRow = algorithmDataInterface[1]
        if np.array_equal(regularMatrixRow, algorithmDataRow):
            return self.createOKResult("check_getitem_header_row")
        else:
            return self.createFailedResult("check_getitem_header_row", "The rows retrieved are not identical")

    def check_setitem_in_header_and_data_success(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithm_data = AlgorithmData(self.dataOfRegularMatrix(regularMatrix))
        algorithmDataInterface = AlgorithmDataInterface(algorithm_data)
        regularMatrix[RowNames.Names.value][1] = "Another Name"
        algorithmDataInterface[RowNames.Names.value][1] = "Another Name"
        regularMatrix[RowNames.Roll.value][1] = FieldRolls.ParameterReduction
        algorithmDataInterface[RowNames.Roll.value][1] = FieldRolls.ParameterReduction
        regularMatrix[RowNames.Types.value][1] = FieldsTypes.IntervalData
        algorithmDataInterface[RowNames.Types.value][1] = FieldsTypes.IntervalData
        regularMatrix[RowNames.NormalizeMethods.value][1] = NormalizeMethod.OneOfN
        algorithmDataInterface[RowNames.NormalizeMethods.value][1] = NormalizeMethod.OneOfN
        regularMatrix[RowNames.MinTarget.value][1] = -1
        algorithmDataInterface[RowNames.MinTarget.value][1] = -1
        regularMatrix[RowNames.MaxTarget.value][1] = 1
        algorithmDataInterface[RowNames.MaxTarget.value][1] = 1
        regularMatrix[RowNames.Min.value][1] = 100
        algorithmDataInterface[RowNames.Min.value][1] = 100
        regularMatrix[RowNames.Max.value][1] = 200
        algorithmDataInterface[RowNames.Max.value][1] = 200
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_setitem_in_header_and_data_success")

    def check_setitem_in_header_and_data_failure(self):
        try:
            self.initConstants()
            regularMatrix = self.createDefaultRegularMatrix()
            dataMatrix = np.matrix(self.dataOfRegularMatrix(regularMatrix))
            algorithm_data = AlgorithmData(dataMatrix)
            algorithmDataInterface = AlgorithmDataInterface(algorithm_data)
            regularMatrix[1][1] = 0
            algorithmDataInterface[1][1] = 0
            result, error = self.compareMatrix(regularMatrix, algorithmDataInterface,
                                               "check_setitem_in_header_and_data_failure")
            return self.createFailedResult("check_setitem_in_header_and_data_failure",
                                           "returned " + error + " - should have raise exception")
        except Exception as e:
            return self.createOKResult("check_setitem_in_header_and_data_failure", " The exception is : " + str(e))

    def check_setitem_in_header_and_index_failure(self):
        try:
            self.initConstants()
            algorithmDataInterface = self.createDefaultAlgorithmData()
            algorithmDataInterface[1][20] = 0
            return self.createFailedResult("check_setitem_in_header_and_index_failure",
                                           "returned " + error + " - should have raise exception")
        except Exception as e:
            return self.createOKResult("check_setitem_in_header_and_index_failure", " The exception is : " + str(e))

    def check_setitem_in_vectors(self):
        self.dataColCount = 1
        self.dataRowsCount = 10
        data = [i for i in range(self.dataRowsCount)]
        regularMatrix = self.createDefaultRegularMatrix(data)
        algorithmDataInterface = self.createDefaultAlgorithmData(data)
        regularMatrix[10][1] = 200
        algorithmDataInterface[10][1] = 200
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_setitem_in_vectors")

    def check_setitem_in_names_col_failure(self):
        try:
            algorithmDataInterface = self.createDefaultAlgorithmData()
            algorithmDataInterface[0][0] = 0
            return self.createFailedResult("check_setitem_in_names_col_failure",
                                           "returned " + error + " - should have raise exception")
        except Exception as e:
            return self.createOKResult("check_setitem_in_names_col_failure", " The exception is : " + str(e))

    def check_hstack_2_matrix(self):
        self.initConstants()
        regularMatrix1 = self.createDefaultRegularMatrix()
        regularMatrix2 = self.createDefaultRegularMatrix()
        algorithmDataInterface1 = self.createDefaultAlgorithmData()
        algorithmDataInterface2 = self.createDefaultAlgorithmData()
        for idx in range(len(regularMatrix1)):
            regularMatrix1[idx].extend(regularMatrix2[idx][1:])

        algorithmDataInterface1 = ufunc.hstack((algorithmDataInterface1, algorithmDataInterface2), True)
        return self.compareMatrix(regularMatrix1, algorithmDataInterface1, "check_hstack_2_matrix")

    def check_hstack_2_arrays(self):
        self.dataColCount = 1
        self.dataRowsCount = 10
        data = [i for i in range(self.dataRowsCount)]
        regularArray1 = self.createDefaultRegularMatrix(data)
        regularArray2 = self.createDefaultRegularMatrix(data)
        algorithmDataInterface1 = self.createDefaultAlgorithmData(data)
        algorithmDataInterface2 = self.createDefaultAlgorithmData(data)

        for idx in range(len(regularArray1)):
            regularArray1[idx].extend(regularArray2[idx][1:])

        algorithmDataInterface1 = ufunc.hstack((algorithmDataInterface1, algorithmDataInterface2), True)
        return self.compareMatrix(regularArray1, algorithmDataInterface1, "check_hstack_2_arrays")

    def check_hstack_array_and_matrix(self):
        self.dataColCount = 1
        self.dataRowsCount = 10
        data = [i for i in range(self.dataRowsCount)]
        regularArray = self.createDefaultRegularMatrix(data)
        algorithmDataInterface1 = self.createDefaultAlgorithmData(data)
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface2 = self.createDefaultAlgorithmData()

        for idx in range(len(regularArray)):
            regularArray[idx].extend(regularMatrix[idx][1:])

        algorithmDataInterface1 = ufunc.hstack((algorithmDataInterface1, algorithmDataInterface2), True)
        return self.compareMatrix(regularArray, algorithmDataInterface1, "check_hstack_array_and_matrix")

    def check_cols_one_index(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        colsToInclude = [2]
        regularMatrix = self.extractCols(regularMatrix, colsToInclude)

        algorithmDataInterface = algorithmDataInterface.cols(colsToInclude)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_one_index")

    def check_cols_one_name(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        colsToInclude = [3]
        colsToIncludePrm = ["A Name"]
        regularMatrix[RowNames.Names.value][3] = "A Name"
        algorithmDataInterface[RowNames.Names.value][3] = "A Name"
        regularMatrix = self.extractCols(regularMatrix, colsToInclude)
        algorithmDataInterface = algorithmDataInterface.cols(colsToIncludePrm)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_one_name")

    def check_cols_some_indexes(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        colsToInclude = [0, 3, 5]
        regularMatrix = regularMatrix = self.extractCols(regularMatrix, colsToInclude)
        algorithmDataInterface = algorithmDataInterface.cols(colsToInclude)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_some_indexes")

    def check_cols_some_names(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        colsToInclude = [1, 3, 5]
        colsToIncludePrm = ["A Name"]
        for col_idx in colsToInclude:
            regularMatrix[RowNames.Names.value][col_idx] = "A Name"
            algorithmDataInterface[RowNames.Names.value][col_idx] = "A Name"
        regularMatrix = regularMatrix = self.extractCols(regularMatrix, colsToInclude)
        algorithmDataInterface = algorithmDataInterface.cols(colsToIncludePrm)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_some_indexes")

    def check_cols_mixed_indexes_and_names(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        # Change the names
        colsToInclude = [1, 3]
        colsToIncludePrm = ["A Name"]
        for col_idx in colsToInclude:
            regularMatrix[RowNames.Names.value][col_idx] = "A Name"
            algorithmDataInterface[RowNames.Names.value][col_idx] = "A Name"

        # Add the indexes
        colsToInclude.append(2)
        colsToIncludePrm.append(2)

        # Sort colsToInclude (This sorting effects only the regular matrix. The AlgorithmData
        # is expected to do the sort by himself)
        colsToInclude = sorted(colsToInclude)

        regularMatrix = self.extractCols(regularMatrix, colsToInclude)
        algorithmDataInterface = algorithmDataInterface.cols(colsToIncludePrm)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_mixed_indexes_and_names")

    def check_cols_one_roll(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        colsToInclude = [3]
        colsToIncludePrm = FieldRolls.ParameterReduction
        for col_idx in colsToInclude:
            regularMatrix[RowNames.Roll.value][col_idx] = FieldRolls.ParameterReduction
            algorithmDataInterface[RowNames.Roll.value][col_idx] = FieldRolls.ParameterReduction

        regularMatrix = self.extractCols(regularMatrix, colsToInclude)
        algorithmDataInterface = algorithmDataInterface.cols(colsToIncludePrm)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_one_roll")

    def check_cols_some_roll(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        colsToInclude = [1, 3, 5]
        colsToIncludePrm = FieldRolls.ParameterReduction
        for col_idx in colsToInclude:
            regularMatrix[RowNames.Roll.value][col_idx] = FieldRolls.ParameterReduction
            algorithmDataInterface[RowNames.Roll.value][col_idx] = FieldRolls.ParameterReduction

        regularMatrix = self.extractCols(regularMatrix, colsToInclude)
        algorithmDataInterface = algorithmDataInterface.cols(colsToIncludePrm)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_cols_one_roll")

    def check_rows(self):
        self.initConstants()
        regularMatrix = self.createDefaultRegularMatrix()
        algorithmDataInterface = self.createDefaultAlgorithmData()

        rowsToInclude = [1, 2, 10, 12]
        regularMatrix = self.extractRows(regularMatrix, rowsToInclude)
        algorithmDataInterface = algorithmDataInterface.rows(rowsToInclude)
        return self.compareMatrix(regularMatrix, algorithmDataInterface, "check_rows")
