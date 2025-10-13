# --- FILE: fetch_tweets.py ---

# Imports the necessary files and tools.
import sys # Tool to access system functions, specifically to read the keyword argument.
import os # Tool to manage file paths.
import csv # Tool for reading and writing data in a structured CSV format.
# Imports the Twitter API objects (client, api) created in the setup file.
from twitter_setup import client 

# Defines the name of the file where the raw tweets will be saved.
OUTPUT_FILE = "raw_tweets.txt" 
# Defines the number of tweets to fetch per query (a common practice for rate limiting).
MAX_TWEETS_PER_QUERY = 100 

# Check if the movie keyword was provided when the script was run.
if len(sys.argv) < 2:
    print("Error: No search keyword provided.")
    sys.exit(1) # Stops the script and reports an error.

# The keyword passed from the main application is the second argument (index 1).
movie_keyword = sys.argv[1] 

# The Twitter search query needs to specify the language and filter out retweets.
# 'lang:en' ensures only English tweets are returned.
query = f"{movie_keyword} -is:retweet lang:en" 

print(f"Searching Twitter (X) for: '{movie_keyword}'...") # Status update for the GUI.

try:
    # Use the Twitter API v2 Client (the modern standard) to search for tweets.
    # The search query is run, requesting the maximum number of tweets allowed per call.
    response = client.search_recent_tweets(
        query=query, 
        max_results=MAX_TWEETS_PER_QUERY
    )

    # Initialize a list to hold the text of all fetched tweets.
    tweets = []
    
    # Check if the response contains any data.
    if response.data:
        # Loop through each individual tweet object in the data.
        for tweet in response.data:
            # We only need the text content for sentiment analysis.
            tweets.append(tweet.text)
        
        # --- File Saving Logic ---
        # Opens the output file for writing, ensuring existing content is overwritten (w).
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # Writes each collected tweet text onto a new line in the file.
            for tweet_text in tweets:
                f.write(tweet_text + "\n")
        
        # Success status update for the main GUI.
        print(f"Successfully fetched and saved {len(tweets)} tweets to '{OUTPUT_FILE}'.")
    
    else:
        # If the search was successful but returned no tweets.
        print(f"No tweets found for the keyword: '{movie_keyword}'.")
        
except Exception as e:
    # Handles any network or API connection errors.
    print(f"An error occurred during Twitter fetching: {e}")
    sys.exit(1) # Stops the script on failure.