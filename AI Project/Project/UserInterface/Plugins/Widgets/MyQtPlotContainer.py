# Python Imports
from __future__ import unicode_literals
import sys
import os
import random
from enum import Enum
import math

# Third party imports
import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from numpy import arange, sin, pi
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# PyQt imports
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSizePolicy

# My imports
try:
    from ....Infrastructure.AlgorithmData import AlgorithmData
    from ....Infrastructure.Enums import FieldRolls
except:
    if not "paths" in sys.modules:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        sys.path.append(os.path.join(dir_path, "..", "..", ".."))
        import Paths
    from AlgorithmData import AlgorithmData
    from Enums import FieldRolls


class PlotColors(Enum):
    blue = 0
    green = 1
    red = 2
    cyan = 3
    magenta = 5
    yellow = 6
    black = 7
    white = 8
    Black = 0


PlotMarkers = ('*', 'o', 'v', '^', '<', '>', '8', 's', 'p', 'h', 'H', 'D', 'd', 'P', 'X')


class MyQtPlotContainer(FigureCanvas):
    """
    Widget that contains a plot

    -   This widget is for containing a plot.
    -   It works together with a class PlotHandler to plot a graph
    -   This class is a skeleton for the plot and is common to all the plots
    -   A class that inherits from PlotHandler is responsible for all the
        subjects for generating the plot

    Example:
        # Create the widget
        myPlotContainer = MyPlotContainer()

        # Connect to PlotHandler and draw the initialize plot
        myPlotContainer.init(ExamplePlotHandler())
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axis = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)
        self.createInitialFigure()

    def createInitialFigure(self):
        line, = self.axis.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        self.drawLegend([line], ["Initialize"], 1, 1.1)
        self.draw()

    def init(self, handler):
        """
        Method : init

        -   Create the connection between this class to PlotHandler
        -   Draw the initialize plot

        Args:
            handler (PlotHandler)   - The handler for creating/changing the plot
        """
        self.handler = handler
        self.handler.container = self
        self.handler.init()
        self.handler.createInitialFigure()

    def drawLegend(self, lines, texts, ncol, scale):
        """
        Method : drawLegend

        Draws a legend at the top of the figure:
        -# get the hight limit of the values
        -# scale the height limit so that there will be a place for the legend
        -# draw the legend at the top

        Args:
            lines : The lines that are drawn in the graph
            texts : The labels of the lines
            ncol  : The number of labels in a line
            yscale : A factor that says how much to enlarge the y axis limit so that 
                     there will be a place for the legend
                    
        """
        ymin, ymax = self.axis.get_ylim()
        self.axis.set_ylim([ymin, ymax * scale])
        self.axis.legend(lines, texts, scatterpoints=1, mode="expand", ncol=ncol, fontsize=8)

    def drawValue(self, value):
        left, width = .25, .6
        bottom, height = .25, .7
        right = left + width
        top = bottom + height

        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        self.axis.text(right, top, str(value), transform=self.axis.transAxes, fontsize=14,verticalalignment='top',horizontalalignment='right',bbox=props)



class PlotHandler(object):
    """
    Class : PlotHandler

    The base class for creating/changing a plot in MyQtPlotContainer
    """

    def __init__(self, algorithm_data):
        self.algorithm_data = algorithm_data
        pass

    def init(self):
        pass

    def createInitialFigure(self):
        pass


class PlotHandlerExample(PlotHandler):
    """
    Class : PlotHandlerExample

    -   This class is an example for the creating a plot.
    -   It sets a timer and changes the plot according to random numbers
    """

    def __init__(self, algorithm_data):
        super(PlotHandlerExample, self).__init__(algorithm_data)
        self.container = None
        pass

    def init(self):
        """
        Method : init

        -   Sets a timer on the MyQtPlotContainer
        -   Connect the timer to the UpdateFigure method
        """
        self.container.timer = QTimer(self.container)
        self.container.timer.timeout.connect(self.updateFigure)
        self.container.timer.start(1000)

    def createInitialFigure(self):
        """
        Method : CreateInitialFigure
        """
        self.container.axis.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def updateFigure(self):
        """
        Method : updateFigure

        -   This Method is activated by the timer to update the graph
        -   It generate random numbers and redraw the graph
        """
        #Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.container.axis.cla()
        self.container.axis.plot([0, 1, 2, 3], l, 'r')
        self.container.draw()


class EvaluationsPlotHandler(PlotHandler):

    def __init__(self, algorithm_data):
        """
        Method : __init__
