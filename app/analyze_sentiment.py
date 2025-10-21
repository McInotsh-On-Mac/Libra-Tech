import psycopg2
import re
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from spellchecker import SpellChecker
import os
from datetime import datetime 
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Initialize Supabase client (same format as fetch_tweets.py)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
if not supabase_url or not supabase_key:
    print("Missing SUPABASE_URL or SUPABASE_KEY in .env")
supabase = create_client(supabase_url, supabase_key)

# Initialize tools and vocab
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
english_vocab = set(w.lower() for w in words.words())
spell = SpellChecker()

# Slang whitelist and shorthand map
slang_whitelist = {"u", "dm", "rn", "pls", "idk", "lol", "brb", "gtg", "lmao", "omg", "tbh", "afaik", "imho"}
shorthand_map = {
    "u": "you",
    "dm": "direct message",
    "rn": "right now",
    "pls": "please",
    "idk": "i don't know",
    "lol": "laugh out loud",
    "gtg": "got to go",
    "brb": "be right back",
    "lmao": "laughing my ass off",
    "omg": "oh my god",
    "tbh": "to be honest",
    "afaik": "as far as i know",
    "imho": "in my humble opinion"
}

#sentiment dictionary
sentiment_dict = {
    # Strong Positive Words
   "masterpiece": 5, "blockbuster": 5, "must-watch": 5, "award-worthy": 5, "oscar-worthy": 5, 
   "breathtaking": 5, "phenomenal": 5, "spectacular": 5, "stunning": 5, "incredible": 5, "legendary": 5, 
   "groundbreaking": 5, "emotionally-powerful": 5, "iconic": 5, "revolutionary": 5, "perfection": 5, 
   "unforgettable": 5, "flawless": 5, "timeless": 5, "brilliantly-crafted": 5, "peak-cinema": 5, "love": 5,
    "epic": 4, "amazing": 4, "awesome": 4, "brilliant": 4, "fantastic": 4,
    "excellent": 4, "outstanding": 4, "thrilling": 4, "wonderful": 4, "mind-blowing": 4,
    "gripping": 4, "electrifying": 4, "remarkable": 4, "heartwarming": 4, "thought-provoking": 4,
    "well-acted": 4, "visually-striking": 4, "inspiring": 4, "emotional": 4, "hilarious": 4,
    "motivating": 4, "joyful": 4, "rewarding": 4, "uplifting": 4, "refreshing": 4,
    "enjoyable": 4, "powerful": 4, "mind-expanding": 4, "captivating": 4, "masterfully-directed": 4,
    "visually-stunning": 4, "tight-script": 4, "brilliant-performance": 4, "moving": 4, "elegant": 4,
    "well-paced": 4, "immersive": 4, "emotional-journey": 4, "genius": 4,
    "beautiful": 4, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4, "enthusiastic": 4,
    "great": 3, "impressive": 3, "superb": 3, "entertaining": 3, "exciting": 3,
    "intense": 3, "high-octane": 3, "cinematic": 3, "riveting": 3, "charming": 3,
    "engaging": 3, "cult-classic": 3, "fun": 3, "cool": 3, "strong": 3,
    "well-done": 3, "solid": 3, "visually-pleasing": 3, "watchable": 3, "stylish": 3,
    "well-written": 3, "clever": 3, "artistic": 3, "emotion-filled": 3, "smart": 3,
    "balanced": 3, "great-dialogue": 3, "unique": 3, "worthy": 3, "likeable": 3,
    "fun-ride": 3, "touching": 3, "laugh-out-loud": 3, "witty": 3, "feel-good": 3,

    # Neutral Words
    "okay": 0, "neutral": 0, "average": 0, "decent": 1, "plain": 1,
    "standard": 1, "typical": 0, "moderate": 1, "simple": 1, "fine": 1,
    "passable": 1, "straightforward": 1, "uncomplicated": 1, "serviceable": 1, "middle-of-the-road": 0,
    "meh": 0, "acceptable": 1, "normal": 1, "basic": 1, "regular": 1,
    "expected": 1, "predictable": -1, "forgettable": -1, "formulaic": -1, "plain-jane": 0, "scary": -1, "surprised": 1,

    # Negative Words
    "mediocre": -1, "predictable": -1, "forgettable": -1, "formulaic": -1, "slow": -2,
    "uninspired": -2, "cliché": -2, "unrealistic": -2, "dry": -2, "flat": -2,
    "underdeveloped": -2, "meh": -2, "confusing": -2, "lackluster": -2, "awkward": -2,
    "weak": -2, "repetitive": -2, "safe": -2, "thin": -2, "shaky": -2,
    "clunky": -2, "overused": -2, "dull": -3, "unoriginal": -3, "underwhelming": -3,
    "overrated": -3, "cheesy": -3, "forced": -3, "messy": -3, "lifeless": -3,
    "dragging": -3, "plot holes": -3, "wooden acting": -3, "bad CGI": -3, "annoying": -3,
    "frustrating": -3, "meaningless": -3, "empty": -3, "poorly-executed": -3, "disjointed": -3,
    "nonsensical": -3, "ridiculous": -3, "over-the-top": -3, "flat-characters": -3, "exaggerated": -3,
    "boring": -4, "disappointing": -4, "flop": -4, "cringe": -4, "waste": -4,
    "waste-of-time": -4, "cringeworthy": -4, "shocking": -4, "disturbing": -4, "forced-dialogue": -4,
    "painful": -5, "horrible": -5, "terrible": -5, "trash": -5, "worst": -5,
    "atrocious": -5, "devastating": -5, "horrific": -5, "disgusting": -5, "hate": -5,
    "angry": -5, "unwatchable": -5, "nauseating": -5, "garbage": -5, "insulting": -5, "anxious": -2, 
    "terrifying": -3, "surprised": 1, "tense": -1, "tearjerker": 4, "beautiful": 4, "nostalgic": 1,

    # Strong Emotions (Positive & Negative)
    "love": 5, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4, "enthusiastic": 4,
    "hate": -5, "angry": -5, "frustrated": -4, "disgusting": -5, "horrific": -5,
    "devastating": -5, "shocking": -4, "unbelievable": -3, "scary": -3, "disturbing": -4,

    # Common Words From Twitter
    "fire": 4, "goat": 5, "slaps": 4, "based": 4, "mid": -2,
    "wack": -3, "overhyped": -3, "underrated": 3, "slept-on": 3, "dead": -3,
    "chef's-kiss": 5, "vibes": 3, "badass": 4, "yawn": -3, "lit": 4,
    "banger": 4, "peak": 4, "goofy": -2, "corny": -3, "sus": -2,
    "hard": 4, "rage": 3, "on-point": 4, "buzz": 2, "flop": -4,
    "sci-fi": 2, "rom-com": 2, "horror": 1, "thriller": 2, "documentary": 1,
    "animation": 2, "drama": 1, "action-packed": 4, "mystery": 2, "psychological": 2,
    "dark": -1, "light-hearted": 3, "gory": -2, "family-friendly": 3, "noir": -1,
    "campy": -2, "twist": 2, "genuine": 3, "cheesy-dialogue": -3, "flashy": 2,
    "breaking": 2, "reaction": 2, "drama": -2, "scandal": -3, "attack": -3,
    "urgent": -2, "exposed": -3, "crisis": -3, "controversial": -3, "rumor": -2,
    "debate": -1, "insane": 3, "leak": 1, "announcement": 2, "performance": 2,
    "directorial-debut": 2, "ensemble-cast": 2, "character-driven": 3, "story-driven": 3, "over-indulgent": -2,
    "melodramatic": -2, "heavy-handed": -2, "understated": 2, "visionary": 4, "self-aware": 3,
    "raw": 3, "elevated": 3, "cinematography": 3, "editing": 2, "score": 2
}

