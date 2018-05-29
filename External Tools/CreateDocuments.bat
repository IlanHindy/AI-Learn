REM set PATH=%PATH%;"C:\Program Files\doxygen\bin"
REM set PATH=%PATH%;"C:\ArtificialIntelligence\ArtificialIntelligence\Python\Projects\Visual Studio External Tools"
REM cd %1
PATH=%PATH%;%CD%
cd ..\docs
doxygen DoxyFile
cd html
set arg="file:///%CD%\index.html"
echo %arg%
start chrome %arg%
echo finished