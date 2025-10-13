import nltk # Imports the Natural Language Toolkit, a core library for analyzing text.
import re # Imports a tool for searching and manipulating strings (like removing links).
import string # Imports a list of standard punctuation characters.
from nltk.corpus import stopwords, words # Imports lists of common words (like 'the', 'a') and the entire English dictionary.
from nltk.stem import WordNetLemmatizer # Imports a tool to reduce words to their base form (e.g., 'running' -> 'run').
from nltk import word_tokenize, pos_tag # Imports tools to break sentences into words and identify their grammatical role (noun, verb, etc.).
from nltk.corpus import wordnet # Imports a large lexical database used by the lemmatizer.
from spellchecker import SpellChecker # Imports a tool to check and suggest corrections for misspelled words.
import sys # Imports a tool to access system functions (used for arguments, but mainly for clean execution here).


# Initialize tools and vocab
stop_words = set(stopwords.words('english')) # Loads the list of very common English words we want to ignore.
lemmatizer = WordNetLemmatizer() # Creates the tool that finds the base form of words.
# Loads the entire English vocabulary for checking if a word is real.
english_vocab = set(w.lower() for w in words.words())
spell = SpellChecker() # Creates the tool that checks spelling.

# Slang whitelist and shorthand map
# A list of common social media abbreviations that we should NOT try to correct or remove.
slang_whitelist = {"u", "dm", "rn", "plz" ,"pls", "idk", "lol", "brb", "gtg", "lmao", "omg", "tbh", "ngl", "afaik", "i0mho", "imo"}
shorthand_map = {
    "u": "you",
    "dm": "direct message",
    "rn": "right now",
    "pls": "please",
    "plz": "please",
    "idk": "i don't know",
    "lol": "laugh out loud",
    "gtg": "got to go",
    "brb": "be right back",
    "lmao": "laughing my ass off",
    "omg": "oh my god",
    "tbh": "to be honest",
    "ngl": "not gonna lie",
    "afaik": "as far as i know",
    "imho": "in my humble opinion",
    "imo": "in my opinion"
}

#sentiment dictionary
# This dictionary assigns a positive or negative score to various keywords.
# Scores range from 5 (Strong Positive) to -5 (Strong Negative).
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

# Function to translate a standard grammatical tag (from NLTK) into a format the lemmatizer understands.
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'): # J means Adjective
        return wordnet.ADJ
    elif treebank_tag.startswith('V'): # V means Verb
        return wordnet.VERB
    elif treebank_tag.startswith('N'): # N means Noun
        return wordnet.NOUN
    elif treebank_tag.startswith('R'): # R means Adverb
        return wordnet.ADV
    else:
        return wordnet.NOUN # Defaults to Noun if the role is unclear.