# Function to clean the tweet
def clean_tweet(tweet):
    tweet = tweet.lower()

    # Step 1: Replace shorthand terms first
    for word, replacement in shorthand_map.items():
        tweet = re.sub(rf'\b{re.escape(word)}\b', replacement, tweet)

    # Step 2: Remove URLs, RTs, mentions, hashtags, digits, punctuation
    tweet = re.sub(r'rt\s+', '', tweet)
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet)
    tweet = re.sub(r'#\w+', '', tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = re.sub(r'\s+', ' ', tweet).strip()

    # Step 3: Tokenize
    tokens = word_tokenize(tweet)

    # Step 4: Remove custom blacklisted words
    blacklist = {'aku', 'gama'}
    tokens = [word for word in tokens if word not in blacklist]

    # Step 5: POS tagging and lemmatization
    pos_tags = pos_tag(tokens)
    cleaned_tokens = []
    for word, tag in pos_tags:
        if word in slang_whitelist:
            cleaned_tokens.append(word)
            continue

        wordnet_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word, wordnet_pos)

        if (
            lemma not in stop_words and
            (len(lemma) > 1 or lemma in shorthand_map) and
            (lemma in english_vocab or spell.correction(lemma) == lemma)
        ):
            cleaned_tokens.append(lemma)

    return cleaned_tokens

