from collections import OrderedDict
import numpy as np


class LongTermMemory(OrderedDict):

    def __init__(self, *tuples):
        super(LongTermMemory, self).__init__(tuples)

    def clone(self):
        self.copy = OrderedDict()
        for key in self.keys():
            self.copy[key] = np.copy(self.__getitem__(key))

    def reverse(self):
        for key in self.copy.keys():
            self.__setitem__(key, self.copy[key])
