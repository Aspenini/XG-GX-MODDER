@echo off
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies. Check your Python installation or requirements.txt.
    pause
    exit /b %ERRORLEVEL%
)
echo Starting Opera GX Mod Maker...
python src/main.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to launch the app. Ensure src/main.py exists and Python is installed.
    pause
    exit /b %ERRORLEVEL%
)
pause