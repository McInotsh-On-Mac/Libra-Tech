import tweepy # Imports the main library for interacting with the Twitter (X) API.
import os # Imports tools to work with the computer's operating system (like finding files or secret keys).
from dotenv import load_dotenv # Imports a tool to automatically load secret keys from a special file named '.env'.

#load environment variables from .env file
load_dotenv()

#retrieve API keys from environment variables
# These lines retrieve the specific secret keys needed for old and new Twitter APIs.
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Needed for API v2

# Ensure variables are loaded from the .env file.
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
    # If any key is missing, the program stops and tells the user to check their secret file.
    raise ValueError("Missing API credentials. Check your .env file.")

#authenticate to twitter
# Sets up the basic authentication handler using the classic API keys.
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
# Attaches the specific access tokens for this application.
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET) 

# create API object
api = tweepy.API(auth, wait_on_rate_limit = True)

#authenticate using API v2 (for fetching tweets)
# Creates the connection object for the modern (v2) API, which is best for searching tweets.
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# test authentication
try:
    user = api.verify_credentials()
    # If successful, prints a confirmation message.
    print(f"Authentication successful! Logged in as: {user.name}")
except Exception as e:
    # If anything goes wrong, prints an error message.
    print(f"Authentication failed: {e}")