#!/bin/bash
# filepath: /Users/jania/Libra-Tech/install.sh

echo "Installing Libra-Tech Sentiment Analysis App..."
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data 
echo "Downloading NLTK data..."
python3 -c "
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)
    print(' NLTK data downloaded successfully')
except Exception as e:
    print(f' Warning: Could not download NLTK data: {e}')
"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo " Creating environment configuration file..."
    cat > .env << EOF
# Twitter/X API Configuration
BEARER_TOKEN=api_bearer_token_here
API_KEY=api_key_here
API_SECRET=api_secret_here
ACCESS_TOKEN=api_access_token_here
TOKEN_SECRET=api_access_token_secret_here

# Database Configuration
DB_NAME=postgres
DB_USER=postgres.rrhyfcqtvbbkgzbeztcg
DB_PASSWORD=LibraTech
DB_HOST=aws-1-us-east-1.pooler.supabase.com
DB_PORT=5432
EOF
    echo "Please edit .env file with your API credentials"
else
    echo "Environment file already exists"
fi

# Make launcher executable
chmod +x launcher.sh

# Create desktop shortcut for macOS
echo " Creating desktop shortcut..."
cat > ~/Desktop/LibraTech.command << EOF
#!/bin/bash
cd "$(dirname "\$0")"
cd "$PWD"
./launcher.sh
EOF
chmod +x ~/Desktop/LibraTech.command

echo ""
echo " Installation completed successfully!"
echo ""
echo " Next steps:"
echo "1. Double-click 'LibraTech.command' on your desktop to launch the app"
echo "   OR run: ./launcher.sh from this directory"
echo ""
echo " For more information, see README.md"