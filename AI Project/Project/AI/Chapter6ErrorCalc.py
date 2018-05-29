""" Error Calculation

    The purpose of this module is to produce one float which is an error estimation of an algorithm.

    -   The error is usually calculated from the expected result and the actual result
    -   The methods accepts 2 vector and produce the error from them
"""
# Python Imports
import math
from typing import List, Union

# Third party imports
import numpy as np

# PyQt imports

# My imports
from ..Infrastructure.AlgorithmData import AlgorithmData


class ErrorCalc(object):
    """
    """

    @staticmethod
    def sse(p, q):
        """ Sum Square Error

            The calculation formula is:
            \f$\sum_{i=0}^n (p_i-q_i)^2\f$.
        """
        p = AlgorithmData(p)
        q = AlgorithmData(q)
        return np.sum((p[:, 0] - q[:, 0])**2)

    @staticmethod
    def rms(p, q):
        """ Root Mean Squires

            The calculation formula is:
            \f$\sqrt{\frac{1}{n}\sum_{i=0}^n (p_i-q_i)^2}\f$.
        """
        p = AlgorithmData(p)
        q = AlgorithmData(q)
        return np.sqrt(np.mean((p[:, 0] - q[:, 0])**2))

    @staticmethod
    def sme(p, q):
        """ Mean Square Root

            The calculation formula is:
            \f$\frac{1}{n}\sum_{i=0}^n (p_i-q_i)^2\f$.
        """
        p = AlgorithmData(p)
        q = AlgorithmData(q)
        return np.mean((p[:, 0] - q[:, 0])**2)
