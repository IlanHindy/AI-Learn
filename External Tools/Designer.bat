REM cd C:\Users\IlanH\Anaconda3\Scripts
REM call activate python36
cd "C:\ArtificialIntelligence\ArtificialIntelligence\Python\AI Project\AI Project\Project"
set PYQTDESIGNERPATH=%CD%\UserInterface\Plugins\Python
echo %PYQTDESIGNERPATH%
REM set PYTHONPATH="c:\ArtificialIntelligence\ArtificialIntelligence\Python\Projects VS Code\ArtificialIntelligence_\ArtificialInteligence"
REM set PYTHONPATH=%PYTHONPATH%;"C:\Users\IlanH\Anaconda3\envs\python36\python36.zip"
REM set PYTHONPATH=%PYTHONPATH%;"C:\Users\IlanH\Anaconda3\envs\python36\DLLs"
REM set PYTHONPATH=%PYTHONPATH%;"C:\Users\IlanH\Anaconda3\envs\python36\lib"
REM set PYTHONPATH=%PYTHONPATH%;"C:\Users\IlanH\Anaconda3\envs\python36"
REM set PYTHONPATH=%PYTHONPATH%;"C:\Users\IlanH\Anaconda3\envs\python36\lib\site-packages"
set PYTHONPATH=%CD%\UserInterface\Plugins\Widgets
set PYTHONPATH=%PYTHONPATH%;%CD%
start /B C:\Users\IlanH\Anaconda3\envs\python36\Library\bin\designer