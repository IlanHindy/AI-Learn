# Python Imports
import sys
import os

# Third party imports
import numpy as np

# PyQt imports

# My imports

from ..Infrastructure.AlgorithmData import AlgorithmData, ufunc, RowNames
from ..Infrastructure.Enums import FieldRolls, FieldsTypes, NormalizeMethod
from ..Tests.TestBase import TestBase


class AlgorithmDataTest(TestBase):
    """description of class"""

    def __init__(self, parentWindow):
        super(AlgorithmDataTest, self).__init__(parentWindow)
        self.addTest("Check __getitem__ retrieve row or rows")
        self.addTest(self.check_row)
        self.addTest(self.check_header_row)
        self.addTest(self.check_rows_listInt)
        self.addTest(self.check_rows_listIntRowNames)
        self.addTest(self.check_rows_allData)
        self.addTest(self.check_rows_slice_start)
        self.addTest(self.check_rows_slice_end)
        self.addTest(self.check_rows_slice_start_end)
        self.addTest(self.check_rows_slice_start_end_step)
        self.addTest("Check __getitem__ retrieve one value")
        self.addTest(self.check_single_value_int_int)
        self.addTest(self.check_single_value_int_FieldRoll)
        self.addTest(self.check_single_value_RowName_int)
        self.addTest(self.check_single_value_RowName_FieldRolls)
        self.addTest("Check __getitem__ retrieve one column row parameter - int")
        self.addTest(self.check_cols_int_listInt)
        self.addTest(self.check_cols_int_listIntFieldRolls)
        self.addTest(self.check_cols_int_slice_all)
        self.addTest(self.check_cols_int_slice_start)
        self.addTest(self.check_cols_int_slice_stop)
        self.addTest(self.check_cols_int_slice_start_stop)
        self.addTest(self.check_cols_int_slice_start_stop_step)
        self.addTest("Check __getitem__ retrieve one column row parameter - RowNames")
        self.addTest(self.check_cols_RowNames_listInt)
        self.addTest(self.check_cols_rowNames_listIntFieldRolls)
        self.addTest(self.check_cols_fieldRolls_slice_all)
        self.addTest(self.check_cols_fieldRolls_slice_all)
        self.addTest(self.check_cols_fieldRolls_slice_stop)
        self.addTest(self.check_cols_rowNames_slice_start_stop)
        self.addTest(self.check_cols_rowNames_slice_start_stop_step)
        self.addTest("Check __getitem__ slice row parameter - list[int]")
        self.addTest(self.check_slice_listInt_listInt)
        self.addTest(self.check_slice_listInt_listIntFieldRolls)
        self.addTest(self.check_slice_ListInt_sliceAll)
        self.addTest(self.check_slice_ListInt_slice_start)
        self.addTest(self.check_cols_int_slice_stop)
        self.addTest(self.check_cols_int_slice_start_stop)
        self.addTest(self.check_cols_int_slice_start_stop_step)
        self.addTest("Check __getitem__ slice row parameter - list[Mixed]")
        self.addTest(self.check_slice_listMixed_listInt)
        self.addTest(self.check_slice_listMixed_listMixed)
        self.addTest(self.check_slice_listMixed_slice_all)
        self.addTest(self.check_slice_listMixed_slice_start)
        self.addTest(self.check_slice_listMixed_slice_start_stop)
        self.addTest(self.check_slice_listMixed_slice_start_stop_step)
        self.addTest("Check __getitem__ slice row parameter - all ([:])")
        self.addTest(self.check_slice_all_listInt)
        self.addTest(self.check_slice_all_listMixed)
        self.addTest(self.check_slice_all_slice_all)
        self.addTest(self.check_slice_all_slice_start)
        self.addTest(self.check_slice_all_slice_start_stop)
        self.addTest(self.check_slice_all_slice_start_stop_step)
        self.addTest("Check __getitem__ slice row parameter - start ([start:])")
        self.addTest(self.check_slice_start_listInt)
        self.addTest(self.check_slice_start_listMixed)
        self.addTest(self.check_slice_start_slice_all)
        self.addTest(self.check_slice_start_slice_start)
        self.addTest(self.check_slice_start_slice_start_stop)
        self.addTest(self.check_slice_start_slice_start_stop_step)
        self.addTest("Check __getitem__ slice row parameter - start, stop ([start:stop])")
        self.addTest(self.check_slice_start_stop_listInt)
        self.addTest(self.check_slice_start_stop_listMixed)
        self.addTest(self.check_slice_start_stop_slice_all)
        self.addTest(self.check_slice_start_stop_slice_start)
        self.addTest(self.check_slice_start_stop_slice_start_stop)
        self.addTest(self.check_slice_start_stop_slice_start_stop_step)
        self.addTest("Check __getitem__ slice row parameter - start, stop, step ([start:stop:step])")
        self.addTest(self.check_slice_start_stop_step_listInt)
        self.addTest(self.check_slice_start_stop_step_listMixed)
        self.addTest(self.check_slice_start_stop_step_slice_all)
        self.addTest(self.check_slice_start_stop_step_slice_start)
        self.addTest(self.check_slice_start_stop_step_slice_start_stop)
        self.addTest(self.check_slice_start_stop_step_slice_start_stop_step)

    def initTestData(self):
        self.dataRowsCount = 10
        self.dataColsCount = 10
        self.data = [[float(row_idx * 10 + col_idx) for col_idx in range(self.dataColsCount)]
                     for row_idx in range(self.dataRowsCount)]

    def createRegularMatrix(self, data=None):
        """
        Note : The data must be python matrix
        """
        if data is None:
            self.initTestData()
        else:
            self.dataColsCount = len(data[0])
        regularMatrix = [["Name" + str(idx) for idx in range(self.dataColsCount)]]
        regularMatrix.append([FieldRolls(idx % len(FieldRolls)) for idx in range(self.dataColsCount)])
        typesRow = ([FieldsTypes(idx % len(FieldsTypes)) for idx in range(self.dataColsCount)])
        regularMatrix.append(typesRow)
        normalizeMethodRow = [NormalizeMethod(idx % len(NormalizeMethod)) for idx in range(self.dataColsCount)]
        regularMatrix.append(
            AlgorithmData.adjust_normalize_method_row_length(np.array(normalizeMethodRow), np.array(typesRow)).tolist())
        regularMatrix.append([idx for idx in range(self.dataColsCount)])
        regularMatrix.append([idx * 10 for idx in range(self.dataColsCount)])
        regularMatrix.append([idx for idx in range(self.dataColsCount)])
        regularMatrix.append([idx * 10 for idx in range(self.dataColsCount)])

        if data is None:
            regularMatrix.extend(self.data)
        else:
            regularMatrix.extend(data)

        return regularMatrix

    def createAlgorithmData(self, regularMatrix):
        nameRow = np.char.array(regularMatrix[RowNames.Names.value])
        rollRow = np.array(regularMatrix[RowNames.Roll.value])
        typeRow = np.array(regularMatrix[RowNames.Types.value])
        normalizeMethodRow = np.array(regularMatrix[RowNames.NormalizeMethods.value])
        targetMinRow = np.array(regularMatrix[RowNames.MinTarget.value])
        targetMaxRow = np.array(regularMatrix[RowNames.MaxTarget.value])
        minRow = np.array(regularMatrix[RowNames.Min.value])
        maxRow = np.array(regularMatrix[RowNames.Max.value])
        dataMatrix = regularMatrix[RowNames.Max.value + 1:]
        algorithm_data = AlgorithmData(dataMatrix, nameRow, rollRow, typeRow, normalizeMethodRow, targetMinRow,
                                      targetMaxRow, minRow, maxRow)
        return algorithm_data

    # retrieve row (one parameter the row number)/// check_rows_listIntRowNames
    # algorithm_data[int]
    def check_row(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRow = regularMatrix[10]
        algorithmDataRow = algorithm_data[10 - len(algorithm_data.header)]
        if np.array_equal(regularMatrixRow, algorithmDataRow):
            return self.createOKResult("check_row")
        else:
            return self.createFailedResult("check_row", "The arrays are not equal")

    # algorithm_data[RowNames]
    def check_header_row(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRow = regularMatrix[0]
        algorithmDataRow = algorithm_data[RowNames.Names]
        if np.array_equal(regularMatrixRow, algorithmDataRow):
            return self.createOKResult("check_header_row")
        else:
            return self.createFailedResult("check_header_row", "The arrays are not equal")

    # algorithm_data[[int,int...]]
    def check_rows_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rowsToGet = [10, 12, 14]
        regularMatrixRows = [regularMatrix[row] for row in rowsToGet]
        algorithmDataRows = algorithm_data[[row - len(algorithm_data.header) for row in rowsToGet]]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_listInt")
        else:
            return self.createFailedResult("check_rows_listInt", "The arrays are not equal")

    # algorithm_data[[RowName, int,int...]]
    def check_rows_listIntRowNames(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rowsToGet = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        regularMatrixRows = [regularMatrix[row] for row in rowsToGet]
        regularMatrixRows = [[str(regularMatrixRows[row_idx][col_idx]) for col_idx in range(len(regularMatrixRows[0]))]
                             for row_idx in range(len(regularMatrixRows))]
        rowsToGetAlgorithmData = [RowNames.Names, RowNames.NormalizeMethods]
        rowsToGetAlgorithmData.extend([row - len(algorithm_data.header) for row in rowsToGet[2:]])
        algorithmDataRows = algorithm_data[rowsToGetAlgorithmData]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_listIntRowNames")
        else:
            return self.createFailedResult("check_rows_listIntRowNames", "The arrays are not equal")

    # algorithm_data[:]
    def check_rows_allData(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRows = regularMatrix[len(algorithm_data.header):]
        algorithmDataRows = algorithm_data[:]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_allData")
        else:
            return self.createFailedResult("check_rows_allData", "The arrays are not equal")

    # algorithm_data[int:]
    def check_rows_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRows = regularMatrix[len(algorithm_data.header) + 2:]
        algorithmDataRows = algorithm_data[2:]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_allData")
        else:
            return self.createFailedResult("check_rows_allData", "The arrays are not equal")

    # algorithm_data[:int]
    def check_rows_slice_end(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRows = regularMatrix[len(algorithm_data.header):len(algorithm_data.header) + 7]
        algorithmDataRows = algorithm_data[:7]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_slice_end")
        else:
            return self.createFailedResult("check_rows_slice_end", "The arrays are not equal")

    # algorithm_data[int:int]
    def check_rows_slice_start_end(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRows = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 7]
        algorithmDataRows = algorithm_data[2:7]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_slice_start_end")
        else:
            return self.createFailedResult("check_rows_slice_start_end", "The arrays are not equal")

    # algorithm_data[int:int:int]
    def check_rows_slice_start_end_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixRows = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 7:2]
        algorithmDataRows = algorithm_data[2:7:2]
        if np.array_equal(regularMatrixRows, algorithmDataRows):
            return self.createOKResult("check_rows_slice_start_end_step")
        else:
            return self.createFailedResult("check_rows_slice_start_end_step", "The arrays are not equal")

    # Retrieve single value
    # algorithm_data[int,int]
    def check_single_value_int_int(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixValue = regularMatrix[10][5]
        algorithmDataValue = algorithm_data[10 - len(algorithm_data.header), 5]
        if regularMatrixValue == algorithmDataValue:
            return self.createOKResult("check_single_value_int_int")
        else:
            return self.createFailedResult("check_single_value_int_int",
                                           "The regular matrix value :" + str(regularMatrixValue) +
                                           " The algorithm data value : " + str(algorithmDataValue))

    # algorithm_data[int, FieldRoll]
    def check_single_value_int_FieldRoll(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        for idx in range(len(regularMatrix[0])):
            regularMatrix[RowNames.Roll.value][idx] = FieldRolls.Parameter
            algorithm_data[RowNames.Roll, idx] = FieldRolls.Parameter

        regularMatrix[RowNames.Roll.value][5] = FieldRolls.StepResult
        algorithm_data[RowNames.Roll, 5] = FieldRolls.StepResult
        regularMatrixValue = regularMatrix[10][5]
        algorithmDataValue = algorithm_data[10 - len(algorithm_data.header), FieldRolls.StepResult]
        if regularMatrixValue == algorithmDataValue:
            return self.createOKResult("check_single_value_int_FieldRoll")
        else:
            return self.createFailedResult("check_single_value_int_FieldRoll",
                                           "The regular matrix value :" + str(regularMatrixValue) +
                                           " The algorithm data value : " + str(algorithmDataValue))

    # algorithm_data[RowName, int]
    def check_single_value_RowName_int(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        for col_idx in range(len(regularMatrix[0])):
            regularMatrix[0][col_idx] = "Name" + str(col_idx)
            algorithm_data[RowNames.Names, col_idx] = "Name" + str(col_idx)
        regularMatrixValue = regularMatrix[0][5]
        algorithmDataValue = algorithm_data[RowNames.Names, 5]
        if regularMatrixValue == algorithmDataValue:
            return self.createOKResult("check_single_value_RowName_int")
        else:
            return self.createFailedResult("check_single_value_RowName_int",
                                           "The regular matrix value :" + str(regularMatrixValue) +
                                           " The algorithm data value : " + str(algorithmDataValue))

    # algorithm_data[RowName, FieldRolls]
    def check_single_value_RowName_FieldRolls(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        for idx in range(len(regularMatrix[0])):
            regularMatrix[RowNames.Roll.value][idx] = FieldRolls.Parameter
            algorithm_data[RowNames.Roll, idx] = FieldRolls.Parameter

        regularMatrix[RowNames.Roll.value][5] = FieldRolls.StepResult
        algorithm_data[RowNames.Roll, 5] = FieldRolls.StepResult
        regularMatrixValue = regularMatrix[RowNames.NormalizeMethods.value][FieldRolls.StepResult.value]
        algorithmDataValue = algorithm_data[RowNames.NormalizeMethods, FieldRolls.StepResult]
        if regularMatrixValue == algorithmDataValue:
            return self.createOKResult("check_single_value_RowName_FieldRolls")
        else:
            return self.createFailedResult("check_single_value_RowName_FieldRolls",
                                           "The regular matrix value :" + str(regularMatrixValue) +
                                           " The algorithm data value : " + str(algorithmDataValue))

    # Retrieve columns
    # Row parameter - int
    # algorithm_data[int, [int,int...]
    def check_cols_int_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        cols_idx = [1, 3, 4, 7]
        cols = 10
        regularMatrixValue = [regularMatrix[10][col_idx] for col_idx in cols_idx]
        algorithmDataValue = algorithm_data[10 - len(algorithm_data.header), cols_idx]
        if np.array_equal(regularMatrixValue, algorithmDataValue):
            return self.createOKResult("check_cols_int_listInt")
        else:
            return self.createFailedResult("check_cols_int_listInt", "The arrays are not equal")

    # algorithm_data[int,[FieldRoll, int...]]
    def check_cols_int_listIntFieldRolls(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        cols_idx = [
            idx for idx in range(len(regularMatrix[RowNames.Roll.value]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.StepResult
        ]
        cols_idx.extend([1, 5, 9])
        cols_idx = sorted(list(set(cols_idx)))

        regularMatrixCols = [regularMatrix[10][col_idx] for col_idx in cols_idx]
        algorithmDataCols = algorithm_data[10 - len(algorithm_data.header), [1, FieldRolls.StepResult, 5, 9]]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_int_listIntFieldRolls")
        else:
            return self.createFailedResult("check_cols_int_listIntFieldRolls", "The arrays are not equal")

    # algorithm_data[int,:]
    def check_cols_int_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[10][:]
        algorithmDataCols = algorithm_data[10 - len(algorithm_data.header), :]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_int_slice_all")
        else:
            return self.createFailedResult("check_cols_int_slice_all", "The arrays are not equal")

    # algorithm_data[int, start:]
    def check_cols_int_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[10][5:]
        algorithmDataCols = algorithm_data[10 - len(algorithm_data.header), 5:]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_int_slice_start")
        else:
            return self.createFailedResult("check_cols_int_slice_start", "The arrays are not equal")

    # algorithm_data[int, :stop]
    def check_cols_int_slice_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[10][:5]
        algorithmDataCols = algorithm_data[10 - len(algorithm_data.header), :5]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_int_slice_stop")
        else:
            return self.createFailedResult("check_cols_int_slice_stop", "The arrays are not equal")

    # algorithm_data[int, start:stop]
    def check_cols_int_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[10][5:7]
        algorithmDataCols = algorithm_data[10 - len(algorithm_data.header), 5:7]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_int_slice_start_stop")
        else:
            return self.createFailedResult("check_cols_int_slice_start_stop", "The arrays are not equal")

    # algorithm_data[int, start:stop:step]
    def check_cols_int_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[10][1:9:2]
        algorithmDataCols = algorithm_data[10 - len(algorithm_data.header), 1:9:2]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_int_slice_start_stop_step")
        else:
            return self.createFailedResult("check_cols_int_slice_start_stop_step", "The arrays are not equal")

    # Retrieve columns
    # Row parameter - RowNames
    # algorithm_data[RowName, [ini,int...]]
    def check_cols_RowNames_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        cols_idx = [1, 3, 4, 7]
        regularMatrixValue = [regularMatrix[RowNames.NormalizeMethods.value][col_idx] for col_idx in cols_idx]
        algorithmDataValue = algorithm_data[RowNames.NormalizeMethods, cols_idx]
        if np.array_equal(regularMatrixValue, algorithmDataValue):
            return self.createOKResult("check_cols_RowNames_listInt")
        else:
            return self.createFailedResult("check_cols_RowNames_listInt", "The arrays are not equal")

    # algorithm_data[RowNames,[FieldRoll, int...]]
    def check_cols_rowNames_listIntFieldRolls(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        cols_idx = [
            idx for idx in range(len(regularMatrix[RowNames.Roll.value]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.StepResult
        ]
        cols_idx.extend([1, 5, 9])
        cols_idx = sorted(list(set(cols_idx)))

        regularMatrixCols = [regularMatrix[RowNames.NormalizeMethods.value][col_idx] for col_idx in cols_idx]
        algorithmDataCols = algorithm_data[RowNames.NormalizeMethods, [1, FieldRolls.StepResult, 5, 9]]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_rowNames_listIntFieldRolls")
        else:
            return self.createFailedResult("check_cols_rowNames_listIntFieldRolls", "The arrays are not equal")

    # algorithm_data[RowNames,:]
    def check_cols_fieldRolls_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[RowNames.Min.value][:]
        algorithmDataCols = algorithm_data[RowNames.Min, :]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_fieldRolls_slice_all")
        else:
            return self.createFailedResult("check_cols_fieldRolls_slice_all", "The arrays are not equal")

    # algorithm_data[RowNames, start:]
    def check_cols_rowNams_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[RowNames.Max.value][5:]
        algorithmDataCols = algorithm_data[RowNames.Max, 5:]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_rowNams_slice_start")
        else:
            return self.createFailedResult("check_cols_rowNams_slice_start", "The arrays are not equal")

    # algorithm_data[int, :stop]
    def check_cols_fieldRolls_slice_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[RowNames.Max.value][:5]
        algorithmDataCols = algorithm_data[RowNames.Max, :5]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_fieldRolls_slice_stop")
        else:
            return self.createFailedResult("check_cols_fieldRolls_slice_stop", "The arrays are not equal")

    # algorithm_data[int, start:stop]
    def check_cols_rowNames_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[RowNames.Max.value][5:7]
        algorithmDataCols = algorithm_data[RowNames.Max, 5:7]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_rowNames_slice_start_stop")
        else:
            return self.createFailedResult("check_cols_rowNames_slice_start_stop", "The arrays are not equal")

    # algorithm_data[int, start:stop:step]
    def check_cols_rowNames_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixCols = regularMatrix[RowNames.Max.value][1:9:2]
        algorithmDataCols = algorithm_data[RowNames.Max, 1:9:2]
        if np.array_equal(regularMatrixCols, algorithmDataCols):
            return self.createOKResult("check_cols_rowNames_slice_start_stop_step")
        else:
            return self.createFailedResult("check_cols_rowNames_slice_start_stop_step", "The arrays are not equal")

    # Slice
    # row parameter - List[int]
    # algorithm_data[list[int],list[int]]
    def check_slice_listInt_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]
        cols_idx = [2, 5, 7]
        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in cols_idx] for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header) for row_idx in rows_idx], cols_idx]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listInt_listInt")
        else:
            return self.createFailedResult("check_slice_listInt_listInt", "The arrays are not equal")

    # algorithm_data[list[int], List[int, fieldRoll]]
    def check_slice_listInt_listIntFieldRolls(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]

        cols_idx = [
            idx for idx in range(len(regularMatrix[RowNames.Roll.value]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.StepResult
        ]
        cols_idx.extend([1, 5, 9])
        cols_idx = sorted(list(set(cols_idx)))

        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in cols_idx] for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header)
                                            for row_idx in rows_idx], [1, FieldRolls.StepResult, 5, 9]]

        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listInt_listIntFieldRolls")
        else:
            return self.createFailedResult("check_slice_listInt_listIntFieldRolls", "The arrays are not equal")

    # algorithm_data[List[int], :]
    def check_slice_ListInt_sliceAll(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]

        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in range(len(regularMatrix[0]))]
                              for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header) for row_idx in rows_idx], :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_ListInt_sliceAll")
        else:
            return self.createFailedResult("check_slice_ListInt_sliceAll", "The arrays are not equal")

    # algorithm_data[List[int], start:]
    def check_slice_ListInt_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]
        cols_idx = [idx for idx in range(5, len(regularMatrix[0]))]

        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in cols_idx] for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header) for row_idx in rows_idx], 5:]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_ListInt_slice_start")
        else:
            return self.createFailedResult("check_slice_ListInt_slice_start", "The arrays are not equal")

    # algorithm_data[list[int], :stop]
    def check_slice_ListInt_slice_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]
        cols_idx = [idx for idx in range(0, 8)]

        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in cols_idx] for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header) for row_idx in rows_idx], :8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_ListInt_slice_stop")
        else:
            return self.createFailedResult("check_slice_ListInt_slice_stop", "The arrays are not equal")

    # algorithm_data[List[int], start:stop]
    def check_slice_ListInt_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]
        cols_idx = [idx for idx in range(5, 8)]

        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in range(len(regularMatrix[0]))]
                              for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header) for row_idx in rows_idx], 5:8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_ListInt_slice_start_stop")
        else:
            return self.createFailedResult("check_slice_ListInt_slice_start_stop", "The arrays are not equal")

    # algorithm_data[List[int], start:stop:step]
    def check_slice_ListInt_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        rows_idx = [10, 12, 15]
        cols_idx = [idx for idx in range(2, 8, 2)]

        regularMatrixSlice = [[regularMatrix[row_idx][col_idx] for col_idx in range(len(regularMatrix[0]))]
                              for row_idx in rows_idx]
        algorithmDataSlice = algorithm_data[[row_idx - len(algorithm_data.header) for row_idx in rows_idx], 2:8:2]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_ListInt_slice_start_stop_step")
        else:
            return self.createFailedResult("check_slice_ListInt_slice_start_stop_step", "The arrays are not equal")

    # Slice
    # row parameter - List[mixed]
    # algorithm_data[list[mixed],list[int]]
    def check_slice_listMixed_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        cols_idx = [1, 3, 5]
        regularMatrixSlice = [regularMatrix[row] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], cols_idx]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_listInt")
        else:
            return self.createFailedResult("check_slice_listMixed_listInt", "The arrays are not equal")

    # algorithm_data[list[mixed],list[mixed]]
    def check_slice_listMixed_listMixed(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        cols_idx = [
            idx for idx in range(len(regularMatrix[0]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.Other
        ]
        cols_idx.extend([1, 3, 5])
        cols_idx = sorted(cols_idx)
        regularMatrixSlice = [regularMatrix[row] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], [1, 3, 5, FieldRolls.Other]]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_listMixed")
        else:
            return self.createFailedResult("check_slice_listMixed_listMixed", "The arrays are not equal")

    # algorithm_data[list[mixed],:]
    def check_slice_listMixed_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        regularMatrixSlice = [regularMatrix[row][:] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in range(len(regularMatrix[0]))]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_slice_all")
        else:
            return self.createFailedResult("check_slice_listMixed_slice_all", "The arrays are not equal")

    # algorithm_data[list[mixed],:]
    def check_slice_listMixed_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        regularMatrixSlice = [regularMatrix[row][:] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in range(len(regularMatrix[0]))]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_slice_all")
        else:
            return self.createFailedResult("check_slice_listMixed_slice_all", "The arrays are not equal")

    # algorithm_data[list[mixed],start:]
    def check_slice_listMixed_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        regularMatrixSlice = [regularMatrix[row][5:] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in range(len(regularMatrixSlice[0]))]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], 5:]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_slice_start")
        else:
            return self.createFailedResult("check_slice_listMixed_slice_start", "The arrays are not equal")

    # algorithm_data[list[mixed],start:stop]
    def check_slice_listMixed_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        regularMatrixSlice = [regularMatrix[row][5:8] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in range(len(regularMatrixSlice[0]))]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], 5:8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_slice_start_stop")
        else:
            return self.createFailedResult("check_slice_listMixed_slice_start_stop", "The arrays are not equal")

    # algorithm_data[list[mixed],start:stop:step]
    def check_slice_listMixed_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        rows_idx = [RowNames.Names.value, RowNames.NormalizeMethods.value, 10, 12, 14]
        regularMatrixSlice = [regularMatrix[row][1:8:2] for row in rows_idx]
        regularMatrixSlice = [[str(regularMatrixSlice[row_idx][col_idx]) for col_idx in range(len(regularMatrixSlice[0]))]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[[
            RowNames.Names, RowNames.NormalizeMethods, 10 - len(algorithm_data.header), 12 - len(algorithm_data.header),
            14 - len(algorithm_data.header)
        ], 1:8:2]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_slice_start_stop_step")
        else:
            return self.createFailedResult("check_slice_listMixed_slice_start_stop_step", "The arrays are not equal")

    # row parameter - all ([:]
    # algorithm_data[:,list[int]]
    def check_slice_all_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        cols_idx = [1, 3, 5]
        regularMatrixSlice = regularMatrix[len(algorithm_data.header):]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[:, cols_idx]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_all_listInt")
        else:
            return self.createFailedResult("check_slice_all_listInt", "The arrays are not equal")

    # algorithm_data[:,list[mixed]]
    def check_slice_all_listMixed(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        cols_idx = [
            idx for idx in range(len(regularMatrix[0]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.StepResult
        ]
        cols_idx.extend([1, 3, 5])
        cols_idx = sorted(list(set(cols_idx)))

        regularMatrixSlice = regularMatrix[len(algorithm_data.header):]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[:, [1, 3, 5, FieldRolls.StepResult]]

        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_all_listMixed")
        else:
            return self.createFailedResult("check_slice_all_listMixed", "The arrays are not equal")

    # algorithm_data[:,:]
    def check_slice_all_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header):]
        regularMatrixSlice = [regularMatrixSlice[row_idx][:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[:, :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_all_slice_all")
        else:
            return self.createFailedResult("check_slice_all_slice_all", "The arrays are not equal")

    # algorithm_data[:,start:]
    def check_slice_all_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header):]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[:, 5:]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_all_slice_start")
        else:
            return self.createFailedResult("check_slice_all_slice_start", "The arrays are not equal")

    # algorithm_data[:,start:stop]
    def check_slice_all_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header):]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:8] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[:, 5:8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_listMixed_slice_start_stop")
        else:
            return self.createFailedResult("check_slice_listMixed_slice_start_stop", "The arrays are not equal")

    # algorithm_data[:,start:stop:step]
    def check_slice_all_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header):]
        regularMatrixSlice = [regularMatrixSlice[row_idx][1:8:2] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[:, 1:8:2]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_all_slice_start_stop_step")
        else:
            return self.createFailedResult("check_slice_all_slice_start_stop_step", "The arrays are not equal")

    # row parameter - all ([start:]
    # algorithm_data[start:,list[int]]
    def check_slice_start_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        cols_idx = [1, 3, 5]
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:, cols_idx]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_listInt")
        else:
            return self.createFailedResult("check_slice_start_listInt", "The arrays are not equal")

    # algorithm_data[start:,list[mixed]]
    def check_slice_start_listMixed(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        cols_idx = [
            idx for idx in range(len(regularMatrix[0]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.Other
        ]
        cols_idx.extend([1, 3, 5])
        cols_idx = sorted(cols_idx)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:, [1, 3, 5, FieldRolls.Other]]

        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_listMixed")
        else:
            return self.createFailedResult("check_slice_start_listMixed", "The arrays are not equal")

    # algorithm_data[start:,:]
    def check_slice_start_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:]
        regularMatrixSlice = [regularMatrixSlice[row_idx][:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:, :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_slice_all")
        else:
            return self.createFailedResult("check_slice_start_slice_all", "The arrays are not equal")

    # algorithm_data[start:,start:]
    def check_slice_start_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:, 5:]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_slice_start")
        else:
            return self.createFailedResult("check_slice_start_slice_start", "The arrays are not equal")

    # algorithm_data[start:,start:stop]
    def check_slice_start_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:8] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:, 5:8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_slice_start_stop")
        else:
            return self.createFailedResult("check_slice_start_slice_start_stop", "The arrays are not equal")

    # algorithm_data[start:,start:stop:step]
    def check_slice_start_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:]
        regularMatrixSlice = [regularMatrixSlice[row_idx][1:8:2] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:, 1:8:2]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_slice_start_stop_step")
        else:
            return self.createFailedResult("check_slice_start_slice_start_stop_step", "The arrays are not equal")

    # row parameter - all ([start:stop]
    # algorithm_data[start:stop,list[int]]
    def check_slice_start_stop_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        cols_idx = [1, 3, 5]
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, cols_idx]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_listInt")
        else:
            return self.createFailedResult("check_slice_start_stop_listInt", "The arrays are not equal")

    # algorithm_data[start:stop,list[mixed]]
    def check_slice_start_stop_listMixed(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        cols_idx = [
            idx for idx in range(len(regularMatrix[0]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.Other
        ]
        cols_idx.extend([1, 3, 5])
        cols_idx = sorted(cols_idx)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, [1, 3, 5, FieldRolls.Other]]

        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_listMixed")
        else:
            return self.createFailedResult("check_slice_start_stop_listMixed", "The arrays are not equal")

    # algorithm_data[start:stop,:]
    def check_slice_start_stop_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [regularMatrixSlice[row_idx][:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_slice_all")
        else:
            return self.createFailedResult("check_slice_start_stop_slice_all", "The arrays are not equal")

    # algorithm_data[start:stop,start:]
    def check_slice_start_stop_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, 5:]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_slice_start")
        else:
            return self.createFailedResult("check_slice_start_stop_slice_start", "The arrays are not equal")

    # algorithm_data[start:stop,start:stop]
    def check_slice_start_stop_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:8] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, 5:8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_slice_start_stop")
        else:
            return self.createFailedResult("check_slice_start_stop_slice_start_stop", "The arrays are not equal")

    # algorithm_data[start:stop,start:stop:step]
    def check_slice_start_stop_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [regularMatrixSlice[row_idx][1:8:2] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, 1:8:2]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_slice_start_stop_step")
        else:
            return self.createFailedResult("check_slice_start_stop_slice_start_stop_step", "The arrays are not equal")

    # row parameter - start, stop, step ([start:stop:step]
    # algorithm_data[start:stop:step,list[int]]
    def check_slice_start_stop_step_listInt(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        cols_idx = [1, 3, 5]
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8:2]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8:2, cols_idx]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_step_listInt")
        else:
            return self.createFailedResult("check_slice_start_stop_step_listInt", "The arrays are not equal")

    # algorithm_data[start:stop:step,list[mixed]]
    def check_slice_start_stop_step_listMixed(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        cols_idx = [
            idx for idx in range(len(regularMatrix[0]))
            if regularMatrix[RowNames.Roll.value][idx] == FieldRolls.Other
        ]
        cols_idx.extend([1, 3, 5])
        cols_idx = sorted(cols_idx)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [[regularMatrixSlice[row_idx][col_idx] for col_idx in cols_idx]
                              for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, [1, 3, 5, FieldRolls.Other]]

        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_step_listMixed")
        else:
            return self.createFailedResult("check_slice_start_stop_step_listMixed", "The arrays are not equal")

    # algorithm_data[start:stop:step,:]
    def check_slice_start_stop_step_slice_all(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8:2]
        regularMatrixSlice = [regularMatrixSlice[row_idx][:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8:2, :]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_step_slice_all")
        else:
            return self.createFailedResult("check_slice_start_stop_step_slice_all", "The arrays are not equal")

    # algorithm_data[start:stop:step,start:]
    def check_slice_start_stop_step_slice_start(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)

        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8, 5:]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop__step_slice_start")
        else:
            return self.createFailedResult("check_slice_start_stop__step_slice_start", "The arrays are not equal")

    # algorithm_data[start:stop:step,start:stop]
    def check_slice_start_stop_step_slice_start_stop(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8:2]
        regularMatrixSlice = [regularMatrixSlice[row_idx][5:8] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8:2, 5:8]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_step_slice_start_stop")
        else:
            return self.createFailedResult("check_slice_start_stop_step_slice_start_stop", "The arrays are not equal")

    # algorithm_data[start:stop:step,start:stop:step]
    def check_slice_start_stop_step_slice_start_stop_step(self):
        regularMatrix = self.createRegularMatrix()
        algorithm_data = self.createAlgorithmData(regularMatrix)
        regularMatrixSlice = regularMatrix[len(algorithm_data.header) + 2:len(algorithm_data.header) + 8:2]
        regularMatrixSlice = [regularMatrixSlice[row_idx][1:8:2] for row_idx in range(len(regularMatrixSlice))]

        algorithmDataSlice = algorithm_data[2:8:2, 1:8:2]
        if np.array_equal(regularMatrixSlice, algorithmDataSlice):
            return self.createOKResult("check_slice_start_stop_step_slice_start_stop_step")
        else:
            return self.createFailedResult("check_slice_start_stop_step_slice_start_stop_step",
                                           "The arrays are not equal")
