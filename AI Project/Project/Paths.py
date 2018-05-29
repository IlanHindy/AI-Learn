import sys
import os

import os
DATA_PATH = "C:\ArtificialIntelligence\ArtificialIntelligence\Python\data"
ALGORITHM_DATA_PATH = os.path.join(os.path.dirname(__file__),"..", "Algorithm Data")
PROJECT_PATH = os.path.dirname(__file__)
print("****", os.path.dirname(os.path.abspath(__file__)))
for dirname, dirnames, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
    for subdirname in dirnames:
        if not "__pycache__" in subdirname:
            name = os.path.join(dirname, subdirname)  # complete directory path
            sys.path.append(name)  # add every entry to the sys.path for easy import

