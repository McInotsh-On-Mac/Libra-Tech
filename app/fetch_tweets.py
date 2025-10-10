import tweepy
import sys
import re
from twitter_setup import client
import langdetect
from langdetect import detect, LangDetectException
from .db import get_db_connection


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
                
            #TODO: Store tweets in DB 
            with open("raw_tweets.txt", "w", encoding="utf-8") as file:
                for tweet in raw_tweets:
                    file.write(tweet + "\n")

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
    # TODO(Elali): Implement logic to store tweet in the database.
    pass

def fetch_and_store_tweets(keyword, count=10, user_id=None):
    # TODO: Integrate with UI, fetch tweets, store in DB, and return list for display.
    pass

# should be removed after refactor
if __name__ == "__main__":
    # Check if a keyword is passed as a command line argument
    if len(sys.argv) > 1:
        keyword = sys.argv[1]  # Get the keyword passed from the command line
        fetch_tweets_v2(keyword)
    else:
        print("No keyword provided.")