# Function to get wordnet POS tags
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# Format cleaned tokens for writing
def format_cleaned_text(tokens):
    return ' '.join(tokens)

def analyze_sentiment(tokens):
    score = 0
    matched_words = []
    
    for token in tokens:
        if token in sentiment_dict:
            word_score = sentiment_dict[token]
            score += word_score
            matched_words.append(f"{token}({word_score})")
    
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, score, matched_words

def fetch_tweets_from_db():
    """
    Fetches all tweets from the database using Supabase.
    Returns a list of tuples: (tweet_id, tweet_content)
    """
    try:
        print("[DB] Fetching tweets from Supabase...")
        
        # Based on your database structure, use the correct column names
        response = supabase.table("tweets").select("tweet_id, content, text").execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"[DB] Error fetching tweets: {response.error}")
            return []
        
        if isinstance(response, dict) and response.get("error"):
            print(f"[DB] Dict error fetching tweets: {response['error']}")
            return []
        
        if hasattr(response, 'data') and response.data:
            print(f"[DB] Raw response data: {response.data}")
            tweets = []
            
            for tweet in response.data:
                tweet_id = tweet.get('tweet_id')
                # Try content first, then text as fallback
                content = tweet.get('content') or tweet.get('text', '')
                
                if content and content.strip():  # Only include tweets with actual content
                    tweets.append((tweet_id, content.strip()))
                    print(f"[DB] Added tweet {tweet_id}: {content[:50]}...")
                else:
                    print(f"[DB] Skipping tweet {tweet_id}: no content")
            
            print(f"[DB] Successfully fetched {len(tweets)} tweets with content")
            return tweets
        else:
            print("[DB] No data in response")
            return []
        
    except Exception as e:
        print(f"[DB] Exception fetching tweets: {e}")
        return []
    
def store_sentiment_in_db(tweet_id, label, score):
    """
    Stores sentiment analysis results in the database using Supabase.
    
    Args:
        tweet_id (int): The ID of the tweet (should match tweets.tweet_id)
        label (str): Sentiment label ('Positive', 'Negative', 'Neutral')
        score (int): Sentiment score
    """
    try:
        data = {
            "tweet_id": int(tweet_id),  # Convert to int to match your database schema
            "label": label,
            "score": score
        }
        
        print(f"[DB] Storing sentiment for tweet {tweet_id}: {label} ({score})")
        
        # Use upsert to handle duplicates (in case we analyze the same tweet twice)
        response = supabase.table("sentiments").upsert(data, on_conflict="tweet_id").execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"[DB] Error storing sentiment: {response.error}")
            return False
        
        if isinstance(response, dict) and response.get("error"):
            print(f"[DB] Dict error storing sentiment: {response['error']}")
            return False
        
        print(f"[DB] Successfully stored sentiment for tweet {tweet_id}")
        return True
        
    except Exception as e:
        print(f"[DB] Exception storing sentiment: {e}")
        return False

