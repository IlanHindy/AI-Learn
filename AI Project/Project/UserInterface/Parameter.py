"""
Module to handle Input parameters

This module handles 2 kinds of parameters:
-   Parameter which is an Ordered Dictionary 
-   A StdPrm which is a Parameter with all the data needed for the presentation

The module define 4 classes:
-   Parameter
-   StdPmr
-   ParameterInput which contains static methods for creating the gui input handeling to the parameters
-   StdPrmInput which is a ParameterInput with methods needed for creating the gui for StdPrm
"""
# Python Imports
import sys
import os
from typing import List, Tuple, NewType
ParameterType = NewType('ParameterType', int)
from collections import OrderedDict
from enum import Enum

# PyQt imports
from PyQt5.QtWidgets import QComboBox, QTextEdit, QPushButton, QMessageBox, QLineEdit, QWidget, QSpinBox

# My imports
try:
    from .Plugins.Widgets.MyQtEnumComboBox import MyQtEnumComboBox
    from ..Utilities.FileUtiles import FileUtiles
    from ..Infrastructure.Enums import *
except:
    if not "paths" in sys.modules:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        sys.path.append(os.path.join(dir_path, "..", "..", ".."))
        import Paths
    from Utilities.FileUtiles import FileUtiles
    from Infrastructure.Enums import *
    from Plugins.Widgets.MyQtEnumComboBox import MyQtEnumComboBox


class Parameter(OrderedDict):
    """

    This class holds parameter

    The parameter is an OrderedDict which has utility methods

    Args:
        tuples (tuples)    : pairs of string and value(any type) to fill the parameter
    """

    def __init__(self, *tuples):
        super(Parameter, self).__init__(tuples)

    def list(self) -> List:
        """

        Converts the values to list

        Returns:
            list of objects that are the values of the ordered dictionary
        """
        return list(self.values())

    def str(self) -> List[Tuple[str, str]]:
        """
        returns a list of the str presentation pf the parameter

        Returns:
            list of tuples with 2 strings : A list representing the str values of the Parameter
        """
        kl = self.keys()
        vl = self.values()
        return [str(kl[idx]) + "," + str(vl[idx]) for idx in range(len(kl))]

    def __getitem__(self, name: str) -> object:
        """
        Get an item in dictionary according to the key

        Args:
            name    : (str)  - The index

        Returns:
            Any     : The value
        """
        return super(Parameter, self).__getitem__(name)

    def __setitem__(self, name: str, value):
        """
        Sets a value in the dictionary according to the key

        Args:
            name    :(str)  - The index
            value   :(Any)  - The value
        """
        super(Parameter, self).__setitem__(name, value)

    @staticmethod
    def from_csv(filename: str) -> List['Parameter']:
        """
        Load parameters from csv

        -   The assumption is that all the parameters has the same keys
        -   The csv structure is as follows:
            -   A keys line
            -   Value lines for all the parameters

        Args:
            filename    :(str) - The file name
        """
        parameters = []
        lines = FileUtiles.csvLoad(filename)
        keys = lines[0]
        for line_idx in range(1, len(lines)):
            values = lines[line_idx]
            parameters.append(Parameter(*((keys[idx], Parameter.eval(values[idx])) for idx in range(len(keys)))))
        return parameters

    @staticmethod
    def eval(value: str) -> object:
        """
        Generate an object from a string

        The following is the problem this method meant to solve:
        -   When activating the eval method on a string it eliminates all the "'
        -   So when we read from a file we get a string with no additional "'
        -   When we save the parameters we use the str method which will save the string with no " in the file
        -   When we reread the string it will be read as a regular string (with no additional " in it) this kind of string
            will not be identified by the eval method as string
        
        Args:
            value   :(str) - The value string

        Returns: 
            Any : the object evaluated
        """
        if value == "":
            return value

        value = eval(value)
        if isinstance(value, str):
            return '"' + value + '"'
        else:
            return value

    @staticmethod
    def to_csv(parameters: List['Parameter'], filename: str):
        """
        Saves parameters from csv

        -   The assumption is that all the parameters has the same keys
        -   The csv structure is as follows:
            -   A keys line
            -   Value lines for all the parameters

        Args:
            parameters  : (List[parameter]) - The parameters to save
            filename    : (str) - The file name
        """
        lines = [parameters[0].keys()]
        for parameter in parameters:
            lines.append(Parameter.to_strs(parameter.values()))
        FileUtiles.csvSave(filename, lines)

    @staticmethod
    def to_strs(items) -> List[str]:
        """
        create a list of strings from the parameter

        The perpause of this method is to handle strings:
        -   In order to handle strings correctly in the file it should be written with "
        -   The action of saving a string removes one " or ' at the beginning and the end
        -   So this method adds a secondary " to the string
        -   "string" -> '"string"'

        Returns:
            List of strings
        """
        result = []
        for item in items:
            if isinstance(item, str):
                if len(item) > 0:
                    if not ((item[0] == '"' and item[-1] == '"') or (item[0] == "'" and item[-1] == "'")):
                        result.append('"' + item + '"')
                    else:
                        result.append(item)
                else:
                    result.append(item)
            else:
                result.append(str(item))
        return result