s
        Assign Member variables
        """
        super(EvaluationsPlotHandler, self).__init__(algorithm_data)
        self.container = None

    def createInitialFigure(self):
        """
        Method : createInitialFigure
        """
        self.drawFigure()

    def drawStepResult(self):
        """
        Method : drawStepResults
        """
        self.drawFigure()

    def drawFigure(self):
        """
        Method : drawFigure
        """
        self.container.axis.cla()
        self.container.axis.plot([idx for idx in range(len(self.algorithm_data.evaluations))],
                                 self.algorithm_data.evaluations, 'r')
        if len(self.algorithm_data.evaluations):
            self.container.drawValue("step = " + str(len(self.algorithm_data.evaluations) - 1) + " value = " + str(self.algorithm_data.evaluations[-1]))
        else:
             self.container.drawValue("")       
        self.container.draw()


class ClusterPlotHandler(PlotHandler):
    """
    Class : ClusterPlotHandler

    This class is a model for MyQtPlotContainer meant to compare
    the results of the clustering algorithm and the actual clustering

    The actual clustering is presented by the colors
    The result of the clustering algorithm is presented by the shape

    In order to avoid recalculation in each phase the following data is saved as members:
    -# The possible results
    -# The result types - means to which cluster in the results an entry belongs
    -# The reduced dimensions - the algorithm parameters reduced dimensions in order to
                                set the place of the shape in the graph
    -# The number of possible results
    -# The total number of combinations (the number of possible results pow 2)
    -# The labels of the options (used for the legend)
    """

    def __init__(self, algorithm_data):
        """
        Method : __init__

        Assign Member variables
        """
        super(ClusterPlotHandler, self).__init__(algorithm_data)
        self.container = None
        self.createMembers()
        self.prevStepResults = np.full(algorithm_data.shape[0], np.inf)

    def createMembers(self):
        pass
        self.possibleResults = np.unique(self.algorithm_data[:, FieldRolls.ResultPresentation])
        self.reducedDimensions = self.algorithm_data[:, FieldRolls.ParameterReduction]
        self.resultNames = self.algorithm_data.resultValues
        self.resultSize = len(self.resultNames)
        self.numOptions = int(math.pow(self.possibleResults.shape[0], 2))
        self.labels = [
            self.resultNames[int(idx / self.resultSize)] + "; #" + str(idx % self.resultSize)
            for idx in range(self.numOptions)
        ]
        self.labels = np.array(self.labels)
        self.resultPresentationIdx = self.algorithm_data[:, FieldRolls.ResultPresentation]
        self.stepResultsIdx = self.algorithm_data[:, FieldRolls.StepResult]

    def createInitialFigure(self):
        """
        Method : createInitialFigure
        """
        self.drawFigure()

    def drawStepResult(self):
        """
        Method : drawStepResults
        """
        self.drawFigure()

    def drawFigure(self):
        """
        Method : drawFigure
        """
        combinedArray = self.algorithm_data[:, FieldRolls.ResultPresentation] * 3 + self.algorithm_data[:, FieldRolls.
                                                                                                        StepResult]

        
        self.container.axis.cla()
        lines = []
        for idx in range(self.numOptions):
            line = self.container.axis.scatter(
                self.reducedDimensions[combinedArray == idx, 0],
                self.reducedDimensions[combinedArray == idx, 1],
                color=PlotColors(int(idx / self.resultSize)).name,
                marker=PlotMarkers[int(idx % self.resultSize)],
                label=str(idx))
            lines.append(line)

        self.container.drawLegend(lines, self.labels, 2, 2)
        self.container.draw()
