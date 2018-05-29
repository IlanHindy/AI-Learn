$cwd = (Get-Item -Path ".\" -Verbose).FullName
cd "C:\ArtificialIntelligence\ArtificialIntelligence\Python\AI Project\AI Project\Project"
$aaa = (Get-Item -Path ".\" -Verbose).FullName
$PYTHONPATH = $aaa
$PYTHONPATH += ";" + $aaa + "\PyUi"
$PYTHONPATH += ";" + $aaa + "\Infrastructure"
$PYTHONPATH += ";" + $aaa + "\Utilities"
$PYTHONPATH += ";" + $aaa + "\Tests"
$PYTHONPATH += ";" + $aaa + "\AI"
$PYTHONPATH += ";" + $aaa + "\PyUi\Chapter 2 - Normalize"
$PYTHONPATH += ";" + $aaa + "\PyUi\Chapter 3 - Distance Metrics"
$PYTHONPATH += ";" + $aaa + "\PyUi\Chapter 5 - K Means Clustering"
$PYTHONPATH += ";" + $aaa + "\UserInterface\Plugins\Widgets"
$PYTHONPATH += ";" + $aaa + "\UserInterface\Chapter 2 - Normalize"
$PYTHONPATH += ";" + $aaa + "\UserInterface\Chapter 3 - Distance Metrics"
$PYTHONPATH += ";" + $aaa + "\UserInterface\Chapter 5 - K Means Clustering"
$PYQTDESIGNERPATH=$env.aaa + "\UserInterface\Plugins\Python"
write-Host $PYTHONPATH
"C:\Users\IlanH\AppData\Local\Continuum\anaconda3\envs\Python36\Library\bin\designer"
cd $cwd
#REM python $args[0]