# app/sentiment_app.py

import tkinter as tk # Imports the main library for creating graphical windows.
from tkinter import messagebox # Imports a tool for simple alert messages (like pop-ups).
# Import the function to fetch tweets (relative import within the app package)
from .fetch_tweets import fetch_tweets_for_ui # Function to go get the movie tweets. Updated by Ryan on 11/3/2025
# Import the function to analyze sentiment (relative import within the app package)
from .analyze_sentiment import analyze_tweets # Function to clean the text and score the sentiment. Updated by Ryan on 11/3/2025

# Define Brand Colors and UI Constants (Colors used for the application's appearance)
BRAND_DARK_BLUE = "#1A237E" # Primary color for buttons and titles (Original).
LIGHT_GRAY_BG = "#F0F0F0" # Standard background color (Original).
ENTRY_BG = "#ffffff" # Background color for text entry fields. Updated by Ryan on 11/3/2025
ENTRY_FG = "#333333" # Foreground color for entry text. Updated by Ryan on 11/3/2025
BTN_BG = "#1A237E" # New background color for the combined button (Better contrast/call to action). Updated by Ryan on 11/3/2025
BTN_FG = "white" # Foreground (text) color for the button (Original was white). Updated by Ryan on 11/3/2025
BTN_BG_ACTIVE = "#1A237E" # Background color when a button is pressed. Updated by Ryan on 11/3/2025
BTN_FG_DISABLED = "#AAAAAA" # Foreground color for disabled buttons. Updated by Ryan on 11/3/2025

