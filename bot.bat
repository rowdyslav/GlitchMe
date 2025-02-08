@echo off
call venv\Scripts\activate.bat
start cmd /k "cd bot && python main.py"
start cmd /k "cd bot && python webhook.py"