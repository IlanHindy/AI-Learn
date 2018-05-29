# Python Imports
from typing import List, Union
from typing import NewType
from enum import Enum
#NdArray = NewType('np.ndarray', type)

# Third party imports
import numpy as np
from sklearn.decomposition import PCA

# PyQt imports

# My imports
# if "relativeImport" in globals():
try:
    from ..Infrastructure.Enums import FieldRolls, FieldsTypes, NormalizeMethod
    from ..Utilities.PythonUtilities import PythonUtilities
except:
    from Enums import FieldRolls, FieldsTypes, NormalizeMethod
    from PythonUtilities import PythonUtilities


class RowNames(Enum):
    """
    Enum for indexing AlgorithmData header rows
    """
    Names = 0
    Roll = 1
    Types = 2
    NormalizeMethods = 3
    MinTarget = 4
    MaxTarget = 5
    Min = 6
    Max = 7


# module methods
def isInt(n):
    try:
        int(n)
        return True
    except:
        return False


class AlgorithmData(np.ndarray):
    """
    The basic data structure of the project

    Holds all the data as well as data that is needed
    for the operations

    The following is the structure of the AlgorithmData:
    -#  Header which is composed from ndarrays that holds
        the descriptive data of the values
    -#  Data which holds the data

    -   The class inherits from np.ndarray so:
    -   The access to the data values is as for the np.ndarray
    -   The access to the header values is by stating the RowName in the first parameter
    -   There are basically 2 ways to access the data:
        -#  Generating a new AlgorithmData methods rows, cols
        -#  Generating an ndarray method __getitem__ (see doc in __getitem__ to the ways to access the data)

    Examples:
        >>> a[1,1]
        accessing data

        >>> a[RowNames.Name,1]
        accessing header data
    """

    def __new__(cls,
                data,
                names: np.chararray=None,
                rolls: np.ndarray=None,
                types: np.ndarray=None,
                normalize_methods: np.ndarray=None,
                target_min: np.ndarray=None,
                taraget_max: np.ndarray=None,
                mins: np.ndarray=None,
                maxs: np.ndarray=None,
                info=None):
        """
        Method : __init__

        This method creates the AlgorithmData object

        Args:
            data                : (numpy.ndarray or np.matrix or list)    - The data of the parameter
            names               : (numpy.chararray)  - The names of the parameters
            rolls               : (numpy.ndarray)    - The roll of the field in the algorithm
            types               : (numpy.ndarray)    - The types of the parameters
            normalize_methods    : (numpy.ndarray)    - The normalize method of the parameter
            target_min           : (numpy.ndarray)    - The normalized minimum
            targetMax           : (numpy.ndarray)    - The normalized maximum
            mins                : (numpy.ndarray)    - The unnormalized minimum
            maxs                : (numpy.ndarray)    - The unnormalized maximum
        """

        data = AlgorithmData.create_data_matrix(data)
        obj = data.view(cls)
        obj.string_length = 100

        names = AlgorithmData.adjust_char_row_length(data.shape[1], names, "Name", obj.string_length)
        rolls = AlgorithmData.adjust_row_length(data.shape[1], rolls, FieldRolls.Parameter)
        types = AlgorithmData.adjust_row_length(data.shape[1], types, FieldsTypes.RatioData)
        normalize_methods = AlgorithmData.adjust_normalize_method_row_length(normalize_methods, types)
        target_min = AlgorithmData.adjust_row_length(data.shape[1], target_min, 0)
        taraget_max = AlgorithmData.adjust_row_length(data.shape[1], taraget_max, 1)
        mins = AlgorithmData.adjust_row_length(data.shape[1], mins, 0)
        maxs = AlgorithmData.adjust_row_length(data.shape[1], maxs, 0)
        obj.evaluations = []
        obj.header = [names, rolls, types, normalize_methods, target_min, taraget_max, mins, maxs]
        return obj

    @staticmethod
    def create_data_matrix(data):
        """
        Method : create_data_matrix

        Creates the data matrix 

        The data can be :
        -#  np.matrix
        -#  np.array one dimension
        -#  np.array tow dimensions
        -#  python list that can be converted to matrix

        The output is a tow dimensions np.ndarray

        Args:
            data - The data that was given in the initialization of the AlgorithmData

        Returns:
            tow dimensions np.ndarray
            
        """
        # If the data is from type np.matrix - return
        if isinstance(data, np.matrix):
            return np.array(data)

        # If the data is from ndarray
        # If the number of dimensions is 1 convert to matrix (with one columns)
        # If the number of dimensions is 2 return the ndarray
        # Else (The dimension is larger than 2) - raise exception
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                return data.reshape((data.shape[0], 1))
            elif data.ndim == 2:
                return data
            else:
                raise ValueError("The number of dimensions is larger than 2")

        # If this is another type of parameter
        # Try to convert it to matrix
        # If the conversion succeeded convert it to ndarray
        # If that does not succeed try to convert to ndarray and convert the ndarray
        #   and reshape the array
        # If that does not work - raise exception
        try:
            data = np.matrix(data)
            return np.array(data)
        except:
            try:
                data = np.array(data)
                if data.ndim == 1:
                    return data.reshape((data.shape[0], 1))
                else:
                    raise ValueError()
            except:
                raise ValueError("The data cannot be converted to 2 dimensional array")

    def __array_finalize__(self, obj):
        """
        Method : __array_finalize__

        This method is called after the creation of AlgorithmData
        and sets the attributes from obj (which is ndarray) to self
        which is AlgorithmData
        """
        if obj is None:
            return
        self.header = getattr(obj, 'header', None)
        self.string_length = getattr(obj, 'string_length', None)

    def __array_wrap__(self, out_arr, context=None):
        """
        Method : __array_wrap__

        This method is activated after ufunc is activated on AlgorithmData
        and ensures that the object returned is AlgorithmData
        """
        return np.ndarray.__array_wrap__(self, out_arr, context)

    @staticmethod
    def adjust_row_length(desired_length: int, arr: np.ndarray, default_value) -> np.ndarray:
        """
        Method : adjust_row_length

        Adjust the length of a header row to that of the data

        -#  if the header row is None - generate an array of the default value
        -#  If the header row length and the data row length are equal - return
        -#  If the header row length is larger than the data row length - cut the header row
        -#  If the header row length is smaller to the data row length - fill with defaults

        Args:
            desired_length  : (int)              - The data row length
            arr             : (numpy.ndarray)    - The header row
            default_value    : (any)              - The value for the fill

        returns:
            numpy.adarray   :The adjusted array
        """
        if arr is None:
            return np.array([default_value for i in range(desired_length)])

        if arr.shape[0] < desired_length:
            list = [default_value for i in range(arr.shape[0])]
            list.extend([default_value for i in range(arr.shape[0], desired_length)])
            return np.array(list)

        return np.array([arr[i] for i in range(desired_length)])

    @staticmethod
    def adjust_char_row_length(desired_length: int, arr: np.chararray, default_value: str,
                            string_length: int) -> np.chararray:
        """
        Method : adjust_char_row_length

        Adjust the length of a header char row to that of the data

        -#  if the header row is None - generate an array of the default value
        -#  If the header row length and the data row length are equal - return
        -#  If the header row length is larger than the data row length - cut the header row
        -#  If the header row length is smaller to the data row length - fill with defaults

        Args:
            desired_length  : (int)              - The data row length
            arr             : (numpy.ndarray)    - The header row
            default_value    : (str)              - The value for the fill
            string_length    : (int)              - The maximum length of the item in the chararray

        returns:
            numpy.chararray   :The adjusted array
        """

        if arr is None:
            return np.char.array([default_value for i in range(desired_length)], string_length)

        if arr.shape[0] < desired_length:
            list = [arr[i] for i in range(arr.shape[0])]
            list.extend([default_value for i in range(arr.shape[0], desired_length)])
            return np.char.array(list, string_length)

        return np.char.array([arr[i] for i in range(desired_length)], string_length)

    @staticmethod
    def adjust_normalize_method_row_length(normalize_methods: np.ndarray, types: np.ndarray) -> np.ndarray:
        """
        Method : adjust_normalize_method_row_length

        Adjust the length of the normalize method row

        The difference between the normalize method row and the other rows is
        that the default normalize method is according to the field type

        -#  if the header row is None - generate an array of the default values according to the type
        -#  If the header row length and the types row length are equal - return
        -#  If the header row length is larger than the types row length - cut the header row
        -#  If the header row length is smaller to the types row length - fill with defaults according to the type

        Args:
            normalize_methods: (numpy.ndarray)    - The Normalize methods row
            types           : (numpy.ndarray)

        returns:
            numpy.ndarray   : The adjusted array
        """
        if normalize_methods is None:
            return np.array([AlgorithmData.correct_normalize_method(types[i]) for i in range(types.shape[0])])

        list = [
            AlgorithmData.correct_normalize_method(types[i], normalize_methods[i])
            for i in range(min(normalize_methods.shape[0], types.shape[0]))
        ]

        if types.shape[0] > normalize_methods.shape[0]:
            list.extend([
                AlgorithmData.correct_normalize_method(types[i]) for i in range(normalize_methods.shape[0], types.shape[0])
            ])

        return np.array(list)

    @staticmethod
    def correct_normalize_method(type: FieldsTypes, normalize_method: NormalizeMethod=None) -> NormalizeMethod:
        """
        Method : correct_normalize_method

        Returns a default normalize method according to the type

        -#  If the type is qualitative make sure that the normalize method is one of qualitative normalize method
        -#  If the type is quantitative make sure the normalize method is one of quantitative normalize method

        Args:
            Type    : (FieldTypes)              - The type of the parameter
            NormalizeMethod : (NormalizeMethod) - The normalize method currently assigned for the parameter

        Returns:
            NormalizeMethod : The adjusted normalized method

        """

        if type in (FieldsTypes.NominalData, FieldsTypes.OrdinalData):
            if normalize_method not in (NormalizeMethod.OneOfN, NormalizeMethod.QualitativeToRange,
                                       NormalizeMethod.EquilateralEncoding):
                return NormalizeMethod.OneOfN
            else:
                return normalize_method
        else:
            if normalize_method not in (NormalizeMethod.NormalizeToRange, NormalizeMethod.ReciprocalNormalization):
                return NormalizeMethod.NormalizeToRange
            else:
                return normalize_method

    def __getitem__(self, index: int):
        """
        Method : __getitem__

        -   This method returns an np.ndarray with data from the AlgorithmData
        -   The access to the AlgorithmData is by using index
        -#  If the index is int or RowNames - return a vector
        -#  The first parameter of the index represents the rows it can be:
            -#  int
            -#  RowNames
            -#  list of integers
            -#  list of integers and RowNames
            -#  slice 
        -#  The second parameter of the index represents the columns it can be:
            -#  int
            -#  string (to access the row by it's name)
            -#  FieldRolls
            -#  list of integers
            -#  list of integers and FieldRolls and strings
            -#  slice


        Args:
            index : The index of the item to retrieve

        Returns:
            any : The item

        Note:
            For row returning this method returns ndarray. 
            If you want to get AlgorithmData use rows method 

        Raises:
            IndexError : If the index is invalid

        Examples:
            >>> a[1,1]
            accessing data entry

            >>> a[RowNames.Name,1]
            accessing header data entry

            >>> a[1]
            accessing data row

            >>> a[RowNames.Name,1]
            accessing a header row

            >>> a[[1,2,5],0:2]
            returns the data found in rows 1,2,5 and columns 0,1
        """

        # if the index is int - return one row (convert the index to 2 dimensions index)
        if not isinstance(index, tuple):
            index = (index, slice(0, self.shape[1]))

        # get the columns
        cols_idx = self.cols_idx(index[1])

        # get the rows
        rows_idx = self.rows_idx(index[0])

        # Copy the data
        return self.getitems(rows_idx, cols_idx)

    def __setitem__(self, index: int, value):
        """
        Method : __setitem__

        Sets an item in the AlgorithmData

        The value has to be from the type of the item currently
        in the location pointed by the index

        Args:
            index   : always in the format of [row, column]
            value   : (any) the value to assign

        Raises:
            IndexError : If the index is invalid
            ValueError : If the value is not from the type of the data in the index location

        Examples:
            >>> a[1,1] = 0
            assigning data

            >>> a[RowNames.Name,1] = "Name"
            assigning header data
        """
        try:
            # Get the column
            index = (index[0], self.col_idx(index[1]))

            # if the index or the row is RowNames - set the field of the header
            if isinstance(index[0], RowNames):

                # the type of the value and the item in the target place has to be the same
                if PythonUtilities.compare_types(value, self.header[index[0].value][index[1]]):
                    self.header[index[0].value][index[1]] = value
                else:
                    error = "An attempt was made to insert : " + str(value) + " of type : " + str(
                        type(value)) + "\n to the row of : " + str(RowNames(index[0].value))
                    raise ValueError(error)

            # if the row index is from the data section - regular np.ndarray set
            else:
                super(AlgorithmData, self).__setitem__(index, value)
        except ValueError as e:
            raise e
        except Exception as e:
            error = "Error while retrieving from index :[" + str(index[0]) + "][" + str(
                index[1]) + "]" "\n the numpy error is :" + str(e)
            raise Exception(error)

    def col_idx(self, index):
        """
        Method : col_idx

        -   Generate the column index for __setitem__
        -   The index can be one of the following:
            -#  int - in this case the method returns it as it is
            -#  FieldRolls - In this case the method returns the column index of the column
                             if there is only one column with the FieldRoll

        Args:
            index (FieldRoll or int)    : - The index of the column
            
        Returns:
            int : The column selected
        """
        if isinstance(index, FieldRolls):
            cols_idx = self.cols_idx(index)
            if len(cols_idx) == 0:
                raise IndexError("there if no column with roll " + str(index))
            elif len(cols_idx) > 1:
                raise IndexError("There is more than one column for the roll " + str(index))
            else:
                return cols_idx[0]
        else:
            return index

    def cols_idx(self, index: Union[List[Union[int, str]], FieldRolls]):
        """
        Method : cols_idx

        Decide which columns to include in the cols and __getitem__ method

        Args:
            index  : A representation of the columns to include

        return:
            List[int] : A list of indexes of columns to extract

        """
        # If the parameter is FieldRolls - return all the column numbers with that FieldRolls
        if isinstance(index, FieldRolls):
            return np.where(self.header[RowNames.Roll.value] == index)[0].tolist()

        # If the parameter is int - return the parameter
        if isInt(index):
            return [index]

        # If the parameter is string - return all the column numbers with that name
        if isinstance(index, str):
            return np.where(self.header[RowNames.Names.value] == index)[0].tolist()

        #  - sorted
        if isinstance(index, list):
            result = []
            for entry in index:
                if isInt(entry):
                    result.append(entry)
                elif isinstance(entry, str):
                    result.extend(np.where(self.header[RowNames.Names.value] == entry)[0].tolist())
                else:
                    result.extend(np.where(self.header[RowNames.Roll.value] == entry)[0].tolist())
            return sorted(list(set(result)))

        # If the index is slice return a list of the products of the slice
        if isinstance(index, slice):
            return [idx for idx in range(*index.indices(self.shape[1]))]

        raise IndexError("The column index type is not supported " + str(type(index)))

    def rows_idx(self, index):
        """
        Method : rows_idx

        Decide which rows to include in the rows and __getitem__ method

        Args:
            index  : A representation of the rows to include

        return:
            List[int] : A list of indexes of rows to extract

        """
        # If the index is RowNames - return the index
        if isinstance(index, RowNames):
            return [index]

        # If the index is int - return the index
        if isInt(index):
            return [index]

        # If the index is a list - return a sorted list with the rows to select
        if isinstance(index, list):
            l = sorted([entry for entry in index if isinstance(entry, RowNames)], key=lambda entry: entry.value)
            l.extend(sorted([entry for entry in index if isInt(entry)]))
            return l

        # If the index is slice return a list of the products of the slice
        if isinstance(index, slice):
            return [idx for idx in range(*index.indices(self.shape[0]))]

        raise IndexError("The row index type is not supported " + str(type(index)))

    def getitems(self, rows_idx, cols_idx):
        """
        Method : get the items specified by cols_idx and row_idx

        Args:
            row_idx : a list of rows to extract
            cols_idx : A list of columns to extract

        Returns:
            np.ndarray
        """

        # If the rows_idx and cols_idx include only one index - return the item
        if len(rows_idx) == 1 and len(cols_idx) == 1:
            return self.get_value(rows_idx[0], cols_idx[0])

        # for a row create a row from the type of the fields in the row
        if len(rows_idx) == 1:
            result = []
            for cols_list_Idx in range(len(cols_idx)):
                result.append(self.get_value(rows_idx[0], cols_idx[cols_list_Idx]))
            return np.array(result)

        # for a column : if the rows contain a non float member - change all the
        # values to strings (this is because the np.array can contain fields from only one type
        if len(cols_idx) == 1:
            result = []
            allfloat = True
            for rows_list_idx in range(len(rows_idx)):
                value = self.get_value(rows_idx[rows_list_idx], cols_idx[0])
                try:
                    value = float(value)
                except:
                    allfloat = False
                result.append(value)

            if not allfloat:
                result = [str(value) for value in result]

            return np.array(result)

        # for a matrix output If one of the values is not float - return a string matrix
        result = []
        allfloat = True
        for rows_list_idx in range(len(rows_idx)):
            row = []
            for cols_list_Idx in range(len(cols_idx)):
                value = self.get_value(rows_idx[rows_list_idx], cols_idx[cols_list_Idx])
                try:
                    value = float(value)
                except:
                    allfloat = False
                row.append(value)
            result.append(row)

        if not allfloat:
            result = [[str(value) for value in row] for row in result]

        return np.array(result)

    def get_value(self, row_idx, col_idx):
        """
        Method : get_value

        Gets a single value from the AlgorithmData

        Args:
            row_idx : The row index
            col_idx : The column index

        Returns:
            The value 
        """
        if isinstance(row_idx, RowNames):
            return self.header[row_idx.value][col_idx]
        else:
            return super(AlgorithmData, self).__getitem__((row_idx, col_idx))

    def cols(self, index):
        """
        Method : cols

        Returns cols specified by index, name, roll

        The access to the cols cane be by :
        -#  int
        -#  string (to access the row by it's name)
        -#  FieldRolls
        -#  list of integers
        -#  list of integers and FieldRolls and strings
        -#  slice

        Note:
            This method returns AlgorithmData with the cols selected

        Args:
            index  : A representation of the columns to include

        Returns:
            AlgorithmData : The rows selected inside AlgorithmData
        """
        # Get a list of indexes from all input types
        index = self.cols_idx(index)

        # Remove columns indexes that are not in the AlgorithmData
        index = sorted([index[idx] for idx in range(len(index)) if index[idx] < self.shape[1]])

        header = [np.array([self.header[row][col] for col in index]) for row in range(len(self.header))]

        # Create the data
        data = np.zeros((self.shape[0], len(index)))

        # Create the AlgorithmData
        algorithm_data = AlgorithmData(data, *header)

        # Fill the new algorithm data with values
        for row in range(self.shape[0]):
            for col in range(len(index)):
                algorithm_data[row, col] = self[row, index[col]]

        # Return
        return algorithm_data

    def rows(self, index):
        """
        Method : rows

        Returns rows specified by index, name, roll

        The access to the cols cane be by :
        -#  int
        -#  RowNames
        -#  list of integers
        -#  list of integers and RowNames
        -#  slice 

        Note:
            This method returns AlgorithmData with the rows selected

        Args:
            index  : A representation of the columns to include

        Returns:
            AlgorithmData : The rows selected inside AlgorithmData
        """
        # Remove rows that are not in the AlgorithmData
        index = sorted([index[idx] for idx in range(len(index)) if index[idx] < self.shape[0]])

        # Copy the header
        header = [np.copy(self.header[idx]) for idx in range(len(self.header))]

        # Allocate place for the data
        data = np.zeros((len(index), self.shape[1]))

        # Create the AlgorithmData
        algorithm_data = AlgorithmData(data, *header)

        # Fill the algorithm_data with values
        for row in range(len(index)):
            for col in range(self.shape[1]):
                algorithm_data[row, col] = self[index[row], col]

        # Return
        return algorithm_data


