@echo off
pyinstaller --onefile --noconsole --icon=assets\icon.ico --add-data "assets;assets" main.py --name "TaskPlanner"
pause