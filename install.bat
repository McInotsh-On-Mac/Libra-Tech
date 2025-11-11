@echo off
echo Installing Libra-Tech Sentiment Analysis App...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
   echo Python is not installed. Please install Python 3.7 or higher first.
   echo Visit: https://www.python.org/downloads/
   pause
   exit /b 1
)

REM Display Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo Python %%i detected

REM Create virtual environment if it doesn't exist
if not exist venv (
   echo Creating virtual environment...
   python -m venv venv
) else (
   echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Download NLTK data (required for sentiment analysis)
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('vader_lexicon', quiet=True); nltk.download('stopwords', quiet=True); print('✅ NLTK data downloaded successfully')"

REM Check if NLTK download was successful
if errorlevel 1 (
   echo ⚠ Warning: Could not download NLTK data. You may need to download it manually.
)

REM Create .env file if it doesn't exist
if not exist .env (
   echo Creating environment configuration file...
   (
       echo # Twitter/X API Configuration
       echo TWITTER_BEARER_TOKEN=your_bearer_token_here
       echo TWITTER_API_KEY=your_api_key_here
       echo TWITTER_API_SECRET=your_api_secret_here
       echo TWITTER_ACCESS_TOKEN=your_access_token_here
       echo TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
       echo.
       echo # Database Configuration
       echo DB_HOST=localhost
       echo DB_NAME=libra_tech
       echo DB_USER=your_db_user_here
       echo DB_PASSWORD=your_db_password_here
       echo DB_PORT=5432
   ) > .env
   echo ✅ Environment configuration file created
   echo Please edit .env file with your API credentials
) else (
   echo Environment file already exists
)

REM Run setup script to create launchers
echo Creating application launchers...
python setup.py

REM Create desktop shortcut - Method 1: Enhanced PowerShell
echo Creating desktop shortcut...
echo Current directory: %CD%
echo Desktop path: %USERPROFILE%\Desktop

powershell -ExecutionPolicy Bypass -Command "try { $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'LibraTech.lnk')); $Shortcut.TargetPath = '%CD%\LibraTech.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'LibraTech Sentiment Analysis App'; $Shortcut.Save(); Write-Host 'Desktop shortcut created successfully at:'; Write-Host ([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'LibraTech.lnk')) } catch { Write-Host 'Error creating desktop shortcut:' $_.Exception.Message; exit 1 }"

if errorlevel 1 (
    echo PowerShell method failed, trying VBScript method...
    
    REM Create desktop shortcut - Method 2: VBScript fallback
    echo Set WshShell = CreateObject("WScript.Shell") > temp_shortcut.vbs
    echo Set Shortcut = WshShell.CreateShortcut("%USERPROFILE%\Desktop\LibraTech.lnk") >> temp_shortcut.vbs
    echo Shortcut.TargetPath = "%CD%\LibraTech.bat" >> temp_shortcut.vbs
    echo Shortcut.WorkingDirectory = "%CD%" >> temp_shortcut.vbs
    echo Shortcut.Description = "LibraTech Sentiment Analysis App" >> temp_shortcut.vbs
    echo Shortcut.Save >> temp_shortcut.vbs
    
    cscript //nologo temp_shortcut.vbs
    del temp_shortcut.vbs
    
    if exist "%USERPROFILE%\Desktop\LibraTech.lnk" (
        echo ✅ Desktop shortcut created successfully using VBScript
    ) else (
        echo ⚠ Could not create desktop shortcut. You can manually create one by:
        echo    1. Right-click on desktop
        echo    2. Choose New ^> Shortcut
        echo    3. Browse to: %CD%\LibraTech.bat
        echo    4. Set working directory to: %CD%
    )
) else (
    echo ✅ Desktop shortcut created successfully using PowerShell
)

REM Create Start Menu shortcut (optional)
echo Creating Start Menu shortcut...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\LibraTech" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\LibraTech"

echo Set WshShell = CreateObject("WScript.Shell") > temp_startmenu.vbs
echo Set Shortcut = WshShell.CreateShortcut("%APPDATA%\Microsoft\Windows\Start Menu\Programs\LibraTech\LibraTech Sentiment Analysis.lnk") >> temp_startmenu.vbs
echo Shortcut.TargetPath = "%CD%\LibraTech.bat" >> temp_startmenu.vbs
echo Shortcut.WorkingDirectory = "%CD%" >> temp_startmenu.vbs
echo Shortcut.Description = "LibraTech Sentiment Analysis App" >> temp_startmenu.vbs
echo Shortcut.Save >> temp_startmenu.vbs

cscript //nologo temp_startmenu.vbs
del temp_startmenu.vbs

if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\LibraTech\LibraTech Sentiment Analysis.lnk" (
    echo ✅ Start Menu shortcut created successfully
) else (
    echo ⚠ Could not create Start Menu shortcut
)

echo.
echo ==========================================
echo ✅ Installation completed successfully!
echo ==========================================
echo.
echo 📋 Next steps:
echo 1. Edit the .env file with your Twitter/X API credentials
echo 2. Set up your PostgreSQL database
echo 3. Launch the app by:
echo    • Double-clicking the LibraTech shortcut on your desktop
echo    • Double-clicking LibraTech.bat in this folder
echo    • Searching for "LibraTech" in your Start Menu
echo.
echo 📖 For more information, see README.md
echo.
pause