class AlgorithmDataRowInterface(object):
    """
    Represent an AlgorithmData row for interface in regular indexing
    """

    def __init__(self, algorithm_data: AlgorithmData, row_index: int):
        """
        Method : __init__

        Initialize AlgorithmDataRowInterface

        Args:
            algorithm_data   : (AlgorithmData)   - The algorithm_data this interface refers to
            row_index        : (int)             - The index in the algorithmDataInterface this row represents
        """

        self.algorithm_data = algorithm_data
        self.row_index = row_index

    def convert_row_index(self):
        """
        Method : convert_row_index

        Convert the row index to the one used by the AlgorithmData

        -#  Decide if the row is a header row or data row
        -#  Convert the row index to the one used in the AlgorithmData:
            -#  Header row  -   index is converted to RowNames enum member
            -#  Data row    -   reduce the header length from the row index

        Returns:
            RowNames or int : The row index as it is used by the AlgorithmData class
        """

        if self.row_index < len(self.algorithm_data.header):
            return RowNames(self.row_index)
        else:
            return self.row_index - len(self.algorithm_data.header)

    def header_size(self):
        """
        Method : header_size

        This method returns the length of the header of the AlgorithmData

        Returns:
            int : The length of the header of the AlgorithmData
        """
        return len(self.algorithm_data.header)

    def __getitem__(self, index: int):
        """
        Method : __getitem__

        This method does the following:
        -#  If the index is FieldRoll - pass it to the algorithm_data
        -#  If the index is int
            -#  If the index is 0 - The name of the row
            -#  Else - Convert the index to the index in algorithm data (reduce 1)
        -#  return the data from the algorithm_data using the converted index


        Args:
            index   : (int or FieldRoll) - The index of the item in the row

        Returns:
            any : The value of the item retrieved
        """
        if isInt(index):
            if index == 0:
                if self.row_index < len(RowNames):
                    return str(RowNames(self.row_index))
                else:
                    return "Data " + str(self.row_index - len(RowNames))
            else:
                index -= 1

            return self.algorithm_data[self.convert_row_index(), index]

    def __setitem__(self, index, value):
        """

        Method : __setitem__

        This method does the following:
        -#  If the index is FieldRoll - pass it to the algorithm_data
        -#  If the index is int
            -#  If the index is 0 - raise error (name column is not writable)
            -#  Else convert the index for use by the algorithm_data (reduce 1)
        -# set the value to the algorithm_data using the converted index.

        Args:
            index   : (int or FieldRoll) - The index of the item in the row
            value   : (any) - The value to set
        """
        if isInt(index):
            if index == 0:
                raise ValueError("Index 0 is reserved for row name and cannot be stetted")
            else:
                index = index - 1

        self.algorithm_data[self.convert_row_index(), index] = value

    def __len__(self) -> int:
        """
        Gets the length of the row in the algorithm_data + 1 which is for the row header column
        """
        return self.algorithm_data.shape[1] + 1


