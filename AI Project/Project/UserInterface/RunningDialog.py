"""
A module for running an algorithm

The module has 2 classes
-#  RunningDialogModel : Which does the actual running of the algorithm
-#  RunningDialog which holds the GUI for running an algorithm
"""
# Python Imports
import os
import sys
import importlib
from datetime import datetime
from threading import Thread, Event
from collections import namedtuple
from queue import Queue, Empty

#from time import *
from enum import Enum

# Third party imports

# PyQt imports
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog, QApplication, QLabel
from PyQt5.QtGui import QTextCharFormat, QFont

# My imports
from .Chapter2Normalize.AlgorithmDataDesign import AlgorithmDataDesign
from .ParametersDialog import ParametersDialog
from .Parameter import ParameterInput, StdPrm
from ..PyUi.Ui_RunningDialog import Ui_RunningDialog
from ..Infrastructure.AlgorithmData import AlgorithmData
from ..UserInterface.Plugins.Widgets.MyQtPlotContainer import EvaluationsPlotHandler, ClusterPlotHandler, PlotHandler
from ..Utilities.FileUtiles import FileUtiles
from ..Utilities.PythonUtilities import PythonUtilities
from ..Utilities.PythonTools import PythonTools
from ..AI.Chapter2Normalize import Normalize
from ..Paths import DATA_PATH

# The ParametersDialog (and inside it the ParametersWidget) Gets a class (for example the BaseTrain class)
# and lets the user choose from all it's sub classes. for this to work all the sub classes has to
# be already imported and that what the following code does
# Load all the algorithm classes
dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, '..', 'AI', 'Algorithms')
thismodule = sys.modules[__name__]
for module in os.listdir(dirname):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    setattr(thismodule, module[:-3], importlib.import_module('...AI.Algorithms.' + module[:-3], __name__))

# Load all the training classes
dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, '..', 'AI', 'Training')
for module in os.listdir(dirname):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    setattr(thismodule, module[:-3], importlib.import_module('...AI.Training.' + module[:-3], __name__))

Message = namedtuple("Message",["Color", "Message"])
class Actions(Enum):
    """
    Enum for the algorithm processing steps

    Used for the communication between the model and the dialog
    """
    Load = 0
    Normalize = 1
    Init = 2
    Step = 3
    RunToEnd = 4
    Test = 5
    SciPy = 6
    SciKitLearn = 7



