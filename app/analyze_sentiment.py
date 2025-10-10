import psycopg2
import re
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from spellchecker import SpellChecker
import os
from .db import get_db_connection


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
    "angry": -5, "unwatchable": -5, "nauseating": -5, "garbage": -5, "insulting": -5, "anxious": -2, "terrifying": -3,  "surprised": 1, "tense": -1, "tearjerker": 4, "beautiful": 4, "nostalgic": 1,



    # Strong Emotions (Positive & Negative)
    "love": 5, "excited": 4, "joy": 4, "funny": 4, "satisfying": 4, "enthusiastic": 4,
    "hate": -5, "angry": -5, "frustrated": -4, "disgusting": -5, "horrific": -5,
    "devastating": -5, "shocking": -4, "unbelievable": -3, "scary": -3, "disturbing": -4,

    # Common Words From Twitter
    "fire": 4, "goat": 5, "slaps": 4, "based": 4, "mid": -2,
    "wack": -3, "overhyped": -3, "underrated": 3, "slept-on": 3, "dead": -3,
    "chef’s-kiss": 5, "vibes": 3, "badass": 4, "yawn": -3, "lit": 4,
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

#format cleaned tokens for writing
def format_cleaned_text(tokens):
    return ' '.join(tokens)

def analyze_sentiment(tokens):
    score = 0
    for token in tokens:
        score += sentiment_dict.get(token, 0)
    if score > 0:
        return "Positive", score
    elif score < 0:
        return "Negative", score
    else:
        return "Neutral", score
    



# TODO: Function to fetch tweets from DB (to be implemented)
def fetch_tweets_from_db():
    pass

# TODO: Function to store cleaned tweet in DB (to be implemented)
def store_sentiment_in_db(tweet_id, label, score):
    pass

# TODO: Function to analyze tweets in DB (to be implemented)
def analyze_tweets_in_db():
    """
    Fetches tweets from DB, analyzes sentiment, and stores results in DB.
    Returns a list of dicts for UI display.
    """
    pass

# Load and clean tweets
# TODO(Ben): Use fetch_tweets_from_db method instead of reading from a file.
# TODO(Ben): Refactor code below into analyze_tweets_in_db method.
with open("raw_tweets.txt", "r", encoding="utf-8") as f:
    raw_tweets = list(set(line.strip() for line in f if line.strip()))

# Analyze and prepare results
output_lines = []
cleaned_tweet_lines = []

for raw in raw_tweets:
    cleaned_tokens = clean_tweet(raw)
    cleaned_text = format_cleaned_text(cleaned_tokens)
    sentiment_label, sentiment_score = analyze_sentiment(cleaned_tokens)

    # Prepare formatted line
    result_line = f"RAW: {raw}\nCLEANED: {cleaned_text}\nSENTIMENT: {sentiment_label} (Score: {sentiment_score})\n{'-'*50}"
    print(result_line)  # Output to console
    output_lines.append(result_line)

    #store cleaned tweets in a list for saving later
    cleaned_tweet_lines.append(cleaned_text)