class SentimentAnalysisApp: # Defines the blueprint for the main application window.
    # TODO(Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page. # Note for the developer team (Original).
    def __init__(self, master): # This function runs when the main app window is created.
        self.master = master # Store the main Tkinter window (root).
        self.master.title("Libra Technology: Sentiment Analysis") # Sets the window title.
        self.master.geometry("600x450") # Sets the starting size of the window.
        self.master.configure(bg=LIGHT_GRAY_BG) # Sets the entire window's background color.

        # Data storage for current session
        self.current_tweets = [] # List to hold fetched tweets. Updated by Ryan on 11/3/2025
        self.current_keyword = "" # String to hold the last keyword searched. Updated by Ryan on 11/3/2025

        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20) # Creates a container frame for the elements.
        self.frame.pack(expand=True, fill=tk.BOTH) # Makes the frame expand and fill the window.

        # Main Title (Branded)
        tk.Label(self.frame, text="Libra Technology: Movie Sentiment Analysis Tool", 
                 font=("Helvetica", 16, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(pady=10) # Displays the branded title.

        # --- keyword entry box ---
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG) # Frame to hold the input area.
        keyword_frame.pack(pady=5) # Places the frame below the title.
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), 
                 bg=LIGHT_GRAY_BG).pack(side=tk.LEFT, padx=5) # Label prompting for the movie keyword.
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30) # The text box for the user to type in.
        self.keyword_entry.pack(side=tk.LEFT, padx=5) # Places the text box next to the label.

        # --- output text box with scrollbar ---
        text_frame = tk.Frame(self.frame) # Frame to hold the large text display area.
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True) # Places the frame and allows it to grow.
        scrollbar = tk.Scrollbar(text_frame) # Vertical scroll bar for long text output.
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Places the scrollbar on the right.

        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Arial", 12), yscrollcommand=scrollbar.set) # The main output box for messages and results.
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Places the text box next to the scrollbar.
        scrollbar.config(command=self.output_text.yview) # Connects the scrollbar to the text box.
        
        # Output Text Tags (for color-coding different output types)
        self.output_text.tag_config('pos', foreground='green', font=("Arial", 10, "bold")) # Tag for positive results (green text). Updated by Ryan on 11/3/2025
        self.output_text.tag_config('neg', foreground='red', font=("Arial", 10, "bold")) # Tag for negative results (red text). Updated by Ryan on 11/3/2025
        self.output_text.tag_config('title', foreground=BRAND_DARK_BLUE, font=("Arial", 12, "bold")) # Tag for section titles (blue, bold). Updated by Ryan on 11/3/2025
        self.output_text.tag_config('muted', foreground='#666666') # Tag for progress/less important messages (gray). Updated by Ryan on 11/3/2025

        # --- buttons ---
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG) # Frame to hold the action buttons.
        btn_frame.pack(pady=10) # Places the button frame at the bottom.

        # Combined Fetch & Analyze Button (Replaces two separate buttons)
        self.combined_button = tk.Button( # Creates the main button. Updated by Ryan on 11/3/2025
            btn_frame, # Place button in the button frame.
            text="Fetch & Analyze Sentiment", # New text for the combined action. Updated by Ryan on 11/3/2025
            command=self.fetch_and_analyze, # Calls the new combined function when clicked. Updated by Ryan on 11/3/2025
            font=("Arial", 12, "bold"), # Sets the font style. 
            bg=BTN_BG, fg=BTN_FG, # Sets the button color. Updated by Ryan on 11/3/2025
            activebackground=BTN_BG_ACTIVE, padx=10, pady=5 # Sets the color when pressed. Updated by Ryan on 11/3/2025
        ) 
        self.combined_button.pack(padx=5) # Packs the single button. Updated by Ryan on 11/3/2025
        # Original self.search_button and self.analysis_button functions were removed here. Updated by Ryan on 11/3/2025
        
    
    def append_output(self, output: str, tag=None): # Function to add status or result text to the output box.
        # TODO(Ayinde): Make sure output is user-friendly and clear. # Note for the developer team (Original).
        self.output_text.insert(tk.END, output + '\n', tag) # Adds the text with optional style tag (e.g., 'pos' for green). Updated by Ryan on 11/3/2025
        self.output_text.see(tk.END) # Scrolls the output box down to show the newest text.
        print(output) # Also prints the text to the developer's console.
    
    # Original open_fetch_tweets and open_sentiment_analysis functions were removed here. Updated by Ryan on 11/3/2025

    def fetch_and_analyze(self):
        """
        Fetches tweets and then immediately analyzes their sentiment, including
        detailed, color-coded output.
        Updated by Ryan on 11/6/2025
        """
        self.output_text.delete('1.0', tk.END) # Clear previous results in the text box.
        
        # Get and validate keyword
        try:
            keyword = self.keyword_entry.get().strip() # Get text and remove whitespace.
        except Exception:
            keyword = "" # Set keyword to empty if there's an error getting it.

        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword before proceeding.") # Show warning if empty.
            return # Stop execution.
            
        # 1. Start: Disable button to prevent spamming
        self.combined_button.config(state=tk.DISABLED, bg=BTN_FG_DISABLED) # Disable button and change color to show it's working.
        self.append_output("--- STARTING ANALYSIS ---", "title") # Log start message.

        # --- FETCHING TWEETS ---
        self.append_output(f"\n🔍 Searching for tweets related to: {keyword}...", "muted") # Log search progress.
        try:
            # Calls function from .fetch_tweets to get raw data.
            result = fetch_tweets_for_ui(keyword, count=10) # Call the fetch function, requesting up to 10 tweets.
            tweets = result.get("tweets", []) # Extract the list of tweets from the result.
            
            if not result.get("success") or not tweets:
                self.append_output("Fetching failed or returned no results.", "neg") # Report failure in red.
                self.combined_button.config(state=tk.NORMAL, bg=BTN_BG) # Re-enable button on failure.
                return # Stop execution.

            self.current_tweets = tweets # Store fetched tweets for analysis.
            self.current_keyword = keyword # Store keyword.
            self.append_output(f"Successfully fetched {len(tweets)} tweets.", "pos") # Report success in green.

        except Exception as e:
            self.append_output(f"Error fetching tweets: {e}", "neg") # Report unexpected error in red.
            messagebox.showerror("Fetch Error", f"Failed to fetch tweets: {e}") # Show pop-up error.
            self.combined_button.config(state=tk.NORMAL, bg=BTN_BG) # Re-enable button.
            return # Stop execution on fetch error.
            
        # --- SENTIMENT ANALYSIS ---
        self.append_output(f"\n🎬 Analyzing sentiment for {len(self.current_tweets)} tweets...", "muted") # Log analysis start.
        analysis_result = None # Initialize result variable.
        try:
            # Calls function from .analyze_sentiment to process the data.
            analysis_result = analyze_tweets(self.current_tweets, self.current_keyword) # Call the analysis function.
            
            if not analysis_result.get("success"):
                self.append_output(f"Analysis failed: {analysis_result.get('message', 'Unknown error')}", "neg") # Report analysis failure.
                self.combined_button.config(state=tk.NORMAL, bg=BTN_BG) # Re-enable button.
                return # Stop execution.

            # --- DISPLAY DETAILED TWEET RESULTS ---
            self.append_output("\n🔬 DETAILED TWEET ANALYSIS", "title") # Display title for detailed section.
            
            for i, detail in enumerate(analysis_result.get("detailed_results", [])): # Loop through each analyzed tweet.
                tweet_number = i + 1 # Tweet counter starting at 1.
                sentiment = detail["sentiment"] # Get the overall sentiment (Positive, Negative, Neutral).
                score = detail["score"] # Get the calculated score.
                raw_text = detail["text"] # Get the original tweet text.
                cleaned_text = detail["cleaned_text"] # Get the text after cleaning.
                matched_words = detail["matched_words"] # Get words that had a sentiment score.
                
                # Determine color tag for the overall tweet result
                sentiment_tag = 'pos' if sentiment == 'Positive' else 'neg' if sentiment == 'Negative' else 'muted' # Set color based on sentiment.
                
                # Display Tweet Metadata
                self.output_text.insert(tk.END, f"Tweet {tweet_number} ({sentiment}, Score: {score}):\n", sentiment_tag) # Insert numbered tweet with score and overall color.
                self.output_text.insert(tk.END, f"  RAW: {raw_text}\n", 'muted') # Insert raw text in muted color.
                
                # Format Cleaned Words with Color Coding
                self.output_text.insert(tk.END, "  WORDS: ") # Insert "WORDS:" label.
                cleaned_tokens = cleaned_text.split() # Split the cleaned text back into individual words.
                
                for word in cleaned_tokens: # Loop through each cleaned word.
                    # Check if the word contributed to the score
                    if word in matched_words: # If the word is one of the sentiment words.
                        # Color based on the word's contribution (using the overall sentiment as a simple guide for color).
                        if sentiment == "Positive":
                            self.output_text.insert(tk.END, f"{word} ", 'pos') # Highlight positive word in green.
                        elif sentiment == "Negative":
                            self.output_text.insert(tk.END, f"{word} ", 'neg') # Highlight negative word in red.
                        else:
                             self.output_text.insert(tk.END, f"{word} ", 'muted') # Highlight if neutral, but matched.
                    else:
                        self.output_text.insert(tk.END, f"{word} ", 'muted') # Neutral/unmatched words are muted (gray).
                        
                self.output_text.insert(tk.END, "\n" + "—" * 50 + "\n", 'muted') # Insert separating line.
                
            # --- DISPLAY SUMMARY RESULTS (Original Logic) ---
            counts = analysis_result.get("sentiment_counts", {}) # Get the total counts of sentiments.
            pos = counts.get("Positive", 0) # Count of positive tweets.
            neg = counts.get("Negative", 0) # Count of negative tweets.
            total = pos + neg + counts.get("Neutral", 0) # Total tweets analyzed.
            
            score = round((pos - neg) / max(1, total), 2) # Calculate the average net sentiment score.
            verdict_tag = "pos" if score > 0 else "neg" if score < 0 else "muted" # Determine final score color.

            self.append_output("\n📊 FINAL SENTIMENT REPORT", "title") # Display final summary title.
            self.append_output(f"Total Analyzed: {total} tweets", "muted") # Display total count.
            self.append_output(f"Positive Count: {pos}", "pos") # Display positive count in green.
            self.append_output(f"Negative Count: {neg}", "neg") # Display negative count in red.
            self.append_output(f"Net Sentiment Score: {score}", verdict_tag) # Display score with appropriate color.
            self.output_text.insert(tk.END, "—" * 50 + "\n", "muted") # Insert final separating line.
                
        except Exception as e:
            self.append_output(f"Error during analysis or display: {e}", "neg") # Log error during analysis/display.
            messagebox.showerror("Analysis Error", f"Failed to analyze or display sentiment: {e}") # Show pop-up error.
            
        finally:
            # 4. End: Re-enable button
            self.combined_button.config(state=tk.NORMAL, bg=BTN_BG) # Re-enable button and restore color.
            self.append_output("\n--- PROCESS COMPLETE ---", "title") # Log process completion.