class RunningDialogModel(object):
    """
    Process methods of an algorithm according to requests of the dialog

    ## The sequence of processing an algorithm:
    -#    Load -  load the data from csv files to self.data_matrix self.test_data_matrix
    -#    Normalize - Show a dialog for designing the algorithm data and produce a normalized
                      self.algorithm_data and self.test_algorithm_data according to the design
    -#    Init - Activate the init method of the train  
    -#    Step/Run to end - Process the algorithm
    -#    Test - test the algorithm with test data
    -#    Scipy - Activate the scipy version of the algorithm
    -#    ScikitLearn - Activate the scikit - Learn of the algorithm

    ## Operating method  
    -#  The run method is activated by the dialog with parameter that tells which processing step is requested
    -#  The run method activate a thread with thread_main as its starting point 
    -#  The thread_main method activates the requested method (for example load, init, step etc.)
    -#  The requested method returns 4 results which are set as members of the module
        -#  self.success - If the processing succeeded  
        -#  self.result - The result of the method
        -#  self.end_message - A return message from the method
        -#  self.algorithm_message - A return message from the algorithm  
    -#  After getting the results the thread_main set an event to signal to the dialog signaling that it finished

    ## Summary of connections between the dialog and the model
    ### Variables created by the dialog
    #### Variables used for all the actions  
    -#  self.view.event - The event is initialized by the dialog and given to model in the run method.
                          The event is set by the model to signal to the dialog that the processing ended  
    -#  self.view.messages - A queue with messages from the model to be presented on the dialog                          
     
    #### Variables used for the load action
    -#  self.train - The training class name (which is converted by the method to an object from the class)
    -#  self.algorithm - The algorithm class name (which is converted by the method to an object from the class)
    -#  self.filename - The file name to load the algorithm from
    -#  self.test_filename - The file name to load the test data  

    #### Variables used by the normalized actions
    -#  self.normalize_data - The normalize data as designed by the AlgorithmDataDesign dialog
    -#  self.data_matrix - The data matrix as generated by the AlgorithmDataDesign dialog
    -#  self.test_data_matrix - The test data matrix as generated in the dialog using the same AlgorithmDataDesign dialog
    

    #### Variables used in the step/run_to_end actions
    -#  self.num_steps - The maximum number of steps to process in one step method
                         or the number of steps between 2 updates of the plot in run to end   

    #### Variables used in the test action
    -   No new variables are needed for this action from the dialog

    #### Variables used in the scipy action
    -   No new variables are needed for this action from the dialog
    
    #### Variables used in the scikitLearn action
    -   No new variables are needed for this action from the dialog
    
    ### Variables created by the model
    -#  self.success - Informs the dialog if the algorithm succeeded
    -#  self.result - The result of the running
    -#  self.end_message - A message produced by the model to inform ending of the processing  
    -#  self.algorithm_message - A message produced by the algorithm informing the result of the processing  
    -#  self.enable_actions - A dictionary that tells the dialog which actions are possible after processing
                              the current step
    
    """

    def __init__(self):
        self.init_methods_dictionary()
        self.init_enable_actions()

    def init_methods_dictionary(self):
        """
        Init a dictionary : Action -> processing method

        The methods dictionary is used by the dialog to tell the model which method (action) to run
        """
        self.methods = {
            Actions.Load: self.load,
            Actions.Normalize: self.normalize,
            Actions.Init: self.init,
            Actions.Step: self.step,
            Actions.RunToEnd: self.run_to_end,
            Actions.Test: self.test,
            Actions.SciPy: self.scipy,
            Actions.SciKitLearn: self.scikitLearn
        }

    def init_enable_actions(self):
        """
        Init a dictionary which holds which actions (processing steps) are allowed
        
        The dictionary is used by the model to tell the dialog which buttons to enable
        """
        self.enable_actions = {
            Actions.Load: True,
            Actions.Normalize: False,
            Actions.Init: False,
            Actions.Step: False,
            Actions.RunToEnd: False,
            Actions.Test: False,
            Actions.SciPy: False,
            Actions.SciKitLearn: False
        }

    def run(self, action : Actions, event: Event):
        """
        Run a step in the processing (The public method of the model)

        Start a processing thread

        Args:  
            action	: (Actions)	 - The step to activate  
            event   : (Event)  - An event to signal to the dialog that the processing ended          
        """
        self.stopEvent = event
        thread = Thread(target=self.thread_main, args=(self.methods[action],))
        thread.start()

    def thread_main(self, action_method):
        """
        The main method of the thread

        The method activate the action method and sets the following variables  
        -#  self.success
        -#  self.result      
        -#  self.end_message  
        -#  self.algorithm_message    

        At the end it sets the event to signal to the dialog that the processing finished

        Args:  
            action_method	: (method)	 - The action method to process  
                
        """
        self.success, self.result, self.end_message, self.algorithm_message = action_method()
        self.stopEvent.set()

    def load(self):
        """
        load a csv file with the data

        #### There are 2 files to load:  
        -#    For learning -  The self.fileneme variable 
        -#    For testing - The self.test_filename   variable

        Returns:  
            bool    - False if error True if ok
            bool    : False if error True if ok  
            string  - The loading end message  
            string  - The reading exception    message
        """
        try:
            self.data_matrix = FileUtiles.load_algorithm_data_from_csv(self.filename)
        except Exception as e:
            return False, False, "Error while loading algorithm data file :" + "\n" + self.filename, str(e)

        try:
            self.test_data_matrix = FileUtiles.load_algorithm_data_from_csv(self.test_filename)
        except Exception as e:
            return False, False, "Error while loading training data file :" + "\n" + self.test_filename, str(e)

        self.init_enable_actions()
        self.enable_actions[Actions.Normalize] = True
        self.stepCount = 0
        return True, True, "Finished Loading Data", ""

    def normalize(self):
        """
        normalize an algorithm data read from the file.

        #### The normalize is composed from 2 steps:  
        -#  Show a dialog in which the design of the algorithm data is done - done by the RunningDialog  
        -#  Normalize the algorithm_data and the test_algorithm_data according to the normalize data generated 
            in the dialog  
        
        Returns:  
            bool    : True
            bool    : True  
            string  : The method end message
            string  : ""  
        
        """

        # Normalize
        normalize = Normalize(self.data_matrix, self.normalize_data)
        self.algorithm_data = normalize.normalize()
        normalize = Normalize(self.test_data_matrix, self.normalize_data)
        self.test_algorithm_data = normalize.normalize()

        # Create the algorithm object and the train object
        if isinstance(self.algorithm, str):
            self.algorithm = eval(self.algorithm + "." + self.algorithm + "(self.algorithmPrms, self.algorithm_data)")
            self.train = eval(self.train + "." + self.train + "(self.trainPrms, self.algorithm, self.algorithm_data)")

        #enable buttons
        self.enable_actions[Actions.Normalize] = False
        self.enable_actions[Actions.Init] = True
        self.enable_actions[Actions.SciPy] = True
        self.enable_actions[Actions.SciKitLearn] = True

        self.view.initPlot()

        #return values
        return True, True, "Finished Normalizing Data", ""

    def init(self):
        """
        Initialize the algorithm (activating the init method of the train)
        
        Returns:  
            bool    : False if error True if ok 
            bool    : The same value as the prev return value 
            string  : The init end message  
            string  : The result message from the algorithm  
        """

        # activate the init
        self.step_idx = 0
        success, message = self.train.init()

        # enable buttons
        self.enable_actions[Actions.Init] = False
        if success:
            self.enable_actions[Actions.Step] = True
            self.enable_actions[Actions.RunToEnd] = True
            return True, True, "Finished Initialization", message
        else:
            return False, False, "Finished Initiating", message

    def step(self):
        """
        Process step/steps in the training  

        #### The following are the possible conditions to stop the loop
            -#  The number of cycles set by the dialog ended
            -#  An error occurred in the processing of the step in the train/algorithm
            -#  The algorithm finished (The check method of the train returned True)

        Returns:  
            bool    : False if error True if ok
            bool    : If the algorithm finished  
            string  : The step end message  
            string  : The result message from the algorithm  
        """
        end_idx = self.step_idx + self.num_steps
        while self.step_idx < end_idx:
            success, message, new_score, finished = self.train.step()
            if not success:
                return False, False, "The step failed ", message

            if message != "":
                if new_score:
                    self.view.messages.put(Message(Qt.yellow, str(self.step_idx) + ". " + message), block = False)
                else:
                    self.view.messages.put(Message(Qt.white, str(self.step_idx) + ". " + message), block = False)

            
            if new_score:
                self.view.plot()

            if finished:
                self.enable_actions[Actions.Step] = False
                self.enable_actions[Actions.RunToEnd] = False
                self.enable_actions[Actions.Test] = True
                return True, True, "Finished algorithm after " + str(self.step_idx) + " steps", ""

            self.step_idx += 1

        return True, False, "Finished " + str(self.step_idx) + " steps -- did not finished", ""

    def run_to_end(self):
        """
        Process the algorithm until finished

        This method activates the step method of the train in an infinite loop
    
        #### The following are the possible conditions to stop the loop
        -#  An error occurred in the processing of one of these actions
        -#  The algorithm finished (The check method of the train returned True)
            
        Returns:  
            bool    : False if error True if finished
            bool    : False if error True if finished  
            string  : The run to end - end message  
            string  : The result message from the algorithm  
        
        """

        # Perform until end of the algorithm
        while True:

            # Perform the step and return if failed
            success, message, new_score, finished = self.train.step()
            if not success:
                return False, False, "The step() failed error message :", message

            if message != "":
                if new_score:
                    self.view.messages.put(Message(Qt.yellow, str(self.step_idx) + ". " + message), block = False)
                else:
                    self.view.messages.put(Message(Qt.white, str(self.step_idx) + ". " + message), block = False)

            if new_score:
                self.view.plot()

            if finished:
                self.enable_actions[Actions.Step] = False
                self.enable_actions[Actions.RunToEnd] = False
                self.enable_actions[Actions.Test] = True
                return True, True, "Finished algorithm after " + str(self.step_idx) + " steps", ""

            self.step_idx += 1


    def test(self):
        """
        Test the algorithm with test data

        Returns:
            bool    : If the test processing was successful
            bool    : True if the test passes
            string  : The test end message
            string  : The result message from the algorithm 
        
        """
        self.enable_actions[Actions.Test] = False
        self.enable_actions[Actions.Init] = False
        success, message, result = self.train.test(self.test_algorithm_data)
        if not success:
            return False, False, "Finished Test with error " , message

        if not result:
            return True, False, "The test Failed ", message
        else:
            return True, True, "The test succeeded ", message


    def scipy(self):
        """
        Activate the scipy version of the algorithm

        -   The scipy action is using the same data as the algorithm
        -   The unchanged data is found in the self.data_matrix and self.test_data_matrix
        -   So we have to continue from there that means to generate 
            the self.algorithm_data and self.test_algorithm_data using the normalize method
        -   After it we can activate the method
        -   Because the method might destroy the algorithm_data we have to force the user to
            reload it. this is done by disabling buttons

       
        Returns:  
            bool    : False if error True if ok
            bool    : The result of the processing   
            string  : The scipy end message  
            string  : The result message from the algorithm   

        """
        # reactivate the normalize for regenerating the algorithm_data and the test_algorithm_data
        self.normalize()

        # After this action only the load action is allowed
        self.init_enable_actions()
        self.enable_actions[Actions.SciPy] = True
        self.enable_actions[Actions.SciKitLearn] = True

        # activate the scipy version of the algorithm
        success, message, result = type(self.train).scipy(type(self.algorithm), self.algorithm_data, self.test_algorithm_data)

        self.view.initPlot()

        return success, result, "Finished SciPy version of the algorithm", message

    def scikitLearn(self):
        """
        Activate the scikit - Learn version of the algorithm

        -   The scipy action is using the same data of the algorithm
        -   The unchanged data is found in the self.data_matrix and self.test_data_matrix
        -   So we have to continue from then that means to generate 
            the self.algorithm_data and self.test_algorithm_data using the normalize method
        -   After it we can activate the method
        -   Because the method might destroy the algorithm_data we have to force the user to
            reload it. this is done by disabling buttons


        Returns:  
            bool    : False if error True if ok
            bool    : The result of the processing  
            string  : The scipy end message  
            string  : The result message from the algorithm   

        """
        # reactivate the normalize for regenerating the algorithm_data and the test_algorithm_data
        self.normalize()

        # After this action only the load action is allowed
        self.init_enable_actions()
        self.enable_actions[Actions.SciPy] = True
        self.enable_actions[Actions.SciKitLearn] = True

        # activate the scipy version of the algorithm
        success, message, result = type(self.train).scikitLearn(
            type(self.algorithm), self.algorithm_data, self.test_algorithm_data)

        self.view.initPlot()

        return success, result, "Finished scikitLearn version of the algorithm", message


