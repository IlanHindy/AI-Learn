"""
ParametersWidget

This module defines 2 classes responsible for displaying and handling a list of parameters

\par General explanation about parameters
-#  There are 4 modules involves in setting the parameters for a class
    -#  A class that is the target of the parameters (The class that will use the parameters)
    -#  A dialog which holds a ParametersWidget for each class
    -#  A ParametersWidget for setting the parameters - This is a general perpose widget that can be used in any dialog
    -#  A Parameter module for holding the parameters - This is a general perpose module that can be used for all the parameters
-#  The parameters are initiated in a prms method of the first type
-#  When generating a parameters their has to be a definitions of all the values of the parameter
-#  In Particular 2 methods are defined
    -#  A method for generating the widget of the parameter : This is a static method in StdPrmInput. 
    -#  A method that is the slot of the widget : This is a method in the ParametersWidget. In order to set the method
        the prms() method gets the widget as a parameter
-#  If you want to program a new behavior of a parameter you should
    -#  Create a static method for generating the widget in StdPrmInput
    -#  Create a slot method in ParametersWidget
    -#  In the prms method create a parameter with these methods


\par The classes are:
-#  ParametersList - Which is responsible to hold a list of Parameter
-#  ParametersWidget - Which is responsible  for presenting the list of Parameter

\par The process of using this widget is:
-#  In the Qt designer insert the widget to the dialog
-#  The main comboBox holds a list of classes that the widget can present parameters from
    -#  Use the method init to set the base class of these classes
    -#  The activation of this method should be placed in the __init__ method of the dialog after setupUI
    -#  Each class that the widget can present the parameters from should have a prms method that returns the list of Parameter
-#  Use the results method to get the parameters and the main combo box selection    
"""
# Python Imports
from __future__ import unicode_literals
import sys
import os
from typing import List, Tuple, Union, Any

from PyQt5.QtWidgets import QWidget, QDialog, QFileDialog, QSizePolicy, QMessageBox

# My imports
# The path is needed for 2 perposes :
# For loading the modules from which the widget presents theire parameters
# When using the widget in the designer it cannot use relative imports so the path has to be
#   Created for importing the modules from this file
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
sys.path.append(os.path.join(dir_path, "..", "..", ".."))
import Paths

try:
    # These imports are used for regular activation of the program
    from ...Parameter import StdPrm, StdPrmInput
    from ....Utilities.FileUtiles import FileUtiles
    from ....Utilities.PythonUtilities import PythonUtilities
    from ....PyUi.Plugins.Widgets.Ui_ParametersWidget import Ui_ParametersWidget
except:
    # These imports are used when the widget is presented in the Qt Designer
    from Parameter import StdPrm, StdPrmInput
    from FileUtiles import FileUtiles
    from PythonUtilities import PythonUtilities
    from Ui_ParametersWidget import Ui_ParametersWidget


class ParametersList(object):
    """
    This class holds a list of standared parameters and implements some utilities on them

    Access to the parameters:
    -   By the widget of the parameter
    -   By the name of the parameter
    -   By the index of the parameter

    Args:
        parameters: (List of Parameter)
    """

    def __init__(self, parameters: List[StdPrm]):
        # remove the duplications from the list
        # insert the indexes of the duplications to a list
        to_remove = []
        for idx in range(len(parameters)):
            name = parameters[idx]["name"]
            for sIdx in range(idx + 1, len(parameters)):
                if parameters[sIdx]["name"] == name:
                    to_remove.append(sIdx)

        # generate a list only from the elements which indexes are not found in the list
        self.parameters = [parameters[idx] for idx in range(len(parameters)) if not idx in to_remove]

    def __append__(self, parameter: StdPrm):
        """
        append a parameter to the model
        """
        self.parameters.append(parameter)

    def __getitem__(self, index: Any) -> StdPrm:
        """
        get an item by index

        There are 3 types of indexes:
        -   widget
        -   str (The name of the parameter)
        -   int (The index of the parameter)

        Args:
            index: (QWidget or str or int)  - The index

        Returns:
            Any: The value of the parameter
        """
        if isinstance(index, QWidget):
            return [parameter for parameter in self.parameters if parameter["widget"] == index][0]
        elif isinstance(index, str):
            return [parameter for parameter in self.parameters if parameter["name"] == index][0]
        elif isinstance(index, int):
            return self.parameters[index]

    def __iter__(self):
        """
        Iterator over the parameters in the model
        """
        return iter(self.parameters)

    def __len__(self):
        """
        The number of parameters in the model
        """
        return len(self.parameters)

    def save(self, clss: str, filename: str):
        """
        save the parameters to csv file

        The following is the structure of the file
        -   A key line 
        -   The values of a new attribute stating the class
        -   The values of the rest of the parameters

        Args:
            clss: (str) - The name of the class presented
            filename: (str) - The name of the file to save to
        """
        # add attribute of algorithm which will be used when loading to check if the
        # file holds parameters of the class that is presented in the widget
        alg_prm = StdPrm("algorithm", clss, True, None, [], None, [])
        save_lst = list(self.parameters)
        save_lst.insert(0, alg_prm)
        StdPrm.to_csv(save_lst, filename)

    def load(self, clss: str, filename: str) -> Tuple[bool, str]:
        """
        Loads a csv file and update the parameters

        The following is the structure of the file
        -   A key line 
        -   The values of a new attribute stating the class
        -   The values of the rest of the parameters
        -   The method reads only the first 2 column of each line
        -   The first line which contains the keys of the parameters is skipped
        -   The class of the file is checked (with the parameter) if they are not the same - an error returned
        -   For each of the rest of the lines the suitable parameter (identified by the name which is the first column) is updated

        Args:
            clss: (str) - The name of the class
            filename : (str) - The file name

        Returns:
            bool - If the algorithm is the same one as the one presented in the dialog
            str - Error message

        """

        # load the csv
        lines = FileUtiles.csvLoad(filename)

        # check if the file is from the same algorithm as the selected algorithm
        # the first line holds the algorithm's name
        if clss != eval(lines[1][1]):
            return False, "The current class is " + clss + " and the file is for :" + lines[1][1]

        # load the parameters
        # the parameters starts from line 2
        for line in lines[2:]:
            self[eval(line[0])]["value"] = "" if (line[1] == "") else eval(line[1])

        return True, ""

    def finish(self) -> Tuple[bool, str]:
        """
        -   This method checks if all the parameters got leagal values
        -   The check is done by activating the check method of each parameter

        Returns:
            bool:   If all the check succeeded
            str:    The error message
        """
        for std_prm in self.parameters:
            result, message = std_prm.check()
            if not result:
                return result, message
        return True, ""


