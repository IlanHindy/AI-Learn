$env:cwd = (Get-Item -Path ".\" -Verbose).FullName
cd "C:\ArtificialIntelligence\ArtificialIntelligence\Python\Projects VS code\ArtificialIntelligence_\ArtificialInteligence"
$env:aaa = (Get-Item -Path ".\" -Verbose).FullName
$env:PYTHONPATH = $env:aaa
$env:PYTHONPATH += ";" + $env:aaa + "\PyUi"
$env:PYTHONPATH += ";" + $env:aaa + "\Infrastructure"
$env:PYTHONPATH += ";" + $env:aaa + "\Utilities"
$env:PYTHONPATH += ";" + $env:aaa + "\Tests"
$env:PYTHONPATH += ";" + $env:aaa + "\AI"
$env:PYTHONPATH += ";" + $env:aaa + "\PyUi\Chapter 2 - Normalize"
$env:PYTHONPATH += ";" + $env:aaa + "\PyUi\Chapter 3 - Distance Metrics"
$env:PYTHONPATH += ";" + $env:aaa + "\PyUi\Chapter 5 - K Means Clustering"
$env:PYTHONPATH += ";" + $env:aaa + "\UserInterface\Plugins\Widgets"
$env:PYTHONPATH += ";" + $env:aaa + "\UserInterface\Chapter 2 - Normalize"
$env:PYTHONPATH += ";" + $env:aaa + "\UserInterface\Chapter 3 - Distance Metrics"
$env:PYTHONPATH += ";" + $env:aaa + "\UserInterface\Chapter 5 - K Means Clustering"
cd $env:cwd
python $args[0]