# Function to clean the tweet
def clean_tweet(tweet):
    tweet = tweet.lower() # Converts all text to lowercase for consistent processing.


    # Step 1: Replace shorthand terms first
    # Looks for and replaces shorthand (like 'lol') with the full meaning before removing punctuation.
    for word, replacement in shorthand_map.items():
        tweet = re.sub(rf'\b{re.escape(word)}\b', replacement, tweet)

    # Step 2: Remove URLs, RTs, mentions, hashtags, digits, punctuation
    tweet = re.sub(r'rt\s+', '', tweet) # Removes Twitter-specific 'RT' (retweet) markers.
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet) # Removes web links (URLs).
    tweet = re.sub(r'#\w+', '', tweet) # Removes hashtags (the # symbol and the word).
    tweet = re.sub(r'@\w+', '', tweet) # Removes user mentions (the @ symbol and the username).
    tweet = re.sub(r'\d+', '', tweet) # Removes all numbers (digits).
    tweet = re.sub(r'[^\w\s]', '', tweet) # Removes all remaining punctuation.
    tweet = re.sub(r'\s+', ' ', tweet).strip() # Removes extra spaces created during the cleanup.

    # Step 3: Tokenize
    tokens = word_tokenize(tweet) # Breaks the cleaned sentence into a list of individual words (tokens).

    # Step 4: Remove custom blacklisted words
    blacklist = {'aku', 'gama'} # Defines specific words to be blocked (e.g., non-English words).
    tokens = [word for word in tokens if word not in blacklist] # Filters out the blacklisted words.

    # Step 5: POS tagging and lemmatization
    pos_tags = pos_tag(tokens) # Identifies the grammatical role (Part-of-Speech, POS) of each word.
    cleaned_tokens = []
    
    # Loop through each word and its grammatical tag.
    for word, tag in pos_tags:
        # If the word is a whitelisted slang term, skip the processing and keep it as is.
        if word in slang_whitelist:
            cleaned_tokens.append(word)
            continue

        wordnet_pos = get_wordnet_pos(tag) # Finds the correct POS tag format for the lemmatizer.
        lemma = lemmatizer.lemmatize(word, wordnet_pos) # Reduces the word to its base form ('running' -> 'run').

        # Final check: only keeps words that meet these conditions:
        if (
            lemma not in stop_words and # 1. It's not a common stop word (like 'is', 'at').
            (len(lemma) > 1 or lemma in shorthand_map) and # 2. It's longer than 1 letter (or it was a known shorthand).
            # 3. It's a real English word OR the spelling is already correct.
            (lemma in english_vocab or spell.correction(lemma) == lemma)
        ):
            cleaned_tokens.append(lemma) # Adds the final, cleaned word to the list.

    return cleaned_tokens # Returns the final list of analysis-ready words.

# Function to reassemble the cleaned words back into a sentence.def format_cleaned_text(tokens):
    return ' '.join(tokens)

# Function to calculate the sentiment score for a list of words.
def analyze_sentiment(tokens):
    score = 0
    for token in tokens:
        # Looks up the word in the dictionary and adds its score (0 if not found).
        score += sentiment_dict.get(token, 0)
    
    # Classifies the overall score into a simple label (Positive, Negative, Neutral).
    if score > 0:
        return "Positive", score
    elif score < 0:
        return "Negative", score
    else:
        return "Neutral", score

# Load and clean tweets
try:
    # Opens the file where the raw tweets (fetched by fetch_tweets.py) are stored.
    with open("raw_tweets.txt", "r", encoding="utf-8") as f:
        # Reads all tweets, removes duplicates (using set), and puts them in a list.
        raw_tweets = list(set(line.strip() for line in f if line.strip()))
except FileNotFoundError:
    print("Error: 'raw_tweets.txt' not found. Please run tweet fetching first.")
    sys.exit(1) # Stops the program if the file isn't there.

# Analyze and prepare results
output_lines = [] # List to hold the final formatted analysis results.
cleaned_tweet_lines = [] # List to hold just the cleaned text for saving.

# Loop through every single raw tweet loaded from the file.
for raw in raw_tweets:
    cleaned_tokens = clean_tweet(raw) # 1. Cleans the tweet and gets a list of words.
    cleaned_text = format_cleaned_text(cleaned_tokens) # 2. Re-joins the cleaned words into a sentence.
    sentiment_label, sentiment_score = analyze_sentiment(cleaned_tokens) # 3. Calculates the score and label.

    # Prepare formatted line
    result_line = f"RAW: {raw}\nCLEANED: {cleaned_text}\nSENTIMENT: {sentiment_label} (Score: {sentiment_score})\n{'-'*50}"
    print(result_line)  # Output to console
    output_lines.append(result_line)

    #store cleaned tweets in a list for saving later
    cleaned_tweet_lines.append(cleaned_text)

# Save cleaned tweets
with open("cleaned_tweets.txt", "w", encoding="utf-8") as f:
    for line in cleaned_tweet_lines:
        f.write(line + "\n")

# Save analysis results
with open("tweet_analysis_results.txt", "w", encoding="utf-8") as f:
    for line in output_lines:
        f.write(line + "\n")

# Prints a final status message to the GUI.
print("Analysis complete! Full results saved to 'tweet_analysis_results.txt'.")