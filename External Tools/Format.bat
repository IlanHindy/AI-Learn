cd D:\Anaconda\Scripts
call activate python35
cd %1
autopep8 -a -i -r "%CD%"
echo finished