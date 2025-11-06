@echo off
echo Starting Libra-Tech Sentiment Analysis App...

cd /d "%~dp0"

if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Checking dependencies...
python -c "
import sys
required_packages = ['tkinter', 'psycopg2', 'bcrypt', 'nltk']
missing_packages = []

for package in required_packages:
    try:
        if package == 'tkinter':
            import tkinter
        elif package == 'psycopg2':
            import psycopg2
        elif package == 'bcrypt':
            import bcrypt
        elif package == 'nltk':
            import nltk
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f'Missing packages: {missing_packages}')
    print('Please run install.bat to install dependencies.')
    sys.exit(1)
else:
    print('All dependencies are installed')
"

if errorlevel 1 (
    pause
    exit /b 1
)

echo Launching application...
python run.py

if errorlevel 1 (
    echo Application exited with an error.
    pause
)