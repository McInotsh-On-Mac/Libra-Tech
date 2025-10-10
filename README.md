# Libra-Tech

**Sentimental Analysis on X**

## **Description**
Libra-Tech is a Python application that leverages Twitter (X) data to perform sentiment analysis.
The user can search for tweets related to a movie, fetch real-time results, and analyze the overall sentiment.

## **Table of Contents**
1) [Tools](#tools)
2) [Installation](#installation)
3) [How To Use](#howitworks)
4) [How It Works](#howitworks)
5) [Credits](#credits)


## Tools
- Visual Studio Code
- X (Twitter)
- X developer tools: X's Standard Search API, OAuth 2.0

## Installation

1. **Prerequisites:**
   - Python 3.7 or higher
   - Visual Studio Code (recommended)

2. **Setup:**
   - Download or clone this repository.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure your X (Twitter) API credentials (see `.env.example`).

3. **Run the Application:**
   - Open the project folder in Visual Studio Code.
   - Run the main script or launch the executable (if provided).
   - For Windows users, you may use `Main.exe` in the `dist` folder for a packaged version.

## How to Use
1. Launch the application.
2. Login (username: `admin`, password: `password` for demo).
3. Enter a movie title or subject in the search box.
4. Click **Fetch Tweets** to get related tweets.
5. Click **Analyze Sentiment** to see the sentiment analysis results.
6. View and export the results as needed.


## How it works

- User enters keywords/hashtags.
- The backend sends a request to X’s API and fetches tweets.
- Text is processed and normalized.
- Sentiment scores are computed and categorized.
- Results are displayed in the UI, with export options.


## Credits
- Jania Southall 
- Elali McNair
- Sebastian McIntosh
- Benjamin Herron
- Ryan Grimes
- Anthony Powell


