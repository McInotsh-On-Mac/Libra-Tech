import os
import tweepy
import sys
import re
import time
from dotenv import load_dotenv

# load local .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from .twitter_setup import client
from langdetect import detect, LangDetectException

print("fetch_tweets.py started")

def remove_emojis(tweet_text):
    return re.sub(r'[^\x00-\x7F]+', '', tweet_text or "")

def is_english(tweet_text):
    try:
        return detect(tweet_text) == 'en'
    except LangDetectException:
        return False
    
# (Benjamin): Fetch function for UI integration
def fetch_tweets_for_ui(keyword, count=10, max_api_pages=1, api_wait_seconds=1):
    """
    Fetch tweets function with debug prints. Returns dict {'success','tweets','message','count'}.

    max_api_pages controls how many batches of tweets to request from Twitter; 
    default 1 prevents fetching too many tweets and hitting rate limits.
    """
    print(f"FETCH start for keyword='{keyword}' count={count}")
    result = {'success': False, 'tweets': [], 'message': '', 'count': 0}
    if not keyword or not keyword.strip():
        result['message'] = "No keyword provided."
        return result

    try:
        count = max(1, min(int(count), 100))
    except Exception:
        count = 10

    collected = []
    seen = set()
    next_token = None
    pages = 0
    sequential_counter = 1

    try:
        while len(collected) < count and pages < max_api_pages:
            pages += 1
            print(f"API request page {pages} next_token={next_token}")
            try:
                # create request
                resp = client.search_recent_tweets(
                    query=keyword,
                    max_results=min(100, max(10, count)),
                    tweet_fields=["id", "text", "created_at", "author_id"],
                    next_token=next_token
                )
            except Exception as api_e:
                print("API call exception:", api_e)
                result['message'] = f"API error: {api_e}"
                return result

            print("API call returned, checking data...")
            if not resp or not getattr(resp, "data", None):
                print("no data in response")
                break

            for t in resp.data:
                text = getattr(t, "text", "") or ""
                text = remove_emojis(text).strip()
                if not text:
                    continue
                if not is_english(text):
                    continue
                one_line = text.replace("\n", " ")
                if one_line in seen:
                    continue
                seen.add(one_line)

                collected.append(one_line)
                # Increment counter for next tweet
                sequential_counter += 1
                print(f"[FETCH] collected {len(collected)}/{count}")
                if len(collected) >= count:
                    break

            # handle pagination token if present
            meta = getattr(resp, "meta", None)
            next_token = None
            if meta and isinstance(meta, dict):
                next_token = meta.get("next_token")

            if next_token:
                print(f"next_token present, waiting {api_wait_seconds}s before next page")
                time.sleep(api_wait_seconds)
            else:
                print("no next_token, finishing")
                break

        if collected:
            result.update({'success': True, 'tweets': collected, 'count': len(collected),
                           'message': f"Fetched {len(collected)} tweets for '{keyword}'"})
        else:
            result['message'] = f"No suitable tweets found for '{keyword}'."
    except Exception as e:
        print("[FETCH] unexpected exception:", e)
        result['message'] = f"Unexpected error: {e}"

    print("FETCH finished:", result.get('message'))
    return result