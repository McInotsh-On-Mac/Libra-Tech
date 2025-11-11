import psycopg2
import re
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from spellchecker import SpellChecker
import os
from datetime import datetime 
from app.utils.env_loader import load_env
load_env()

# Load environment variables
##load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Initialize tools and vocab
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
english_vocab = set(w.lower() for w in words.words())
spell = SpellChecker()

# Slang whitelist and shorthand map (Benjamin Herron)
slang_whitelist = {
    # Base list
    "u", "dm", "rn", "pls", "idk", "lol", "brb", "gtg", "lmao", "omg", "tbh",
    "afaik", "imho", "atp", "wya", "fr", "afk", "smh", "fomo", "yolo", "iykyk",

    # Extended list
    "143", "2day", "4eae", "adn", "ama", "amho", "b2b", "b2c", "b4n", "bfn",
    "f2f", "ftf", "f2p", "fubar", "fwb", "fyeo", "fyi", "fwiw", "glhf", "gm",
    "gn", "grwm", "hak", "hand", "hth", "idc", "im", "imo", "iirc", "irl",
    "iu2u", "iykwim", "jic", "jomo", "kfy", "kpc", "lmbo", "lmirl", "lsr",
    "myob", "nifoc", "nmu", "oic", "ootd", "op", "ot", "p2p", "qotd", "rotfl",
    "rt", "sm", "some", "tbd", "tbt", "tl;dr", "tt", "ttys", "ugt", "ugc",
    "wcw", "wtp", "ymmv", "csm", "diftp", "fyeo", "ftf", "g2g", "lmirl"
}

shorthand_map = {
    # Core list
    "u": "you",
    "dm": "direct message",
    "rn": "right now",
    "pls": "please",
    "idk": "i don't know",
    "lol": "laugh out loud",
    "brb": "be right back",
    "gtg": "got to go",
    "lmao": "laughing my ass off",
    "omg": "oh my god",
    "tbh": "to be honest",
    "afaik": "as far as i know",
    "imho": "in my humble opinion",
    "atp": "at this point",
    "wya": "where you at",
    "fr": "for real",
    "afk": "away from keyboard",
    "smh": "shaking my head",
    "fomo": "fear of missing out",
    "yolo": "you only live once",
    "iykyk": "if you know you know",

    # Extended mappings
    "143": "i love you",
    "2day": "today",
    "4eae": "forever and ever",
    "adn": "any day now",
    "ama": "ask me anything",
    "amho": "in my humble opinion",
    "b2b": "business to business",
    "b2c": "business to consumer",
    "b4n": "bye for now",
    "bfn": "bye for now",
    "f2f": "face to face",
    "ftf": "face to face",
    "f2p": "free to play",
    "fubar": "fouled up beyond all recognition",
    "fwb": "friends with benefits",
    "fyeo": "for your eyes only",
    "fyi": "for your information",
    "fwiw": "for what it's worth",
    "glhf": "good luck have fun",
    "gm": "good morning",
    "gn": "good night",
    "grwm": "get ready with me",
    "hak": "hugs and kisses",
    "hand": "have a nice day",
    "hth": "hope this helps",
    "idc": "i don't care",
    "im": "instant message",
    "imo": "in my opinion",
    "iirc": "if i recall correctly",
    "irl": "in real life",
    "iu2u": "it's up to you",
    "iykwim": "if you know what i mean",
    "jic": "just in case",
    "jomo": "joy of missing out",
    "kfy": "kiss for you",
    "kpc": "keep parents clueless",
    "lmbo": "laughing my butt off",
    "lmirl": "let's meet in real life",
    "lsr": "loser",
    "myob": "mind your own business",
    "nifoc": "naked in front of computer",
    "nmu": "not much, you?",
    "oic": "oh, i see",
    "ootd": "outfit of the day",
    "op": "original poster",
    "ot": "off topic",
    "p2p": "peer to peer",
    "qotd": "quote of the day",
    "rotfl": "rolling on the floor laughing",
    "rt": "retweet",
    "sm": "social media",
    "some": "shout out my ex",
    "tbd": "to be determined",
    "tbt": "throwback thursday",
    "tl;dr": "too long; didn't read",
    "tt": "talk to",
    "ttys": "talk to you soon",
    "ugt": "you got this",
    "ugc": "user-generated content",
    "wcw": "woman crush wednesday",
    "wtp": "what’s the plan",
    "ymmv": "your mileage may vary",
    "csm": "commenting for better reach",
    "diftp": "do it for the plot",
    "g2g": "got to go"
}