def analyze_tweets_for_ui():
    """
    Function that fetches tweets from DB, analyzes sentiment, 
    stores results in DB, and returns formatted results for UI display.
    """
    try:
        # Fetch tweets from database
        tweets = fetch_tweets_from_db()
        
        if not tweets:
            return {
                'success': False,
                'message': 'No tweets found in database. Please fetch some tweets first.',
                'total_tweets': 0,
                'processed_tweets': 0,
                'results': [],
                'formatted_results': [],
                'summary': 'No tweets available for analysis.',
                'sentiment_counts': {'Positive': 0, 'Negative': 0, 'Neutral': 0, 'Error': 0}
            }
        
        results = []
        processed_count = 0
        sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0, 'Error': 0}
        formatted_results = []
        
        for tweet_id, tweet_content in tweets:
            try:
                # Clean and analyze the tweet
                cleaned_tokens = clean_tweet(tweet_content)
                cleaned_text = format_cleaned_text(cleaned_tokens)
                sentiment_label, sentiment_score, matched_words = analyze_sentiment(cleaned_tokens)
                
                # Store sentiment in database
                store_success = store_sentiment_in_db(tweet_id, sentiment_label, sentiment_score)
                
                # Prepare result for internal processing
                result_dict = {
                    'tweet_id': tweet_id,
                    'raw_text': tweet_content,
                    'cleaned_text': cleaned_text,
                    'sentiment_label': sentiment_label,
                    'sentiment_score': sentiment_score,
                    'matched_words': matched_words,
                    'stored_in_db': store_success
                }
                
                results.append(result_dict)
                processed_count += 1
                
                # Format for UI display
                matched_words_str = ', '.join(matched_words) if matched_words else 'No sentiment words found'
                
                formatted_line = (
                    f"Tweet ID: {tweet_id}\n"
                    f"RAW: {tweet_content}\n"
                    f"CLEANED: {cleaned_text}\n"
                    f"SENTIMENT: {sentiment_label} (Score: {sentiment_score})\n"
                    f"MATCHED WORDS: {matched_words_str}\n"
                    f"{'-'*60}"
                )
                
                formatted_results.append(formatted_line)
                sentiment_counts[sentiment_label] += 1
                
            except Exception as e:
                print(f"Error processing tweet {tweet_id}: {e}")
                # Still add failed tweets to results for debugging
                error_result = {
                    'tweet_id': tweet_id,
                    'raw_text': tweet_content,
                    'cleaned_text': 'Error processing',
                    'sentiment_label': 'Error',
                    'sentiment_score': 0,
                    'matched_words': [],
                    'stored_in_db': False,
                    'error': str(e)
                }
                results.append(error_result)
                
                # Format error for UI
                formatted_line = (
                    f"Tweet ID: {tweet_id}\n"
                    f"RAW: {tweet_content}\n"
                    f"ERROR: {str(e)}\n"
                    f"{'-'*60}"
                )
                formatted_results.append(formatted_line)
                sentiment_counts['Error'] += 1
        
        # Generate summary statistics
        total_analyzed = sentiment_counts['Positive'] + sentiment_counts['Negative'] + sentiment_counts['Neutral']
        
        if total_analyzed > 0:
            summary = (
                f"\n{'='*60}\n"
                f"SENTIMENT ANALYSIS SUMMARY\n"
                f"{'='*60}\n"
                f"Total Tweets Analyzed: {total_analyzed}\n"
                f"Positive: {sentiment_counts['Positive']} ({(sentiment_counts['Positive']/total_analyzed*100):.1f}%)\n"
                f"Negative: {sentiment_counts['Negative']} ({(sentiment_counts['Negative']/total_analyzed*100):.1f}%)\n"
                f"Neutral: {sentiment_counts['Neutral']} ({(sentiment_counts['Neutral']/total_analyzed*100):.1f}%)\n"
                f"Errors: {sentiment_counts['Error']}\n"
                f"{'='*60}\n"
            )
        else:
            summary = "\nNo tweets were successfully analyzed.\n"
        
        return {
            'success': True,
            'message': f'Successfully analyzed {processed_count} tweets',
            'total_tweets': len(tweets),
            'processed_tweets': processed_count,
            'results': results,
            'formatted_results': formatted_results,
            'summary': summary,
            'sentiment_counts': sentiment_counts
        }
        
    except Exception as e:
        print(f"Error in analyze_tweets_for_ui: {e}")
        return {
            'success': False,
            'message': f'Error analyzing tweets: {str(e)}',
            'total_tweets': 0,
            'processed_tweets': 0,
            'results': [],
            'formatted_results': [],
            'summary': 'Analysis failed due to an error.',
            'sentiment_counts': {'Positive': 0, 'Negative': 0, 'Neutral': 0, 'Error': 0}
        }

