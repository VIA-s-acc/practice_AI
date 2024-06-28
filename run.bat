@echo off

REM Set the path to your virtual environment
set "VENV_DIR=C:\practice\.venv"

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate"

REM Run the flet command
flet run gui
