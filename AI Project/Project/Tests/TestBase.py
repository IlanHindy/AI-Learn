import sys
import os

try:
    from ..Utilities.PythonTools import PythonTools
except:
    if not "paths" in sys.modules:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        sys.path.append(os.path.join(dir_path, ".."))
        import Paths
    from PythonTools import PythonTools


class TestBase(object):
    """description of class"""

    def __init__(self, parentWindow):
        self.parentWindow = parentWindow
        self.checkStage = -1
        self.result = ""
        self.checks = []

    def addTest(self, test):
        self.checks.append(test)

    def createFailedResult(self, checkName, error):
        return False, checkName + " : Failed error : " + error

    def createOKResult(self, checkName, message=""):
        return True, checkName + " : OK " + message

    def getAllChecksToString(self):
        result = ""
        for idx in range(len(self.checks)):
            result += str(idx) + " : " + self.checks[idx].__name__ + "\n"
        return result

    def getAllChecksToList(self):
        result = []
        for idx in range(len(self.checks)):
            if isinstance(self.checks[idx], str):
                result.append(self.checks[idx])
            else:
                result.append(str(idx) + " : " + self.checks[idx].__name__)
        return result

    def createDisableList(self):
        result = []
        for idx in range(len(self.checks)):
            if isinstance(self.checks[idx], str):
                result.append(False)
            else:
                result.append(True)
        return result

    def headerIndexes(self):
        result = []
        for idx in range(len(self.checks)):
            if isinstance(self.checks[idx], str):
                result.append(idx)
        return result

    def check(self):
        self.inputMatrix = None
        self.outputMatrix = None
        if isinstance(self.checks[self.checkStage], str):
            return True, None, str(self.checkStage) + \
                ":" + self.checks[self.checkStage]
        else:
            try:
                result, resultString = self.checks[self.checkStage]()
                return False, result, str(self.checkStage) + ":" + resultString
            except Exception as e:
                PythonTools.printException(str(e))
                result, resultString = self.createFailedResult(self.checks[self.checkStage].__name__,
                                                               "Exception : " + str(e))
                return False, result, str(self.checkStage) + ": " + resultString