class AlgorithmDataInterface(object):
    """
    This class is an interface to the AlgorithmData which simulate access like regular list

    This class is used when there is a need to access the AlgorithmData and other
    python lists in the same code

    The mechanize used to get and set data
    -#  A method from this class is called. It returns a AlgorithmDataRowInterface
    -#  It gives the AlgorithmDataRowInterface the AlgorithmData and the row
    -#  The AlgorithmDataRowInterface get the index of the column in it's __getitem__/__setitem__ method
    -#  The AlgorithmDataRowInterface composes the index np style and calls the AlgorithmData with this index

    Examples:
        >>> a[1][1]
        accessing data in the header row 1 (types)

        >>> a[7][1]
        accessing the data (starting from row - len(a.algorithm_data.header))
    """

    def __init__(self, algorithm_data: AlgorithmData):
        """
        Method : __init__

        Initialize the algorithmDataInterface - setting the AlgorithmData var
        """
        self.algorithm_data = algorithm_data

    def __getitem__(self, index: int) -> AlgorithmDataRowInterface:
        """
        Method : __getitem__

        Get a row of the Algorithm data
   
        Args:
            index   : (int) - The index of the row to retrieve

        Returns:
            AlgorithmDataRowInterface   : Interface to the row in the AlgorithmData

        Examples:
            >>> a[1][1]
            accessing data entry

            >>> a[1]
            accessing data row
        """
        return AlgorithmDataRowInterface(self.algorithm_data, index)

    def __len__(self) -> int:
        """
        Method : __len__

        Returns the length of the AlgorithmDataInterface (header + data)

        Returns:
            self.algorithm_data.shape[0] + len(self.algorithm_data.header)
        """
        return self.algorithm_data.shape[0] + len(self.algorithm_data.header)

    def cols(self, cols_to_include: Union[List[Union[int, str]], FieldRolls]):
        """
        Method : cols

        Returns :
            AlgorithmDataInterface with the columns selected
        """
        if not isinstance(cols_to_include, FieldRolls):

            # remove column 0 if exist because it contains the RowNames
            if 0 in cols_to_include:
                cols_to_include.remove(0)

            # the rest of the indexes of the cols to remove should be reduced by one
            # because the index 0 in the AlgorithmData is found in index 1 in the AlgorithmDataInterface
            cols_to_include = [
                cols_to_include[idx] - 1 if isInt(cols_to_include[idx]) else cols_to_include[idx]
                for idx in range(len(cols_to_include))
            ]

        return AlgorithmDataInterface(self.algorithm_data.cols(cols_to_include))

    def rows(self, rows_to_include: List[int]):
        """
        Method : rows

        Returns :
            AlgorithmDataInterface with the rows selected
        """
        # Remove header rows and convert the other rows to the AlgorithmData
        # indexes
        header_length = len(self.algorithm_data.header)
        rows_to_include = [rowToInclude - header_length for rowToInclude in rows_to_include if rowToInclude >= header_length]

        return AlgorithmDataInterface(self.algorithm_data.rows(rows_to_include))


