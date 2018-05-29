"""
This program is activating package documents in doxygen
For doxygen in order to identify a package documentation it needs the string "## @package " at the beginning of the file
But the doxypypy has a bug that the documentation of a package begins with "## @brief"
so this program checks if there is a "## @brief" at the beginning of the file and if there is it replaces it with "## @package "
The program is activated in pipe after doxypypy (see py_filter.bat)
The pipe adds <cr> to each line ends. so the program replaces each <cr><cr> with a single <cr>
"""

import sys
import os
import string
# f = open("C:\\Temp\\testfile.txt", "a")
# f.write("-------------------\n")
# f.write("argv[1] = " + sys.argv[1] + "\n")
# f.write("filename = " + filename + "\n")

filename = os.path.basename(sys.argv[1])
filename = filename.replace(".py", "")
#f.write("filename = " + filename + "\n")
data = sys.stdin.read()
#f.write("To Remove :" + data[0:9])
if data[0:9] == "## @brief":
    #f.write("Module identified + \n")
    data = "## @package " + filename + "\n\n" + "#" + data[9:]
    #f.write(data)

lines = data.split("\n\n")
result = ""
for line in lines:
    result += line + "\n"

# if filename == "ParametersDialog" or filename == "RunningDialog":
#     f.write("++++++++++++++++++++++++++++++++\n")
#     f.close()
#     g = open("c:\\Temp\\" + filename + ".py", "w")
#     g.write(result)
#     g.close()
sys.stdout.write(result)

#data = data.replace(data, "\n\n\r", "\n", 10000)
#print(data)

#
#
#sys.stdout.write(
#    "*****************************************************************")
