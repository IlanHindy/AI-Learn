REM cd C:\Users\IlanH\Anaconda3\Scripts
REM call activate python36
echo the first parameter is %1
echo the second parameter is %2
REM echo the thired parameter is %3
cd C:\ArtificialIntelligence\ArtificialIntelligence\Python\AI Project\AI Project\Project 
if "%~2"==""  (
	echo 1 parameter
	pyuic5 Ui\%1.ui -o PyUi\Ui_%1.py
) else (
	echo 2 parameters
	echo %1
	REM echo %internalPath%
	pyuic5 "Ui\%~1\%2.ui" -o "PyUi\%~1\Ui_%2.py"
)
echo finished

