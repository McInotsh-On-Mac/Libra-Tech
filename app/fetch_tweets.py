# app/fetch_tweets.py

import os
import tweepy
import sys
import re
import time
from app.utils.env_loader import load_env

# Load environment variables from .env
load_env()

# Import the Twitter client from twitter_setup
from app.twitter_setup import client

# Supabase
from supabase import create_client
from langdetect import detect, LangDetectException

# Initialize Supabase client (fail fast if missing)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
if not supabase_url or not supabase_key:
    print("Missing SUPABASE_URL or SUPABASE_KEY in .env")
supabase = create_client(supabase_url, supabase_key)

print("fetch_tweets.py started")


def remove_emojis(tweet_text):
    """Remove non-ASCII characters (emojis) from tweet text."""
    return re.sub(r'[^\x00-\x7F]+', '', tweet_text or "")


def is_english(tweet_text):
    """Detect if the tweet text is English."""
    try:
        return detect(tweet_text) == 'en'
    except LangDetectException:
        return False


def safe_store_tweet_in_db(text, tweet_id=None, user_id=None, timestamp=None):
    """Safely store a tweet in the database, ignoring failures."""
    try:
        data = {"content": text}
        if tweet_id is not None:
            data["tweet_id"] = str(tweet_id)
            data["tweets__id"] = str(tweet_id)
        if user_id is not None:
            data["user_id"] = str(user_id)
        if timestamp is not None:
            data["timestamp"] = str(timestamp)

        print(f"[DB] inserting tweet_id={tweet_id} ...")
        res = supabase.table("tweets").insert(data).execute()

        print("[DB] insert response:", res)
        if getattr(res, "error", None):
            print("[DB] error attr:", res.error)
            return False
        if isinstance(res, dict) and res.get("error"):
            print("[DB] dict error:", res["error"])
            return False

        return True
    except Exception as e:
        print("[DB] Exception while inserting:", e)
        return False


def fetch_tweets_for_ui(keyword, count=10, max_api_pages=1, api_wait_seconds=1):
    """
    Fetch recent tweets for a keyword, filtered for English and uniqueness.
    Returns a dict: {'success', 'tweets', 'message', 'count'}.
    """
    print(f"[FETCH] start for keyword='{keyword}' count={count}")
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

    try:
        while len(collected) < count and pages < max_api_pages:
            pages += 1
            print(f"[FETCH] API request page {pages} next_token={next_token}")
            try:
                resp = client.search_recent_tweets(
                    query=keyword,
                    max_results=min(100, max(10, count)),
                    tweet_fields=["id", "text", "created_at", "author_id"],
                    next_token=next_token
                )
            except Exception as api_e:
                print("[FETCH] API call exception:", api_e)
                result['message'] = f"API error: {api_e}"
                return result

            if not resp or not getattr(resp, "data", None):
                print("[FETCH] no data in response")
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

                # Attempt DB store
                try:
                    stored = safe_store_tweet_in_db(
                        one_line,
                        tweet_id=getattr(t, "id", None),
                        user_id=getattr(t, "author_id", None),
                        timestamp=getattr(t, "created_at", None)
                    )
                    if not stored:
                        print("[FETCH] DB store returned False (continuing)")
                except Exception as db_e:
                    print("[FETCH] DB exception (ignored):", db_e)

                collected.append(one_line)
                print(f"[FETCH] collected {len(collected)}/{count}")
                if len(collected) >= count:
                    break

            # handle pagination token
            meta = getattr(resp, "meta", None)
            next_token = meta.get("next_token") if isinstance(meta, dict) else None

            if next_token:
                print(f"[FETCH] next_token present, waiting {api_wait_seconds}s before next page")
                time.sleep(api_wait_seconds)
            else:
                break

        if collected:
            result.update({
                'success': True,
                'tweets': collected,
                'count': len(collected),
                'message': f"Fetched {len(collected)} tweets for '{keyword}'"
            })
        else:
            result['message'] = f"No suitable tweets found for '{keyword}'."

    except Exception as e:
        print("[FETCH] unexpected exception:", e)
        result['message'] = f"Unexpected error: {e}"

    print("[FETCH] finished:", result.get('message'))
    return result


if __name__ == "__main__":
    # Quick debug run
    print(fetch_tweets_for_ui("test", count=5, max_api_pages=1))