class ParametersWidget(QWidget, Ui_ParametersWidget):
    """
    This widget is responsible for presenting and changing attributes
    
    # Dialog Description
       
    ## Perpose
    To set parameters for a class 
    
    ## Structure
    -#  A main combo box for selecting the target class for the parameter
    -#  A Grid in scroll area with 2 columns:
        -#  The parameter name
        -#  The parameter setting widget
    -#  A horizontal layout with the buttons:
        -#  Reset
        -#  Load
        -#  Save
        -#  A LineEdit with the name of the file
    
    ## Widget working method
    -#  After the widget was loaded the method init is called
    -#  The init gets 2 main parameters:
        -#  The base class
        -#  The label for the widget
    -#  The init gets all the inheritors of the base class saves them and 
        fill there names in the MainComboBox
    -#  When the MainComboBox is filled the slot of the ComboBox is activated 
    -#  The slot of the combo box gets the parameters of the target class
        by importing it and activating the prms method of it
    -#  The slot calls the StdPrmInput.widgets to creates the widgets for each parameters
        and filles the grid
    -#  Now the user can change the values of the parameters
    -#  The attributes can also be changed by the buttons
    -#  If the user changes the selection in the MainComboBox the slot method start again

    ##  File save and load handling
    ### The file structure
    -#  The first line of the file is the names (keys) of the attributes
    -#  The second line of the file is a standared attribute that contains the target class
    -#  The rest of the lines are the values of the standared parameters

    ### The loading
    -#  Check if the module is the same between the MainComboBox and the file (second line)
    -#  Change the values of the parameters. The changing is done in the following way:
        -#  The first column is the name of the parameter 
        -#  The second column is the value of the parameter
        -#  The insertion is : model[Name]["value"] (using indexers on the ParametersList and Parameter)
   
    ## Attributes
    -#  filename - The name of the file of the last save or load operation
    -#  noSaveQuestion - Used to set is a question for saving should be done
    -#  model - The ParametersList
    
    ## Activation Parameters
    None
    """

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.noSaveQuestion = True
        self.model = None
        self.filename = Paths.ALGORITHM_DATA_PATH
        self.comboBox_main.currentTextChanged.connect(self.comboBox_main_currentTextChanged)

        self.pushButton_save.clicked.connect(self.pushButton_save_clicked)
        self.pushButton_load.clicked.connect(self.pushButton_load_clicked)
        self.pushButton_reset.clicked.connect(self.pushButton_reset_clicked)

    def init(self, baseClass: type, label: str, includeBaseClass: bool = False):
        """
        Fill the ComboBox with the possible classes (Inherited from the baseClass parameter)

        Args:
            baseClass: (type) - The class that all it's inheritors will be options in the MainComboBox
            label: (str)  - The label of the widget
            includeBaseClass: (bool) - If to include the base class in the list of classes

        """
        self.classes = PythonUtilities.inheritors(baseClass, includeBaseClass)
        self.label_header.setText(label)
        self.comboBox_main.addItems([cls.__name__ for cls in self.classes])

    def setModel(self, selection: str):
        """
        After class selection or in init create the ParametersList and fill the grid

        Args:
            selection: (str) - The selection of the MainComboBox
        """
        # Delete all the widgets from the grid
        self.deleteAll()

        # Create the ParametersList using the prms method of the calling dialog
        if len(self.classes):
            for cls in self.classes:
                if cls.__name__ == selection:
                    break
            self.model = ParametersList(cls.prms(self))
        else:
            return

        # For each parameter:
        # Get the widgets and put them in the grid
        for parameterIdx in range(len(self.model)):
            widgets = StdPrmInput.widgets(self.model[parameterIdx])
            for widgetIdx in range(len(widgets)):
                widgets[widgetIdx].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.gridLayout_parameters.addWidget(widgets[widgetIdx], parameterIdx + 2, widgetIdx)

    def deleteAll(self):
        """
        Empty the grid
        """
        if self.model != None:
            for parameter in self.model:
                parameter["name widget"].deleteLater()
                parameter["widget"].deleteLater()

    def fileInput(self):
        """
        This method is used as a slot to the signal from the button of the parameter

        The perpose of this method is to get a filename
        """
        stdPrm = self.model[self.sender()]
        fname = QFileDialog.getOpenFileName(self, stdPrm["slot prms"][0], stdPrm["slot prms"][1],
                                            stdPrm["slot prms"][2])
        if fname[0] == '':
            return
        else:
            stdPrm["value"] = fname[0]
            stdPrm["widget"].setText(fname[0])

    def selectionChanged(self, selection: str):
        """
        This method is used as a slot to the signal from the ComboBox of the parameter

        The perpose of this method is to set the new value of the parameter

        Args :
            selection: (str) - The selection of the combo box
        """
        self.model[self.sender()]["value"] = selection

    def spinValueChanged(self, value: int):
        """
        This method is used as a slot to the signal from the SpinBox of the parameter

        The perpose of this method is to set the new value of the parameter

        Args :
            value: (int) - The value of the spin box
        """
        self.model[self.sender()]["value"] = value

    def comboBox_main_currentTextChanged(self, selection: str):
        """
        A new algorithm was selected

        -#  Ask the user if he wants to save the current data
        -#  Create a new ParametersList and refill the grid
        """
        self.saveQuestion()
        self.setModel(selection)

    def pushButton_save_clicked(self):
        """
        A slot for the Save button

        -#  Get the file name with a dialog
        -#  Set the self.filename
        -#  Activate the save of the ParametersList
        -#  Update the filename label
        """
        fname = QFileDialog.getSaveFileName(self, "Select file", self.filename, "csv file (*.csv)")
        if fname[0] == '':
            return
        else:
            self.filename = fname[0]
            algorithm = self.comboBox_main.currentText()
            self.model.save(algorithm, fname[0])
            self.label_file.setText(os.path.basename(self.filename))

    def pushButton_load_clicked(self):
        """
        A slot for loading file button

        -#  Get the file name
        -#  Call the load method of the model to load the file data to the parameters
        -#  If the load failed (The classes are not the same) show MessageBox
        -#  Update the dialog with the data

        """
        fname = QFileDialog.getOpenFileName(self, "Select file", self.filename, "csv file (*.csv)")
        if fname[0] == '':
            return
        else:
            self.filename = fname[0]
            algorithm = self.comboBox_main.currentText()
            result, *message = self.model.load(algorithm, fname[0])
            if not result:
                QMessageBox.critical(self, "ParametersDialog Message", message[0])
            self.updateWidgets()
            self.label_file.setText(os.path.basename(self.filename))

    def pushButton_reset_clicked(self):
        """
        A slot for the reset button

        Reread the prms from the selected class
        """
        self.saveQuestion()
        clss = self.comboBox_main.currentText()
        self.setModel(clss)

    def pushButton_exit_clicked(self):
        """
        A slot for the exit button
        """
        self.saveQuestion()
        self.accept()

    def saveQuestion(self):
        """
        Save the data before all the operations that change it
        """
        selection = self.comboBox_main.currentText()
        if not self.noSaveQuestion:
            qresult = QMessageBox.question(self, "ParametersWidget Message",
                                           "Do you want to save the existing data for " + selection + " first?",
                                           QMessageBox.Yes, QMessageBox.No)
            if qresult == QMessageBox.Yes:
                self.pushButton_save_clicked()
        else:
            self.noSaveQuestion = False

    def updateWidgets(self):
        """
        Update all the widgets in the parameters with the value in the value field of the parameter
        """
        for parameter in self.model:
            StdPrmInput.updateWidget(parameter)

    def results(self):
        """
        Returns the results of the parameter
        """
        return self.comboBox_main.currentText(), self.model

    def finish(self) -> bool:
        """
        Check if all the parameters are correct and save the parameters in a file (if needed)
        """
        result, message = self.model.finish()
        if result:
            self.saveQuestion()
            return True
        else:
            QMessageBox.critical(self, "ParametersWidget : " + self.comboBox_main.currentText(), message)
            return False
