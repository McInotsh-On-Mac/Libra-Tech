@echo off
echo Starting Libra-Tech Sentiment Analysis App...
cd /d "%~dp0"
if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)
call venv\Scripts\activate
python run.py
if errorlevel 1 (
    echo Application exited with an error.
    pause
)