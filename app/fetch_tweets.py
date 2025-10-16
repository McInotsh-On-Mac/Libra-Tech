import tweepy
import sys
import re
from .twitter_setup import client
import langdetect
import os
from supabase import create_client
from langdetect import detect, LangDetectException
from .db import get_db_connection

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

print("fetch_tweets.py has started running...")
#TODO: Refactor to be modular for UI integration

def remove_emojis(tweet_text):
    #remove emohies using regex pattern (unicode ranges for emojies)
    return re.sub(r'[^\x00-\x7F]+', '', tweet_text)


def is_english(tweet_text):
    try:
        #detect language
        return detect(tweet_text) == 'en'
    except LangDetectException:
        return False #if detection fails, consider it not english
    
def fetch_tweets_v2(keyword, count=10):
    # TODO: refactor this into fetch_and_store_tweets()
    """ Fetch tweets based on a keyword and display them """
    try:
        count = max(1, min(count, 10))
        # Fetch tweets with the provided keyword
        response = client.search_recent_tweets(query=keyword, max_results=10)
        
        raw_tweets = []
        seen_tweets = set()
        shown = 0

        if response and response.data:
            print(f"\nFetched tweets for keyword: '{keyword}'\n")

            for tweet in response.data:
                if shown >= count:
                    break

                text = tweet.text.strip()
                text = remove_emojis(text)

                if not text or not is_english(text) or text in seen_tweets:
                    continue #skip if the tweet is not in english or duplicate
                
                text_one_line = text.replace("\n", " ")
                raw_tweets.append(text_one_line)
                seen_tweets.add(text_one_line)
                shown += 1

            if not raw_tweets:
                print("No suitable English tweets found.")
                return
                
            store_tweet_in_db(text_one_line)  # Store tweet in DB

            # Print aligned and numbered output
            print("Tweets Fetched:\n")
            max_digits = len(str(len(raw_tweets)))
            for i, tweet in enumerate(raw_tweets, 1):
                num_str = f"{i}".rjust(max_digits)
                print(f"{num_str}. {tweet}")
            print("\nAll tweets saved to 'raw_tweets.txt'.\n")

        else:
            print("No tweets found.")
    except Exception as e:
        print(f"Error fetching tweets: {e}")


def store_tweet_in_db(text, user_id=None):
    # Person 2: Store tweet using Supabase
    data = {"text": text}
    if user_id:
        data["user_id"] = user_id
    supabase.table("tweets").insert(data).execute()

def fetch_tweets_for_ui(keyword, count=10):
    """
    Fetch tweets for UI display - returns a dictionary with results and status
    """
    result = {
        'success': False,
        'tweets': [],
        'message': '',
        'count': 0
    }
    
    try:
        count = max(1, min(count, 10))
        # Fetch tweets with the provided keyword
        response = client.search_recent_tweets(query=keyword, max_results=10)
        
        raw_tweets = []
        seen_tweets = set()
        shown = 0

        if response and response.data:
            for tweet in response.data:
                if shown >= count:
                    break

                text = tweet.text.strip()
                text = remove_emojis(text)

                if not text or not is_english(text) or text in seen_tweets:
                    continue #skip if the tweet is not in english or duplicate
                
                text_one_line = text.replace("\n", " ")
                raw_tweets.append(text_one_line)
                seen_tweets.add(text_one_line)
                shown += 1
                
                # Store each tweet in DB
                try:
                    store_tweet_in_db(text_one_line)
                except Exception as db_error:
                    print(f"Database storage error: {db_error}")

            if raw_tweets:
                result['success'] = True
                result['tweets'] = raw_tweets
                result['count'] = len(raw_tweets)
                result['message'] = f"Successfully fetched {len(raw_tweets)} tweets for '{keyword}'"
            else:
                result['message'] = f"No suitable English tweets found for keyword '{keyword}'"
        else:
            result['message'] = f"No tweets found for keyword '{keyword}'"
            
    except Exception as e:
        result['message'] = f"Error fetching tweets: {str(e)}"
        
    return result

# should be removed after refactor
if __name__ == "__main__":
    # Check if a keyword is passed as a command line argument
    if len(sys.argv) > 1:
        keyword = sys.argv[1]  # Get the keyword passed from the command line
        fetch_tweets_for_ui(keyword)
    else:
        print("No keyword provided.")
