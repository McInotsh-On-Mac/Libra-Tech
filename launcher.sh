#!/bin/bash
# Jania Southall: Created the launcher script for Libra-Tech Sentiment Analysis App

echo "Starting Libra-Tech Sentiment Analysis App..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo " Virtual environment not found. Please run install.sh first."
    read -p "Press any key to exit..."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if required packages are installed
python3 -c "
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
    print('Please run install.sh to install dependencies.')
    sys.exit(1)
else:
    print('✅ All dependencies are installed')
"

if [ $? -ne 0 ]; then
    read -p "Press any key to exit..."
    exit 1
fi

# Run the application
echo "Launching application..."
python3 run.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo " Application exited with an error."
    read -p "Press any key to exit..."
fi