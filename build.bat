
@echo off
RD venv dist /S /Q 
virtualenv venv
pip freeze > requirements.txt
pip install -r .\requirements.txt
pip install pyinstaller

pyinstaller -w --icon=assets\asset.ico --add-data="assets\asset.ico;." -n psplashy.exe  app\app.py 

