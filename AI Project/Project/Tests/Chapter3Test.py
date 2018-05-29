# Python Imports
import sys
import os

# Thired party imports

# PyQt imports

# My imports
# try:
#     from ..Tests.TestBase import TestBase
#     from ..AI.Chapter3DistanceMetrics import DistanceMetrics
# except:
#     if not "paths" in sys.modules:
#         path = os.path.abspath(__file__)
#         dir_path = os.path.dirname(path)
#         sys.path.append(os.path.join(dir_path, ".."))
#         import Paths
#     from TestBase import TestBase
#     from Chapter3DistanceMetrics import DistanceMetrics
from ..Tests.TestBase import TestBase
from ..AI.Chapter3DistanceMetrics import DistanceMetrics


class Chapter3Test(TestBase):
    """description of class"""

    def __init__(self, parentWindow):
        super(Chapter3Test, self).__init__(parentWindow)
        self.addTest("Check select")
        self.addTest(self.check_select_from_boleans_result_1)
        self.addTest(self.check_select_from_boleans_result_0)

    def check_select_from_boleans_result_1(self):
        metrics = DistanceMetrics()
        options = [["False", "False", "False", "False", "False", "False", "False"],
                   ["True", "False", "False", "False", "False", "False", "False"]]
        prmOptions = [["False", "True"] for idx in range(7)]
        result = metrics.select(prmOptions, options, ["True", "False", "False", "False", "False", "False", "False"])
        if result != 1:
            return self.createFailedResult("check_select_from_boleans_result_1",
                                           " Result is " + str(result) + " instead of 1")
        else:
            return self.createOKResult("check_select_from_boleans")

    def check_select_from_boleans_result_0(self):
        metrics = DistanceMetrics()
        options = [["False", "False", "False", "False", "False", "False", "False"],
                   ["True", "False", "False", "False", "False", "False", "False"]]
        prmOptions = [["False", "True"] for idx in range(7)]
        result = metrics.select(prmOptions, options, ["False", "False", "False", "False", "False", "False", "False"])
        if result != 0:
            return self.createFailedResult("check_select_from_boleans_result_0",
                                           " Result is " + str(result) + " instead of 0")
        else:
            return self.createOKResult("check_select_from_boleans")