def get_sentiment_summary():
    """
    Get a summary of stored sentiment analysis results from the database.
    """
    try:
        print("[DB] Getting sentiment summary from Supabase...")
        response = supabase.table("sentiments").select("label").execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"[DB] Error getting sentiment summary: {response.error}")
            return {}
        
        if isinstance(response, dict) and response.get("error"):
            print(f"[DB] Dict error getting sentiment summary: {response['error']}")
            return {}
        
        if hasattr(response, 'data') and response.data:
            # Count sentiments manually since Supabase doesn't support GROUP BY in basic queries
            sentiment_counts = {}
            for item in response.data:
                label = item['label']
                sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
            return sentiment_counts
        else:
            return {}
        
    except Exception as e:
        print(f"[DB] Exception getting sentiment summary: {e}")
        return {}

def save_movie_sentiment_to_db(movie_name, overall_sentiment, sentiment_counts, sentiment_score):
    """
    Save movie sentiment analysis results to database.
    Allows duplicate movie names to track sentiment history over time.
    Args:
        movie_name (str): Name of the movie
        overall_sentiment (str): Overall sentiment label
        sentiment_counts (dict): Counts of sentiments {'Positive': int, 'Negative': int, 'Neutral': int}
        sentiment_score (float): Overall sentiment score
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        from .db import get_db_connection  # Import the same connection function used by login
        
        # Calculate totals and percentages
        total_tweets = sum(sentiment_counts.values())
        if total_tweets == 0:
            print("[DB] No tweets to save sentiment for")
            return False
            
        positive_pct = (sentiment_counts.get("Positive", 0) / total_tweets) * 100
        negative_pct = (sentiment_counts.get("Negative", 0) / total_tweets) * 100
        neutral_pct = (sentiment_counts.get("Neutral", 0) / total_tweets) * 100
        
        # Get current timestamp
        analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connects to PostgreSQL database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert the movie sentiment data using SQL (same pattern as login)
        cur.execute("""
            INSERT INTO movie_sentiment_history 
            (movie_name, overall_sentiment, total_tweets_analyzed, 
             positive_count, negative_count, neutral_count,
             positive_percentage, negative_percentage, neutral_percentage,
             sentiment_score, analyzed_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            movie_name.strip(),
            overall_sentiment,
            total_tweets,
            sentiment_counts.get("Positive", 0),
            sentiment_counts.get("Negative", 0),
            sentiment_counts.get("Neutral", 0),
            round(positive_pct, 1),
            round(negative_pct, 1),
            round(neutral_pct, 1),
            round(sentiment_score, 3),
            analysis_time
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"[DB] Successfully saved movie sentiment for '{movie_name}' to PostgreSQL at {analysis_time}")
        return True
        
    except Exception as e:
        print(f"[DB] Error saving movie sentiment: {e}")
        return False

