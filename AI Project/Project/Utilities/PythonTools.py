import io
import sys
import os
import traceback
import inspect
try:
    from ..Infrastructure.Enums import *
except:
    from Enums import *
import copy
from collections import OrderedDict
from builtins import reversed


class PythonTools(object):
    """class : PythonTools

        Tools to be used for python
    """

    @classmethod
    def printException(self, title, message=""):
        """ static method : PrintException

        print an exception data

        Args:
            title - string: The title for the message window
            message - string: The message of the error default: ""

        Returns:
            None.
        """

        exc_type, exc_value, exc_traceback = sys.exc_info()
        stackEntries = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print(title + '\n', message + '\n', * [stackEntry + '\n' for stackEntry in stackEntries])

        #titleTextBlock = CustomizedMessageBox.SetTextBlock([title, Font(fontSize = 16, fontWeight = FontWeights.Bold)])
        # CustomizedMessageBox.Show(
        #    [titleTextBlock, message + self.GetStackEntries(stackEntries)], title,
        #    None, Icons.Error)

    @classmethod
    def GetStackEntries(self, stackEntries=None):
        """ static method : GetStackEntries

        The method gets the stack entries (If not given as parameters)
        and formats them for printing

        Args:
            stackEntries - list of strings: The stack entries if already retrieved. default: None.

        Returns:
            list of strings represent the stack entries
        """

        # Get the path of this file
        path = os.path.realpath(__file__)

        # Remove the file name from the path
        path = os.path.dirname(path)

        # remove the PythonTools directory leaving the main project directory
        path = os.path.dirname(path)

        # Get the stack entries
        if stackEntries is None:
            stackEntries = []
            for idx in range(len(inspect.stack())):
                moduleName, className, methodName, lineNumber = self.GetStackEntry(idx)
                stackEntries.append(
                    moduleName.replace(path, "") + "." + className + "." + methodName + "\t" + str(lineNumber) + "\n")
            stackEntries.reverse()

        # remove the path from the entries leaving only the sub directory and the file name
        # in each entry
        # Add all the entries to one string
        result = ""
        for stackEntry in stackEntries:
            startPathIndex = stackEntry.find("\"")
            if startPathIndex != -1:
                endPathIndex = startPathIndex + len(path)
                stackEntry = stackEntry[0:startPathIndex] + \
                    stackEntry[endPathIndex + 1:len(stackEntry)]
            result += stackEntry
        return result

    @classmethod
    def MaxRank(self, value):
        """ static method : MaxRank

        Recursive function that checks the maximum rank

        Args:
            value: the element to take the rank of

        Returns
            0: If the value is not a list
            max the rank of all the elements in the list + 1: If the value is a list
        """
        if type(value).__name__ == 'StandaredMatrix' or type(value).__name__ == 'StandaredVector':
            value = value._inner_list

        if not isinstance(value, list):
            return 0
        elif len(value) == 0:
            return 1
        else:
            return max([self.MaxRank(value[idx]) + 1 for idx in range(len(value))])

    @classmethod
    def CheckTypes(self, parameters, printErrorMessage, options):
        """static method : CheckTypes

            Check a list of parameters for types options

            Args:
                parameters : a list of the values of the parameters passed to
                             the function. can be retrieved by calling locals().values()
                             after the definition of the function
                variableNumberOfParameters - bool : True if there is a variable number of parameters
                printErrorMessage - bool : True if printing error message is needed in case of error
                options : a parameter for each acceptted option of types for the parameters
                          each option can be:
                          a type if there is only one parameter and one type option
                          a list of types if there are several parameters each one has one type option
                          a list composed from types or a list of types. If the entry is a type
                            That meens that there is one acceped type for the parameter
                            If the entry is a list of types one of the types has to be accepted
            Returns:
                int: The option selected
                -1: if no option was selected

            Examples:
                 >>> CheckTypes(locals().values(), False, True, int)
                 One parameter and one option:

                 >>> CheckTypes(locals().values(), False, True, [int, bool])
                 Two parameters with one option for each:

                 >>> CheckTypes(locals().values(), False, False, [[int, bool], [float, str]])
                 Two parameters each one has 2 options
                 Do not show error Message

                 >>> CheckTypes(locals().values(), False, True, [int, float], [[int, bool], [str, float]])
                 Two parameters with 2 options in the first option there is one type option for each parameter
                 And in the second option there is 2 type options for each parameter

                 >>> CheckTypes(locals().values(), True, [int, int], [float, bool, int])
                 Variable number of arguments. there are 2 options one accepts 2 parameters and the other accepts
                 3 parameters. In each option there is one possible type for each parameters

                 >>> CheckType([parameter1, parameter2], [int, int], [float, int])
        """
        # Check if all the keys in the options list are in the parameters
        for option in options:
            for parameterName in option.keys():
                if parameterName not in parameters.keys():
                    raise ValueError("The parameter name : " + parameterName + " is not one of the method parameters")

        # options is a list of option
        # option is a dictionary : parameterName : a list of optionForParameter
        # optionForParameter is a list of types
        # Here we replace the type with a list [type, True] in order to be able to show wher the
        # check failed
        options = [
            {
                parameterName: [
                    # generate a list for each value
                    [[typeForValue, True] for typeForValue in optionForParameter]
                    for optionForParameter in option[parameterName]
                ]  # generate a list of options for parameter
                for parameterName in option
            }  # generate a dictionary for each option
            for option in options
        ]

        for idx in range(len(options)):
            option = options[idx]
            if self.CheckOption(parameters, option):
                return idx
        if printErrorMessage:
            self.PrintCheckTypesError(parameters, options)
        return -1

    @classmethod
    def GetStackEntry(self, stackFrameIdx):
        """ static method : GetCallerName

            Gets the name of the method that called CheckTypes

            Args:
                stackFrameIdx - int:

            Returns:
                The method name
        """
        stack = inspect.stack()
        parentframe = stack[stackFrameIdx][0]
        moduleName = inspect.getmodule(parentframe).__name__
        if 'self' in parentframe.f_locals.keys():
            className = parentframe.f_locals['self'].__class__.__name__
        else:
            className = ""
        methodName = inspect.stack()[stackFrameIdx][3] + "()"
        lineNumber = inspect.stack()[stackFrameIdx][2]
        return moduleName, className, methodName, lineNumber

    @classmethod
    def PrintCheckTypesError(self, parameters, options):
        """ static method : PrintCheckTypesError

        Print the error detected by CheckTypes

        Args:
            callerClassName: The name of the class of the calling method
            parameters - list: list of parameters that's types were checked
            optons - list: the options for the parameters

        Returns:
            None
        """
        messages = []
        messages.append(" The parameters are:")
        parametersString = ""
        for parameter in parameters:
            parametersString += str(parameter) + ":" + \
                type(parameter).__name__ + "  "
        messages.append(parametersString[:])
        messages.append("The options are:")
        for option in options:
            textBlockParameters = []
            for optionsForParameter in option:
                textBlockParameters.append("[")
                for optionForParameterKey in optionsForParameter:
                    if optionsForParameter[optionForParameterKey] == False:
                        textBlockParameters.append([optionForParameterKey.__name__, Font(foreground=Brushes.Red)])
                    else:
                        textBlockParameters.append(optionForParameterKey.__name__)
                    textBlockParameters.append(" or ")
                textBlockParameters = textBlockParameters[:len(textBlockParameters) - 1]
                textBlockParameters.append("]")
            messages.append(CustomizedMessageBox.SetTextBlock(*textBlockParameters))

        # get the caller function module name and function name
        callerModuleName, callerClassName, callerMethodName, callerLineNumber = self.GetStackEntry(3)
        callerNameTextBlock = CustomizedMessageBox.SetTextBlock([
            "Error in passing parameters to " + callerModuleName + "." + callerClassName + "." + callerMethodName +
            " at line " + str(callerLineNumber),
            Font(fontWeight=FontWeights.Bold)
        ])
        CustomizedMessageBox.Show([self.GetStackEntries()] + [callerNameTextBlock] + messages, "Parameters errors",
                                  None, Icons.Error)

    @classmethod
    def CheckParameterType(self, parameterValue, optionsForParameter):
        """static method : CheckParameterType

          Get a parameter and check if it is from one of the types

          Args:
            parameter : the parameter to check
            optionsForParameter : a list of possible types

          Returns:
            The true option index : if found - the index in the list of the first correct type
            -1 : if not found
         """
        # All the parameter values are handled like a list of values
        if isinstance(parameterValue, str):
            parameterValue = [parameterValue]
        else:
            try:
                len(parameterValue)
            except:
                parameterValue = [parameterValue]

        # each options for a parameter is a dictionary in which :
        # The expected type of the parameter is a key
        # True is the value
        # The parameterValue is a list of values
        # In order that an option will be accepted all the types of the
        # parameterValue element has to be from the type of the key of the
        # dictionary
        for optionForParameter in optionsForParameter:
            if len(optionForParameter) != len(parameterValue):
                for idx in range(len(optionForParameter)):
                    optionForParameter[idx][1] = False
                continue
            if all([
                    self.checkValueType(parameterValue[idx], optionForParameter[idx])
                    for idx in range(len(parameterValue))
            ]):
                return optionsForParameter.index(optionForParameter)

        return -1

    def checkValueType(value, valueType):
        # If the parameter is int it has to be acceped by float and long
        floatName = float.__name__
        intName = int.__name__
        if valueType[0].__name__ in (floatName, intName) and type(value).__name__ in (intName):
            return True

        # for the rest of the types an exact much needed
        if type(value).__name__ == valueType[0].__name__:
            return True
        else:
            valueType[1] = False
            return False

    @classmethod
    def CheckOption(self, parameters, option):
        """static method : CheckOption

        Check if a list of parameters is accepted by an option

        Args:
            parameters : a list of parameters for values check
            option : a list in which in each entry there is possible types for each parameter

        returns:
            True: if the optionTypes acceptes the parameters
            False: otherwise
        """
        return all([
            self.CheckParameterType(parameters[parameterName], option[parameterName]) != -1 for parameterName in option
        ])

    @classmethod
    def CheckUniformList(self, checkName, listPrm, printErrorMessage, *options):
        """static method : CheckUniformList

        Check if all elements in a list are from allowed type and the same type

        Args:
            checkName - string : A description of the check for the error message
            listPrm - list : the list to check
            printErrorMessage - bool : If to print error message
            option : a list of options for the parameter

        returns:
            -1  : In case of error
            int : the option selected
        """

        # Check if the list is not empty and if the parameters is a list
        try:
            if len(listPrm) == 0:
                self.PrintCheckUniformListError(checkName, printErrorMessage, "The list is empty", -1, listPrm, options)
                return -1
        except:
            self.PrintCheckUniformListError(checkName, printErrorMessage, "The parameter is not a list", -1, listPrm,
                                            options)
            return -1

        optionsDictionary = OrderedDict([(option, False) for option in options])
        selectedOption = self.CheckParameterType(listPrm[0], optionsDictionary)

        if selectedOption == -1:
            self.PrintCheckUniformListError(checkName, printErrorMessage,
                                            "The Type of the first element is not one of the options", -1, listPrm,
                                            options)
            return -1

        # Check that all the elements in the list are from the same type as the
        # first
        for elementIdx in range(len(listPrm)):
            if self.CheckParameterType(listPrm[elementIdx], optionsDictionary) != selectedOption:
                self.PrintCheckUniformListError(
                    checkName, printErrorMessage,
                    "The Type of the first element is not equal to the type of element idx :" + str(elementIdx),
                    elementIdx, listPrm, options)
                return -1

        return selectedOption

    @classmethod
    def PrintCheckUniformListError(self, checkName, printErrorMessage, errorMessage, errorElementIdx, listPrm, options):
        """static method : PrintCheckUniformListError

        Show the error of CheckUniformList

        Args:
            checkName - string : The name of the check
            printErrorMessage - bool : Whether to show error message
            errorMessage - string : A description of the error
            errorElementIdx - int : The index of the element that the type check failed for
            listPrm - list : The list of the parameters
            options - list : the list of possible type options

        returns:
            None.
        """
        # return if the indication to print error message is false
        if not printErrorMessage:
            return

        messages = []

        # The name of the check
        messages.append(CustomizedMessageBox.SetTextBlock([checkName, Font(fontWeight=FontWeights.Bold)]))

        # The stack entries
        messages.extend([self.GetStackEntries()])

        # The calling method
        moduleName, className, methodName, lineNumber = self.GetStackEntry(3)
        messages.append(
            CustomizedMessageBox.SetTextBlock([
                "Error in passing parameters to " + moduleName + "." + className + "." + methodName + "()",
                Font(fontWeight=FontWeights.Bold)
            ]))

        # The error message
        messages.append(errorMessage)

        # The options
        optionsString = ""
        for option in options:
            optionsString += option.__name__ + ', '
        optionsString = optionsString[:len(optionsString) - 2]
        messages.append("\n The options for the type are: \n " + optionsString)

        # Print the list. the failure element will be painted in red
        # If not a list or empty list do not print anything
        try:
            if len(listPrm) == 0:
                raise

            messages.append("\n The list is")
            listElementsData = [" "]
            for elementIdx in range(len(listPrm)):
                elementString = str(listPrm[elementIdx]) + ":" + type(listPrm[elementIdx]).__name__
                if elementIdx == errorElementIdx:
                    listElementsData.append([elementString, Font(foreground=Brushes.Red)])
                else:
                    listElementsData.append(elementString)
                listElementsData.append(', ')
            listElementsData = listElementsData[:len(listElementsData) - 1]
            messages.append(CustomizedMessageBox.SetTextBlock(*listElementsData))
        except:
            pass

        # Show the message box
        CustomizedMessageBox.Show(messages, checkName, None, Icons.Error)