class RunningDialog(QDialog, Ui_RunningDialog):
    """
    running dialog for all the algorithms  
    
    # Dialog Description  
    
    ## Purpose  
    To run an AI algorithms  
    
    ## Structure  
    The dialog is composed from  
    -#  Horizontal layout that holds 2 Plot containers (viewing of a graph) 
        and a text edit for the messages
    -#  Grid layout with 4 rows (from top to button):  
        -#  labels that will be used to show the time elapse for the action activated by the 
            buttons below them 
        -#  The buttons row to activate the algorithm
        -#  labels that will be used to show the time elapse for independent actions 
        -#  The buttons row for the independent actions 
            
    ## Dialog working method  
    -#  Each one of the buttons is responsible for one step in the processing of the
        algorithm  
    -#  The steps are :  
        -#  Load   
        -#  Normalize  
        -#  Init  
        -#  Repeating steps or Run to end  
        -#  Test  
    -#  Additionally There are independent actions:  
        -#  Activate the scipy version of the algorithm  
        -#  Activating the scikit - Learn version of the algorithm  
    -#  Each button is doing:  
        -#  Get all the inputs needed for the action  
        -#  Activate the activate method  
    -#  The activate method does:  
        -#  Start a timer  
        -#  Call the run method of the model to perform the action  
    -#  While the action is running in a separate thread in the model, the timer is active in the dialog  
    -#  The timer is running as long as the model is running an action    
    -#  When the model finished an action, it sets an event  
    -#  The timer method checks the event and if it is set it does:  
        -#  Stop the timer    
        -#  Generate a finish/error message  
        -#  Set the enable attribute of the buttons according a dictionary in the model  
       
    ## Attributes  
    -#  self.model - The model of the dialog (That performs the actual operations)  
    -#  self.timer - The timer that is presenting the time and activates the end action operations  
    -#  self.action - The action to perform (set by the activate method to be sent to the model)  
    -#  self.timerLabel - Tells the timer event handler where to write the time elapsed when an action is performed  
    -#  self.timerText -  A text for the time label (set by the action method and used by the timer event handler)  
    -#  self.startTime -  The start time of the action to be used by the timer event  
    -#  self.stopEvent - The event that will be used by the model to signal to the timer that it finished  
    
    Args:
        Parent  : (QDialog) - The calling dialog
    """

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.pushButton_load.clicked.connect(self.pushButton_load_clicked)
        self.pushButton_normalize.clicked.connect(self.pushButton_normalize_clicked)
        self.pushButton_init.clicked.connect(self.pushButton_init_clicked)
        self.pushButton_step.clicked.connect(self.pushButton_step_clicked)
        self.pushButton_runToEnd.clicked.connect(self.pushButton_runToEnd_clicked)
        self.pushButton_test.clicked.connect(self.pushButton_test_clicked)
        self.pushButton_scipy.clicked.connect(self.pushButton_scipy_clicked)
        self.pushButton_scikitLearn.clicked.connect(self.pushButton_scikitLearn_clicked)
        self.pushButton_exit.clicked.connect(self.reject)
        self.model = RunningDialogModel()
        self.model.view = self
        self.setWidgetsEnable()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerEvent)
        

    @staticmethod
    def prms(widget):
        """
        This is a static method that returns the parameters that the user can set for the dialog

        The parameters are changed in the ParametersDialog dialog

        Args:
            widget: (QWidget) - The parametersWidget that is used to change the parameters
        """
        parameters = []
        parameters.append(
            StdPrm("Algorithm data file", "", False, ParameterInput.button, ["Select algorithm data file"],
                   widget.fileInput, ["Select data file", DATA_PATH, "csv file (*.csv)"]))

        parameters.append(
            StdPrm("Test data file", "", False, ParameterInput.button, ["Select test data file"], widget.fileInput,
                   ["Select test data file", DATA_PATH, "csv file (*.csv)"]))
        plotHandlers = [plotHandler.__name__ for plotHandler in PythonUtilities.inheritors(PlotHandler)]
        parameters.append(
            StdPrm("Left Plot Handler", plotHandlers[0], False, ParameterInput.comboBox, [plotHandlers],
                   widget.selectionChanged, []))
        parameters.append(
            StdPrm("Right Plot Handler", plotHandlers[0], False, ParameterInput.comboBox, [plotHandlers],
                   widget.selectionChanged, []))

        return parameters

    def setWidgetsEnable(self):
        """
        Sets the widgets enable attribute according to the allowed actions by the model

        Each action in the model decides according to it's results what are the possible actions
        that can be activated after it

        This method enable/disable the buttons according to that decision
       
        """
        self.pushButton_load.setEnabled(self.model.enable_actions[Actions.Load])
        self.pushButton_normalize.setEnabled(self.model.enable_actions[Actions.Normalize])
        self.pushButton_init.setEnabled(self.model.enable_actions[Actions.Init])
        self.pushButton_step.setEnabled(self.model.enable_actions[Actions.Step])
        self.spinBox_numSteps.setEnabled(self.model.enable_actions[Actions.Step] or \
            self.model.enable_actions[Actions.Step])
        self.pushButton_runToEnd.setEnabled(self.model.enable_actions[Actions.RunToEnd])
        self.pushButton_test.setEnabled(self.model.enable_actions[Actions.Test])
        self.pushButton_scipy.setEnabled(self.model.enable_actions[Actions.SciPy])
        self.pushButton_scikitLearn.setEnabled(self.model.enable_actions[Actions.SciKitLearn])

    def timerEvent(self):
        """
        The event activated by the timer  

        #### This method does:  
        -#  When the timer is active - Show the time elapsed from the beginning of the action    
        -#  When the event is set - Activating ending actions    
        """
        currentTime = datetime.now()
        elapsedTime = currentTime - self.startTime
        self.timerLabel.setText(self.timerText + " time: " + str(elapsedTime))
        self.addMessage()
        if self.stopEvent.isSet():
            QApplication.restoreOverrideCursor()
            self.setWidgetsEnable()
            self.generateEndMessage()
            self.timer.stop()
                

    def generateEndMessage(self):
        """
        Generate the end action message

        The inputs of the message generation is found in the model

        #### The message is generated in the following way:  
        -#  If the algorithm message is not empty add the algorithm message to the model message   
        -#  Else leave the model message  
        -#  If the step succeeded produce an information message  
        -#  Else produce an error message  
        """
        if self.model.algorithm_message == "":
            message = self.model.end_message
        else:
            message = self.model.end_message + ":\n" + self.model.algorithm_message

        if self.model.success:
            QMessageBox.information(self, "RunningDialog Information", message)
        else:
            QMessageBox.critical(self, "RunningDialog Information", message)

    
    def initPlot(self):
        """
        Initialize a plot
        """

        self.myQtPlotContainer_left.init(
            eval(self.parameters["Left Plot Handler"]["value"] + "(self.model.algorithm_data)"))
        self.myQtPlotContainer_right.init(
            eval(self.parameters["Right Plot Handler"]["value"] + "(self.model.algorithm_data)"))

    def plot(self):
        """      
        Update a plot
        """

        self.myQtPlotContainer_left.handler.drawStepResult()
        self.myQtPlotContainer_right.handler.drawStepResult()

    def addMessage(self):
        """
        Add all the messages currently in the queue to the
        PlainTextEdit

        - This method is activated while running by the timer
        - Because it is activated by the timer it is not known
          how many messages the model inserted to it between the 
          timer ticks. so we empty all the queue in a loog
        """

        while True:
            try:
                msg = self.messages.get(block = False)
                textCharFormat = QTextCharFormat()
                textCharFormat.setForeground(msg.Color)
                self.plainTextEdit_messages.textCursor().insertText(msg.Message + "\n", textCharFormat)
                self.plainTextEdit_messages.ensureCursorVisible()
            except Empty:
                break
        

    def activate(self, action: Actions, label: QLabel, text: str):
        """

        Activate an action (The timer and the appropriate action of the model)  
        
        Args:  
            action	: (Actions)	- The action to perform  
            label   : (QLabel)  - The label to write the time result in  
            text    : (string)  - The text for the time label          
        """
        self.messages = Queue()
        self.action = action
        self.timerLabel = label
        self.timerText = text
        self.startTime = datetime.now()
        self.stopEvent = Event()
        self.timer.start(100)
        self.model.run(action, self.stopEvent)

    def initRun(self):
        """
        Clear all the time labels when a load is done
        """
        self.label_loadTime.setText("")
        self.label_normalizeTime.setText("")
        self.label_initTime.setText("")
        self.label_stepTime.setText("")
        self.label_runToEndTime.setText("")
        self.stepCount = 0

    def pushButton_load_clicked(self):
        """
        Set the parameters and load the file

        -#  Activate the Running dialog to get the:
            -#  Parameters for the dialog
            -#  The training method
            -#  The parameters for the training class
            -#  The algorithm
            -#  The parameters for the algorithm
        -#  Check if algorithm data file was inserted
        """
        
        parametersDialog = ParametersDialog(self)
        if parametersDialog.exec_() == QDialog.Accepted:
            _, self.parameters = parametersDialog.dialogPrms()
            self.model.train, self.model.trainPrms = parametersDialog.trainPrms()
            self.model.algorithm, self.model.algorithmPrms = parametersDialog.algorithmPrms()
            self.model.filename = self.parameters["Algorithm data file"]["value"]
            self.model.test_filename = self.parameters["Test data file"]["value"]
            self.plainTextEdit_messages.clear()
            self.initRun()
            self.activate(Actions.Load, self.label_loadTime, "Load")

    def pushButton_normalize_clicked(self):
        """
        Normalize data and design the algorithm data

        -#  Start an algorithmDataDesign dialog  
        -#  Set the results of the algorithm data design in the model  
        -#  activate normalize action in the model (by calling to the activate method)  
        """
        # activate the algorithm_data design and set the model.data_matrix (data for the algorithm)
        algorithmDataDesign = AlgorithmDataDesign(self, self.model.data_matrix,
                                                  self.parameters["Algorithm data file"]["value"])
        algorithmDataDesign.exec_()
        self.model.normalize_data = algorithmDataDesign.normalizeData
        self.model.data_matrix = algorithmDataDesign.dataMatrix
        _, _, self.model.test_data_matrix = algorithmDataDesign.loadNormalizeData(self.model.test_data_matrix)

        # create the model
        self.activate(Actions.Normalize, self.label_normalizeTime, "Normalize")

    def pushButton_init_clicked(self):
        """
        Activate the init action of the algorithm
        """
        self.activate(Actions.Init, self.label_initTime, "Init")
        self.plot()

    def pushButton_step_clicked(self, numSteps=0):
        """
        Activate the step action of the model
        """
        self.model.num_steps = self.spinBox_numSteps.value()
        self.message = ""
        self.activate(Actions.Step, self.label_stepTime, "Step")

    def pushButton_runToEnd_clicked(self):
        """
        Activate the run to end action of the model
        """
        self.model.num_steps = self.spinBox_numSteps.value()
        self.activate(Actions.RunToEnd, self.label_runToEndTime, "RunToEnd")

    def pushButton_test_clicked(self):
        """
        Activate the test action of the algorithm

        -# Gets the file name of the test data    
        -# Set the test file name attribute of the model    
        -# Activate the test action of the model    
        """
        self.activate(Actions.Test, self.label_testTime, "Test")

    def pushButton_scipy_clicked(self):
        """
        Activate the scipy vertion of the algorithm

        -# Gets the file name of the test data  
        -# Set the test file name attribute of the model  
        -# Activate the test action of the model  
        """
        self.activate(Actions.SciPy, self.label_scipyTime, "Scipy")

    def pushButton_scikitLearn_clicked(self):
        """
        Activate the scikit - Learn version aof the algorithm

        -# Gets the file name of the test data  
        -# Set the test file name attribute of the model  
        -# Activate the test action of the model  
        """
        self.activate(Actions.SciKitLearn, self.label_scikitLearnTime, "Scikit-Learn")
        self.initPlot()
