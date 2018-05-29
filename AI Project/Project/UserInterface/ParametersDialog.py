"""
ParametersDialog

A dialog for inserting parameters for running an algorithm
"""
from PyQt5.QtWidgets import QDialog
from ..PyUi.Ui_ParametersDialog import Ui_ParametersDialog
from ..AI.Training.BaseTrain import BaseTrain
from ..AI.Algorithms.BaseAlgorithm import BaseAlgorithm


class ParametersDialog(QDialog, Ui_ParametersDialog):
    """
    A dialog for setting parameters for running an algorithm
    
    # Dialog Description
    
    ## Perpose
    There are 3 type of classes involves in the running of an algorithm
    -#  The RunningDialog
    -#  The train class
    -#  The algorithm class

    This dialog allows selection of the classes and set their parameters
    
    ## Structure
    -#  3 ParametersWidget for each type of class
    -#  An exit button
    
    ## Dialog working method
    -#  After initializing the ParametersWidget the dialog calls theire init method
    -#  When the exit button is pressed each dialog is asked to activate it's save file option
    -#  After the dialog was closed the calling dialog can get the parameters using methods of this dialog
    
    ## Attributes
    
    ## Activation Parameters
    parent : The RunningDialog
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.parametersWidget_dialog.init(type(parent), "Running Dialog", True)
        self.parametersWidget_train.init(BaseTrain, "Training Method")
        self.ParametersWidget_algorithm.init(BaseAlgorithm, "Algorithm")
        self.pushButton_exit.clicked.connect(self.accept)

    def dialogPrms(self):
        """
        Get the parameters of the RunningDialog
        """
        return self.parametersWidget_dialog.results()

    def trainPrms(self):
        """
        Get the parameters and type of the training class
        """
        return self.parametersWidget_train.results()

    def algorithmPrms(self):
        """
        Get the parameters and type of the algorithm
        """
        return self.ParametersWidget_algorithm.results()

    def accept(self):
        """
        slot for exiting the dialog
        """
        if not self.parametersWidget_dialog.finish():
            return
        if not self.parametersWidget_train.finish():
            return
        if not self.ParametersWidget_algorithm.finish():
            return
        super(ParametersDialog, self).accept()
