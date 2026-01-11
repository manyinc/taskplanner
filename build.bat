@echo off
call .venv\Scripts\activate
pyinstaller --onefile --noconsole --icon=assets\icon.ico --add-data "assets;assets" main.py --name "TaskPlanner"
pause