class StdPrm(Parameter):
    """
    This class is used for parameters setting in the ParametersWidgets

    Args:
            name    : (str) - The name of the parameters
            value   : (Any) - The value of the parameter
            changed : (bool) - If the value of this field is False that means that the parameter still have to ve changed
            build_mothod    : The method that is used to build the widget for input to the parameter
            build_method_prms   : The parameters for the build method (See the build method used for the specifications)
            slot                : The method tha is used as a slot
            slor_prms           : The values used by the slot
    """

    def __init__(self, name: str, value, changed: bool, build_method, build_method_prms, slot,
                 slot_prms):
        self.in_init = True
        super(StdPrm,
              self).__init__(("name", name), ("value", value), ("changed", changed), ("build method", build_method),
                             ("build method prms", build_method_prms), ("slot", slot), ("slot prms", slot_prms))
        self.in_init = False

    def __setitem__(self, name: str, value):
        """
        Sets a value in the dictionary according to the key

        If the attribute "value" is changed the "changed" attribute is set to false

        Args:
            name    :(str)  - The index
            value   :(Any)  - The value
        """
        super(StdPrm, self).__setitem__(name, value)
        if not self.in_init:
            if name == "value":
                super(StdPrm, self).__setitem__("changed", True)

    def check(self) -> Tuple[bool, str]:
        """
        This method is used to check whether the parameter was changed
        """
        if self["changed"]:
            return True, ""
        else:
            return False, "The " + self["name"] + " parameter have to be set"


class ParameterInput(object):
    """
    This class is responsible for utility methods  used for input to parameters
    """

    def __init__(self):
        pass

    @staticmethod
    def widgets(parameter: Parameter):
        """
        Given a parameter this method produces a list of default widgets for their input
        """
        widgets = []
        for key in parameter.keys():
            textEdit = QTextEdit()
            textEdit.setText(key)
            widgets.append(textEdit)
            if isinstance(parameter[key], Enum):
                comboBox = MyQtEnumComboBox()
                comboBox.fillValues(type(parameter[key]))
                widgets.append(comboBox)
            elif isinstance(parameter[key], bool):
                comboBox = QComboBox()
                comboBox.addItems(("False", "True"))
                widgets.append(comboBox)
            else:
                textEdit = QTextEdit()
                textEdit.setText(str(parameter[key]))
                widgets.append(textEdit)
        for widget in widgets:
            widget.setFixedHeight(30)
        return widgets

    @staticmethod
    def button(args: List, slot) -> QPushButton:
        """
        A method for creating a QPushButton for a parameter

        The arguments used by the method are found in the parameter and passed to this method
        -   args[0] - text
        -   slot - slot

        Args:
            args    : (List[Any]) - List of arguments to be used by this method (see above)
            slot    : The slot method that should be activated by the signal of the button

        Returns:
            QPushButton
        """
        button = QPushButton()
        button.setText(args[0])
        button.clicked.connect(slot)
        return button

    @staticmethod
    def lineEdit(args: list) -> QLineEdit:
        """
        A method for creating a QLineEdit for a parameter

        The arguments used by the method are found in the parameter and passed to this method
        -   args[0] - text

        Args:
            args    : (List[Any]) - List of arguments to be used by this method (see above)

        Returns:
            QPushButton
        """
        lineEdit = QLineEdit()
        lineEdit.setText(args[0])
        return lineEdit

    @staticmethod
    def comboBox(args: list, slot) -> QComboBox:
        """
        A method for creating a QComboBox for a parameter

        The arguments used by the method are found in the parameter and passed to this method
        args[0] - list of options
        slot - slot

        Args:
            args    : (List[Any]) - List of arguments to be used by this method (see above)
            slot    : The slot method that should be activated by the signal of the button

        Returns:
            QPushButton
        """
        comboBox = QComboBox()
        comboBox.addItems(args[0])
        comboBox.currentTextChanged.connect(slot)
        return comboBox

    @staticmethod
    def spinBox(args: list, slot) -> QComboBox:
        """
        A method for creating a QSpinBox for a parameter

        The arguments used by the method are found in the parameter and passed to this method
        args[int] - The step size
        slot - slot

        Args:
            args    : (List[Any]) - List of arguments to be used by this method (see above)
            slot    : The slot method that should be activated by the signal of the button

        Returns:
            QSpinBox
        """
        spinBox = QSpinBox()
        spinBox.valueChanged.connect(slot)
        spinBox.setSingleStep(args[0])
        return spinBox

class StdPrmInput(ParameterInput):
    """
    This class is used for the methods needed for presenting the StdPrm
    """
    @staticmethod
    def widgets(std_prm: Parameter) -> List[QWidget]:
        """
        -   This method generates all needed for input to the std_prm
        -   A QLineEdit for the std_prm name
        -   An input widget for the std_prm (by activating the "build_method" attribute of the parameters)
        
        Args:
            std_prm  : (Parameter) - The parameter to be presented
        """
        widgets = []

        # The name widget
        textEdit = QLineEdit()
        textEdit.setText(std_prm["name"])
        widgets.append(textEdit)

        # The input widget
        inputWidget = std_prm["build method"](std_prm["build method prms"], std_prm["slot"])
        widgets.append(inputWidget)

        # Add the input widget to the parameter
        # this field will be used to identify the parameter
        # in the slot
        std_prm["name widget"] = textEdit
        std_prm["widget"] = inputWidget
        return widgets

    @staticmethod
    def updateWidget(parameter: Parameter):
        """
        Update the widget of the parameter with the value.

        The following is the process of the update:
        -   The widget is changed
        -   The widget change activates a slot
        -   The slot changes the Parameter value
        -   This method is used to change the widget
        """
        if isinstance(parameter["widget"], QPushButton):
            parameter["widget"].setText(parameter["value"])
        elif isinstance(parameter["widget"], QComboBox):
            parameter["widget"].currentTextChanged.disconnect()
            parameter["widget"].setCurrentText(parameter["value"])
            parameter["widget"].currentTextChanged.connect(parameter["slot"])

