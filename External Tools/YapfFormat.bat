cd C:\Users\IlanH\Anaconda3\Scripts
call activate python36
cd "C:\ArtificialIntelligence\ArtificialIntelligence\Python\Projects\Visual Studio External Tools"
Python SavedNeededWarning.py
cd %1
d:
echo %CD%
REM yapf  --recursive --style="google" --in-place %CD%
REM yapf  --recursive --style="{based_on_style: chromium, indent_width: 4, column_limit: 120}" --in-place %CD%
yapf  --recursive  --in-place %CD%
echo finished