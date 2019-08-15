SET mypath=%~dp0
echo %mypath:~0,-1%
cd %1

python %mypath:~0,-1%\hash_names.py %2