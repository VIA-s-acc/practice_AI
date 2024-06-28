@echo off



REM run script
python install.py

if %ERRORLEVEL%==0 (

    REM Activate the virtual environment
    call ".venv\Scripts\activate.bat"

    REM run flet app
    py -3.10 run.py
    
) else if %ERRORLEVEL%==1 (
    echo EXIT CODE 1 - VENV ERROR || Failed to create virtual environment
) else if %ERRORLEVEL%==2 (
    echo EXIT CODE 2 - VERSION ERROR || Need python 3.10
) else if %ERRORLEVEL%==3 (
    echo EXIT CODE 3 - PIP ERROR || Error in packages installing 
)

pause