class ufunc(object):
    """
    This class is a converter of ufunc methods of numpy for the use with AlgorithmData
    """

    @staticmethod
    def hstack(args: List[Union[AlgorithmData, AlgorithmDataInterface]], returnInterface: bool=False):
        """
        Method : hstack

        Horizontal concatenation of AlgorithmsData

        The results of this method is an AlgorithmData or AlgorithmDataInterface with the
        following structure

        | args[0] | args[1] | args[2] |
        |---------| --------|---------|
        | Header0 | Header1 | Header2 |
        | Data0   | Data1   | Data2   |

        Args:
            args    : list of AlgorithmData or AlgorithmDataInterface
            returnInterface : (bool) if True will return AlgorithmDataInterface else will return AlgorithmData

        Returns:
            AlgorithmData or AlgorithmDataInterface : the concatenated AlgorithmData

        """

        # If an argument is AlgorithmDataInterface - change it to AlgorithmData
        args = [arg.algorithm_data if isinstance(arg, AlgorithmDataInterface) else arg for arg in args]

        # Create a new header by concatenating all the headers of the args
        # horizontally
        header = []
        for idx in range(len(args[0].header)):
            header.append(np.concatenate([arg.header[idx] for arg in args], 0))

        # Create the data by concatenating all the data
        data = np.concatenate(args, 1)

        # Create the result - AlgorithmData
        result = AlgorithmData(data, *header)

        if returnInterface:
            return AlgorithmDataInterface(result)
        else:
            return result

    @staticmethod
    def parameters_reduction(algorithm_data: AlgorithmData):
        """
        Method : parameters_reduction

        Perform parameters reduction - shrink the number of parameters

        The parameters reduction is done from the FieldRoll.Parameters
        to the FieldRoll.Parameters Reduction columns

        Args:
            algorithm_data   (AlgorithmData) : The algorithm data to perform the parameters reduction in
        """
        # If the parameter is AlgorithmDataInterface change it to AlgorithmData
        if isinstance(algorithm_data, AlgorithmDataInterface):
            algorithm_data = algorithm_data.algorithm_data

        # Get the indexes of cols of the parameters reduction
        indexes = algorithm_data.cols_idx(FieldRolls.ParameterReduction)
        if len(indexes) == 0:
            return

        # Get the parameters columns
        parameters = algorithm_data[:, FieldRolls.Parameter]

        # Perform the parameters reduction
        pca = PCA(n_components=len(indexes))
        parameters_reduction = pca.fit(parameters).transform(parameters)

        # Copy the parameters reduction result to the algorithm data
        ufunc.copy_to(algorithm_data, parameters_reduction, [row_idx for row_idx in range(algorithm_data.shape[0])], indexes)
        

    @staticmethod
    def to_ndarray(algorithm_data: AlgorithmData):
        """
        Method :  to_ndarray

        Convert AlgorithmData to ndarray

        Args:
            algorithm_data   (AlgorithmData) : The algorithm data to converts
        """
        result = np.zeros(algorithm_data.shape)
        np.copyto(result, algorithm_data)
        return result

    @staticmethod
    def result_presentation(algorithm_data: AlgorithmData, originalResultCol, valuesOrder):
        """
        method : resultTypes

        If we have several types of result this method shrinks the types to one column
        by giving an index to each type and set the ResultPresentation column entry
        to the type calculated

        Args:
            algorithm_data   (AlgorithmData) : The algorithm data to perform
        """
        for row_idx in range(algorithm_data.shape[0]):
            algorithm_data[row_idx, FieldRolls.ResultPresentation] = \
                valuesOrder.index(originalResultCol[row_idx])

        algorithm_data.resultValues = valuesOrder

    @staticmethod
    def fill(algorithm_data: AlgorithmData, cols_to_include: Union[List[int], int, FieldRolls], value):
        """
        Method : fill

        Fills column or columns with a value

        Args:
            algorithm_data   (AlgorithmData) : The algorithm_data to change
            cols_to_include   (list of integers, int, FieldRolls) : the columns to include
            value   : The value to assign
        """
        cols_idx = algorithm_data.cols_idx(cols_to_include)
        for col_idx in cols_idx:
            for row_idx in range(algorithm_data.shape[0]):
                algorithm_data[row_idx, col_idx] = value

    @staticmethod
    def copy_to(algorithm_data, src, rows_idx, cols_idx=None):

        # Get the rows and cols idxs
        rows_idx = algorithm_data.rows_idx(rows_idx)
        if cols_idx is None:
            cols_idx = [idx for idx in range(algorithm_data.shape[0])]
        else:
            cols_idx = algorithm_data.cols_idx(cols_idx)

        # Check size compatibility
        performCopy = False

        # If there is only one row - check:
        # the size of rosIdx is 1
        # the size of cols_idx equals to the size of the row in the src
        if src.ndim == 1:
            if len(rows_idx) == 1 and len(cols_idx) == src.shape[0]:
                performCopy = True

        # If there are many rows - check the equality of the number of rows and columns
        if src.ndim == 2:
            if len(rows_idx) == src.shape[0] and len(cols_idx) == src.shape[1]:
                performCopy = True

        if not performCopy:
            raise IndexError("The shape of the source is : " + str(src.shape) + " and the destination shape id (" +
                             str(len(rows_idx)) + " , " + str(len(cols_idx)) + ")")

        if src.ndim == 1:
            for col_idx in range(len(rows_idx)):
                algorithm_data[rows_idx[0], cols_idx[col_idx]] = src[col_idx]

        if src.ndim == 2:
            for row_idx in range(len(rows_idx)):
                for col_idx in range(len(cols_idx)):
                    algorithm_data[rows_idx[row_idx], cols_idx[col_idx]] = src[row_idx][col_idx]

    @staticmethod
    def index(lst, itm):
        itm_idx = -1
        for itm_idx in range(ufunc.len(lst)):
            lst_itm = lst[itm_idx]
            if ufunc.len(lst_itm) == ufunc.len(itm):
                for in_itm_idx in range(ufunc.len(lst[itm_idx])):
                    if not lst_itm[in_itm_idx] == itm[in_itm_idx]:
                        break
                if in_itm_idx == ufunc.len(lst_itm):
                    return itm_idx
        return -1

    @staticmethod
    def len(lst):
        try:
            return lst.shape[0]
        except:
            return len(lst)
