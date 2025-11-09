# app/twitter_setup.py

import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global client variable
client = None
api = None

def initialize_twitter_client():
    """
    Initialize Twitter API client with credentials from environment.
    This is called lazily when credentials are needed.
    Returns True if successful, False otherwise.
    """
    global client, api
    
    # Retrieve API keys from environment variables
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    
    # Check if all required variables are loaded
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
        print("Warning: Twitter API credentials not found in .env file")
        return False
    
    try:
        # Authenticate to Twitter API v1.1
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        
        # Create API v1.1 object with automatic rate limit handling
        api = tweepy.API(auth, wait_on_rate_limit=False)
        
        # Authenticate using API v2 (for fetching tweets) with rate limit handling
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET,
            wait_on_rate_limit=False
        )
        
        print("Twitter API client initialized successfully")
        return True
        
    except Exception as e:
        print(f"Error initializing Twitter client: {e}")
        return False

def get_client():
    """
    Get the Twitter client, initializing it if necessary.
    Returns the client or None if initialization fails.
    """
    global client
    
    if client is None:
        # Reload environment variables in case they were just saved
        load_dotenv(override=True)
        if not initialize_twitter_client():
            return None
    
    return client

def get_api():
    """
    Get the Twitter API v1.1 object, initializing it if necessary.
    Returns the API object or None if initialization fails.
    """
    global api
    
    if api is None:
        # Reload environment variables in case they were just saved
        load_dotenv(override=True)
        if not initialize_twitter_client():
            return None
    
    return api

def check_rate_limit_status():
    """Check current rate limit status"""
    current_api = get_api()
    if current_api is None:
        return None
        
    try:
        rate_limit_status = current_api.get_rate_limit_status()
        search_limit = rate_limit_status['resources']['search']['/search/tweets']
        return {
            'remaining': search_limit['remaining'],
            'reset_time': search_limit['reset'],
            'limit': search_limit['limit']
        }
    except Exception as e:
        print(f"Error checking rate limit: {e}")
        return None

def test_authentication():
    """Test both API v1.1 and v2 authentication"""
    current_client = get_client()
    current_api = get_api()
    
    if current_client is None or current_api is None:
        print("Authentication failed: Client not initialized")
        return False
        
    try:
        # Test API v1.1
        user = current_api.verify_credentials()
        print(f"API v1.1 Authentication successful! Logged in as: {user.name}")
        
        # Test API v2
        me = current_client.get_me()
        print(f"API v2 Authentication successful! User ID: {me.data.id}")
        
        return True
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

# Don't initialize on import - wait until credentials are available
if __name__ == "__main__":
    test_authentication()