@echo off
echo Installing Libra-Tech Sentiment Analysis App...
echo ==================================================

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.7 or higher first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('vader_lexicon', quiet=True); nltk.download('stopwords', quiet=True); print('NLTK data downloaded successfully')"

if not exist .env (
    echo Creating environment configuration file...
    copy nul .env
    echo # Twitter/X API Configuration > .env
    echo TWITTER_BEARER_TOKEN=your_bearer_token_here >> .env
    echo TWITTER_API_KEY=your_api_key_here >> .env
    echo # Database Configuration >> .env
    echo DB_HOST=localhost >> .env
    echo DB_NAME=libra_tech >> .env
    echo Please edit .env file with your API credentials
)

python setup.py

echo.
echo Installation completed successfully!
echo.
echo Next steps:
echo 1. Edit the .env file with your Twitter/X API credentials
echo 2. Set up your PostgreSQL database
echo 3. Double-click LibraTech.bat to launch the app
echo.
pause