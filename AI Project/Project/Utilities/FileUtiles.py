# Python Imports
import io
import sys
import os
import traceback
import inspect
import csv

# Third party imports
import numpy as np

# PyQt imports

# My imports


class FileUtiles(object):
    """description of class"""

    @staticmethod
    def load_algorithm_data_from_csv(filename):
        return np.genfromtxt(filename, dtype=np.dtype(str), delimiter=',')

    @staticmethod
    def GetAllFilesInFolder(dir, removeExtention=True, extention='.py'):
        """ static method : GetAllFilesInFolder

        Args:
            dir - string: The directory to take the files from
            removeExtention - bool: remove the extention from the files. default: True
            extention - string: the extension of the files to look for. default: '*.py'

        Returns:
            a list of string of the file names

        """
        result = [filename for filename in os.listdir(dir) if filename.endswith(extention)]
        if removeExtention:
            result = [filename.replace(extention, '') for filename in result]
        return result

    @staticmethod
    def loadCsv(filename):
        """ Load a CSV file. The CSV file is assumed to have column headers as the first row. The headers will be read,
            and can be used to reference individual columns.  The columns can also be referenced by index.

        """
        result = []
        first = True

        with open(filename, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    if first:
                        first = False
                        header = row
                    else:
                        result.append(row)

        # for idx in range(0, len(self.header)):
        #    self.column_map[self.header[idx]] = idx
        result.insert(0, header)
        return result

    @staticmethod
    def csvSave(filename, l, newline=''):
        try:
            with open(filename, 'w') as f:
                writer = csv.writer(f, lineterminator='\n', quoting=csv.QUOTE_ALL)
                writer.writerows(l)
            return True
        except:
            return False

    @staticmethod
    def csvLoad(filename):
        result = []
        try:
            with open(filename, 'rt') as f:
                reader = csv.reader(f)
                for row in reader:
                    result.append(row)
            return result
        except:
            return None
