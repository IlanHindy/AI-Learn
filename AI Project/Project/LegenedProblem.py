# Thired party imports
import matplotlib
import matplotlib.pyplot as plt
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
import numpy as np
import numpy.random as random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

fig, axis = plt.subplots()


def drawFigure():
    """
        Method : CreateInitialFigure
        """
    # input arrays
    # The perpouse is to show results from 2 arrays:
    # resultTypes - shown by theire colors
    # step result types - shown by theire shape
    # For eche there are 3 possible values. each value is a list of 3 0 or 1
    possibleResults = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    resultTypes = random.randint(0, 3, 100)
    stepResultTypes = random.randint(0, 3, 100)
    reducedDimentions = np.array([random.random(100), random.random(100)])
    reducedDimentions = reducedDimentions.transpose()

    # Create an array with values 0..8
    #entries = np.array([[int(idx / 3), idx % 3] for idx in range(possibleResults.shape[0])])
    entries = np.arange(9)
    combinedArray = np.array(
        [resultTypes[idx] * 3 + stepResultTypes[idx] for idx in range(resultTypes.shape[0])])
    colors = ['navy', 'turquoise', 'darkorange']
    target_names = ["one", "two", "Three"]
    lw = 2
    markers = [u'+', u'^', u'o']

    axis.cla()
    lines = []
    texts = []
    for idx in entries:
        line = axis.scatter(
            reducedDimentions[combinedArray == idx, 0],
            reducedDimentions[combinedArray == idx, 1],
            color=colors[int(idx / 3)],
            marker=markers[int(idx % 3)],
            label=str(idx))
        lines.append(line)
        texts.append(str(idx))
    axis.legend(lines, texts, scatterpoints=1, loc='lower left', ncol=3, fontsize=8)
    plt.show()


drawFigure()