def analyze_tweets_directly(tweets_list, keyword=""):
    """
    Analyze sentiment of tweets directly from a list of tweet texts.
    Automatically saves movie sentiment to database using PostgreSQL
    """
    print(f"[DIRECT] Starting direct analysis of {len(tweets_list)} tweets for keyword: {keyword}")
    
    result = {
        'success': False,
        'message': '',
        'detailed_results': [],
        'sentiment_counts': {'Positive': 0, 'Negative': 0, 'Neutral': 0},
        'summary': '',
        'total_tweets': len(tweets_list)
    }
    
    if not tweets_list:
        result['message'] = "No tweets provided for analysis"
        return result
    
    try:
        analyzed_results = []
        
        for i, tweet_text in enumerate(tweets_list, 1):
            print(f"[DIRECT] Analyzing tweet {i}/{len(tweets_list)}")
            
            # Clean the tweet (returns list of tokens)
            cleaned_tokens = clean_tweet(tweet_text)
            
            # Convert tokens back to string for display
            cleaned_text = format_cleaned_text(cleaned_tokens)
            
            # Check if we have any tokens after cleaning
            if not cleaned_tokens or len(cleaned_tokens) == 0:
                print(f"[DIRECT] Skipping empty tweet {i} after cleaning")
                continue
            
            # Analyze sentiment using the tokens
            sentiment_label, sentiment_score, matched_words = analyze_sentiment(cleaned_tokens)
            
            # Store detailed result
            detailed_result = {
                'text': tweet_text[:100] + "..." if len(tweet_text) > 100 else tweet_text,
                'cleaned_text': cleaned_text,
                'sentiment': sentiment_label,
                'score': sentiment_score,
                'matched_words': matched_words
            }
            analyzed_results.append(detailed_result)
            
            # Update counts
            if sentiment_label in result['sentiment_counts']:
                result['sentiment_counts'][sentiment_label] += 1
            
            print(f"[DIRECT] Tweet {i}: {sentiment_label} (score: {sentiment_score})")
        
        # Create summary
        total_analyzed = len(analyzed_results)
        if total_analyzed > 0:
            counts = result['sentiment_counts']
            
            # Calculate percentages
            pos_pct = (counts['Positive'] / total_analyzed) * 100
            neg_pct = (counts['Negative'] / total_analyzed) * 100
            neu_pct = (counts['Neutral'] / total_analyzed) * 100
            
            # Calculate overall sentiment score
            pos_weight = counts['Positive']
            neg_weight = counts['Negative']
            total_weight = max(1, pos_weight + neg_weight)
            overall_score = (pos_weight - neg_weight) / total_weight
            
            # Determine overall sentiment
            if counts['Positive'] > counts['Negative'] and counts['Positive'] >= counts['Neutral']:
                overall_sentiment = "Positive"
            elif counts['Negative'] > counts['Positive'] and counts['Negative'] > counts['Neutral']:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"
            
            # Save movie sentiment to database using PostgreSQL (like login system)
            if keyword and keyword.strip():
                try:
                    save_success = save_movie_sentiment_to_db(
                        movie_name=keyword,
                        overall_sentiment=overall_sentiment,
                        sentiment_counts=counts,
                        sentiment_score=overall_score
                    )
                    if save_success:
                        print(f"[DB] Movie sentiment saved successfully for '{keyword}'")
                    else:
                        print(f"[DB] Failed to save movie sentiment for '{keyword}'")
                except Exception as e:
                    print(f"[DB] Error saving movie sentiment: {e}")
            
            result['detailed_results'] = analyzed_results
            result['success'] = True
            result['message'] = f"Successfully analyzed {total_analyzed} tweets"
            result['overall_sentiment'] = overall_sentiment
            result['sentiment_score'] = overall_score
            
        else:
            result['message'] = "No valid tweets could be analyzed after cleaning"
            
    except Exception as e:
        print(f"[DIRECT] Error during analysis: {e}")
        result['message'] = f"Analysis error: {e}"
        import traceback
        traceback.print_exc()
    
    print(f"[DIRECT] Analysis complete. Success: {result['success']}")
    return result