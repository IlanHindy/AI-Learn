cd %1
cd ..
cd docs
cd html
set arg="file:///%CD%\index.html"
echo %arg%
start chrome %arg%
echo finished