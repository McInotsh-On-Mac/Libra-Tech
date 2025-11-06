import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Ensure all required variables are loaded
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
    raise ValueError("Missing API credentials. Check your .env file.")

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

def check_rate_limit_status():
    """Check current rate limit status"""
    try:
        rate_limit_status = api.get_rate_limit_status()
        search_limit = rate_limit_status['resources']['search']['/search/tweets']
        return {
            'remaining': search_limit['remaining'],
            'reset_time': search_limit['reset'],
            'limit': search_limit['limit']
        }
    except Exception as e:
        return None

# Test authentication
def test_authentication():
    """Test both API v1.1 and v2 authentication"""
    try:
        # Test API v1.1
        user = api.verify_credentials()
        print(f"API v1.1 Authentication successful! Logged in as: {user.name}")
        
        # Test API v2
        me = client.get_me()
        print(f"API v2 Authentication successful! User ID: {me.data.id}")
        
        return True
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

# Run authentication test when module is imported
if __name__ == "__main__":
    test_authentication()
else:
    pass