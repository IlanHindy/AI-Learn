import numbers
#from ..Paths import PROJECT_PATH


class PythonUtilities(object):
    """description of class"""

    def __init__(self):
        self.__dir__()

    @staticmethod
    def compare_types(value1, value2):
        if isinstance(value1, numbers.Number) and isinstance(value2, numbers.Number):
            return True
        if type(value1).__name__ == type(value2).__name__:
            return True
        return False

    @staticmethod
    def inheritors(klass: type, include_base_class: bool = False):
        """
        This class find all the subclasses of a class
        """       
        subclasses = set()
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        if include_base_class:
            subclasses.add(klass)
        return subclasses

    # @staticmethod
    # def imp(caller, called):
    #     level = len(caller.__dir__())
    #     called_path = os.path.dirname(caller.__module__.__file__)
    #     called_path.replace(PROJECT_PATH, "", 1)
    #     called_path.replace("\\", ".", 100)
    #     return called_path + "." + called.__module__.__name__, level