#sentiment dictionary (Benjamin Herron)
sentiment_dict = {
    # Strong Positive Words
   "masterpiece": 5, "blockbuster": 5, "must-watch": 5, "award-worthy": 5, "oscar-worthy": 5, 
   "breathtaking": 5, "phenomenal": 5, "spectacular": 5, "stunning": 5, "incredible": 5, "legendary": 5, 
   "groundbreaking": 5, "emotionally-powerful": 5, "iconic": 5, "revolutionary": 5, "perfection": 5, 
   "unforgettable": 5, "flawless": 5, "timeless": 5, "brilliantly-crafted": 5, "peak-cinema": 5, "love": 5,
   "masterful": 5, "transformative": 5, "triumphant": 5, "breathtakingly-beautiful": 5,

    "epic": 4, "amazing": 4, "awesome": 4, "brilliant": 4, "fantastic": 4,
    "excellent": 4, "outstanding": 4, "thrilling": 4, "wonderful": 4, "mind-blowing": 4,
    "gripping": 4, "electrifying": 4, "remarkable": 4, "heartwarming": 4, "thought-provoking": 4,
    "well-acted": 4, "visually-striking": 4, "inspiring": 4, "emotional": 4, "hilarious": 4,
    "motivating": 4, "joyful": 4, "rewarding": 4, "uplifting": 4, "refreshing": 4,
    "enjoyable": 4, "powerful": 4, "mind-expanding": 4, "captivating": 4, "masterfully-directed": 4,
    "visually-stunning": 4, "tight-script": 4, "brilliant-performance": 4, "moving": 4, "elegant": 4,
    "well-paced": 4, "immersive": 4, "emotional-journey": 4, "genius": 4,
    "beautiful": 4, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4, "enthusiastic": 4,
    "delightful": 4, "optimistic": 4, "fulfilling": 4, "wholesome": 4, "soulful": 4,
    "poetic": 4, "dreamlike": 4, "satisfying-ending": 4, "heart-touching": 4,
    "strong-narrative": 4,

    # Neutral Words
    "okay": 0, "neutral": 0, "average": 0, "decent": 1, "plain": 1,
    "standard": 1, "typical": 0, "moderate": 1, "simple": 1, "fine": 1,
    "passable": 1, "straightforward": 1, "uncomplicated": 1, "serviceable": 1, "middle-of-the-road": 0,
    "meh": 0, "acceptable": 1, "normal": 1, "basic": 1, "regular": 1,
    "expected": 1, "predictable": -1, "forgettable": -1, "formulaic": -1, "plain-jane": 0,
    "scary": -1, "surprised": 1, "reflective": 1, "subdued": 0, "mellow": 1,
    "understated": 1, "grounded": 1, "minimalistic": 1, "realistic": 1, "moody": 0,
    "introspective": 1, "ambiguous": 0, "ordinary": 0, "steady": 1, "contemplative": 1,
    "surreal": 2, "toned-down": 0,

    # Negative Words
    "mediocre": -1, "predictable": -1, "forgettable": -1, "formulaic": -1, "slow": -2,
    "uninspired": -2, "cliché": -2, "unrealistic": -2, "dry": -2, "flat": -2,
    "underdeveloped": -2, "confusing": -2, "lackluster": -2, "awkward": -2, "weak": -2,
    "repetitive": -2, "safe": -2, "thin": -2, "shaky": -2, "clunky": -2,
    "overused": -2, "dull": -3, "unoriginal": -3, "underwhelming": -3, "overrated": -3,
    "cheesy": -3, "forced": -3, "messy": -3, "lifeless": -4, "dragging": -3,
    "plot holes": -3, "wooden acting": -3, "bad CGI": -3, "annoying": -3, "frustrating": -3,
    "meaningless": -3, "empty": -3, "poorly-executed": -3, "disjointed": -3, "nonsensical": -3,
    "ridiculous": -3, "over-the-top": -3, "flat-characters": -3, "exaggerated": -3,
    "boring": -4, "disappointing": -4, "flop": -4, "cringe": -4, "waste": -4,
    "waste-of-time": -4, "cringeworthy": -4, "shocking": -4, "disturbing": -4, "forced-dialogue": -4,
    "painful": -5, "horrible": -5, "terrible": -5, "trash": -5, "worst": -5,
    "atrocious": -5, "devastating": -5, "horrific": -5, "disgusting": -5, "hate": -5,
    "angry": -5, "unwatchable": -5, "nauseating": -5, "garbage": -5, "insulting": -5,
    "anticlimactic": -3, "unconvincing": -3, "pretentious": -4, "hollow": -3, "lifeless-performance": -3,
    "melodramatic": -3, "soulless": -4, "lazy": -3, "sloppy": -3, "clumsy": -3,
    "painful-dialogue": -4, "generic": -2, "flat-ending": -3, "pointless": -4, "shallow": -3,
    "unpleasant": -3, "gloomy": -2, "depressing": -3, "hopeless": -4, "furious": -4,
    "bitter": -3, "rage-filled": -4, "anxious-energy": -2, "messy-editing": -3,
    "inconsistent": -2, "overstuffed": -2, "chaotic": -3, "overly-long": -2, "tedious": -3,

    # Strong Emotions (Positive & Negative)
    "love": 5, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4, "enthusiastic": 4,
    "hate": -5, "angry": -5, "frustrated": -4, "disgusting": -5, "horrific": -5,
    "devastating": -5, "shocking": -4, "unbelievable": -3, "scary": -3, "disturbing": -4,
    "hopeful": 3, "content": 3, "furious": -4, "bitter": -3,

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

# (Jania) Save movie sentiment to database function
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

# (Benjamin) Analyze tweets function
def analyze_tweets(tweets_list, keyword=""):
    """
    Analyze sentiment of tweets directly from a list of tweet texts.
    Automatically saves movie sentiment to database using PostgreSQL
    """
    print(f"Starting analysis of {len(tweets_list)} tweets for keyword: {keyword}")
    
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
            print(f"Analyzing tweet {i}/{len(tweets_list)}")
            
            # Clean the tweet (returns list of tokens)
            cleaned_tokens = clean_tweet(tweet_text)
            
            # Convert tokens back to string for display
            cleaned_text = format_cleaned_text(cleaned_tokens)
            
            # Check if we have any tokens after cleaning
            if not cleaned_tokens or len(cleaned_tokens) == 0:
                print(f"Skipping empty tweet {i} after cleaning")
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
            
            print(f"Tweet {i}: {sentiment_label} (score: {sentiment_score})")
        
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
            
            # Save movie sentiment to database using PostgreSQL
            if keyword and keyword.strip():
                try:
                    save_success = save_movie_sentiment_to_db(
                        movie_name=keyword,
                        overall_sentiment=overall_sentiment,
                        sentiment_counts=counts,
                        sentiment_score=overall_score
                    )
                    if save_success:
                        print(f"Movie sentiment saved successfully for '{keyword}'")
                    else:
                        print(f"Failed to save movie sentiment for '{keyword}'")
                except Exception as e:
                    print(f"Error saving movie sentiment: {e}")

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