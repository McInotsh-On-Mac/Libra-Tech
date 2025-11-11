<<<<<<< HEAD
# app/sentiment_app.py

import tkinter as tk # Imports the main library for creating graphical windows.
from tkinter import messagebox # Imports a tool for simple alert messages (like pop-ups).
# Import the function to fetch tweets (relative import within the app package)
from .fetch_tweets import fetch_tweets_for_ui # Function to go get the movie tweets. Updated by Ryan on 11/3/2025
# Import the function to analyze sentiment (relative import within the app package)
from .analyze_sentiment import analyze_tweets # Function to clean the text and score the sentiment. Updated by Ryan on 11/3/2025
=======
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Notebook
import datetime  # for timestamps
import requests  # for api calls
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .sample_tweets import generate_sample_tweets  # Use sample tweets instead
from .fetch_tweets import fetch_tweets_for_ui  # Real API fetcher
from .chart_sentiment import create_sentiment_charts
from .analyze_sentiment import analyze_sentiment  # Import analyze_sentiment function
>>>>>>> f715db17172f8a51fe3fcbcc1e3593d1653be9f2

# Define Brand Colors and UI Constants (Colors used for the application's appearance)
BRAND_DARK_BLUE = "#1A237E" # Primary color for buttons and titles (Original).
LIGHT_GRAY_BG = "#F0F0F0" # Standard background color (Original).
ENTRY_BG = "#ffffff" # Background color for text entry fields. Updated by Ryan on 11/3/2025
ENTRY_FG = "#333333" # Foreground color for entry text. Updated by Ryan on 11/3/2025
BTN_BG = "#1A237E" # New background color for the combined button (Better contrast/call to action). Updated by Ryan on 11/3/2025
BTN_FG = "white" # Foreground (text) color for the button (Original was white). Updated by Ryan on 11/3/2025
BTN_BG_ACTIVE = "#1A237E" # Background color when a button is pressed. Updated by Ryan on 11/3/2025
BTN_FG_DISABLED = "#AAAAAA" # Foreground color for disabled buttons. Updated by Ryan on 11/3/2025

<<<<<<< HEAD
class SentimentAnalysisApp: # Defines the blueprint for the main application window.
    # TODO(Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page. # Note for the developer team (Original).
    def __init__(self, master): # This function runs when the main app window is created.
        self.master = master # Store the main Tkinter window (root).
        self.master.title("Libra Technology: Sentiment Analysis") # Sets the window title.
        self.master.geometry("600x450") # Sets the starting size of the window.
        self.master.configure(bg=LIGHT_GRAY_BG) # Sets the entire window's background color.
=======
# new high-contrast ui tokens
BTN_BG           = "#304FFE"   # bright blue button
BTN_BG_ACTIVE    = "#1E40FF"   # darker on press
BTN_FG           = "#000000"   # black text for readability
BTN_FG_DISABLED  = "#333333"   # dim black when disabled
ENTRY_BG         = "#FFFFFF"   # white input bg
ENTRY_FG         = "#FFFFFF"   # white typing
ENTRY_PLACEHOLDER= "#8A8A8A"   # gray placeholder
SELECTION_BG     = "#CCE0FF"
SELECTION_FG     = "#000000"
CARET_COLOR      = "#000000"
>>>>>>> f715db17172f8a51fe3fcbcc1e3593d1653be9f2

        # Data storage for current session
        self.current_tweets = [] # List to hold fetched tweets. Updated by Ryan on 11/3/2025
        self.current_keyword = "" # String to hold the last keyword searched. Updated by Ryan on 11/3/2025

<<<<<<< HEAD
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
=======
class SentimentAnalysisApp:
    # (Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page.
    def __init__(self, master):
        # window setup
        self.master = master
        self.master.title("Libra Technology: Sentiment Analysis")
        self.master.geometry("1200x800")  # Wider window to accommodate header
        self.master.configure(bg=LIGHT_GRAY_BG)

        # store fetched tweets + keyword
        self.current_tweets = []
        self.current_keyword = ""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)  # Increased padding
        
        # Create main analysis tab
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Analysis")
        
        # Create charts tab
        self.charts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_tab, text="Charts")
        
        # Initialize main analysis tab
        self.init_analysis_tab()
        
        # Initialize charts tab
        self.init_charts_tab()

    def init_analysis_tab(self):
        # Main frame for the Analysis tab
        self.frame = tk.Frame(self.analysis_tab, bg=LIGHT_GRAY_BG, padx=30, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Main Title
        tk.Label(self.frame, text="Libra Technology: Movie Sentiment Analysis Tool",
                 font=("Helvetica", 16, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(pady=10)

        # Keyword Entry
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12),
                 bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(side=tk.LEFT, padx=5)
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # Placeholder and focus handlers
        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"
        self._set_entry_placeholder()
        self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out)

        # Output Text Box with Scrollbar
        text_frame = tk.Frame(self.frame)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=12,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set,
            bg="#FFFFFF",  # White background for better readability
            fg="#000000"   # Default text color (black)
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Define Output Text Tags for clarity
        self.output_text.tag_config('pos', foreground='#228B22', font=("Arial", 10, "bold"))  # Green for positive
        self.output_text.tag_config('neg', foreground='#B22222', font=("Arial", 10, "bold"))  # Red for negative
        self.output_text.tag_config('neutral', foreground='#808080', font=("Arial", 10, "italic"))  # Gray for neutral
        self.output_text.tag_config('title', foreground=BRAND_DARK_BLUE, font=("Arial", 12, "bold"))  # Blue for titles
        self.output_text.tag_config('muted', foreground='#A9A9A9')  # Light gray for less important messages
        self.output_text.tag_config('separator', foreground='#000000', font=("Arial", 10))  # Black for separators

        # --- buttons ---
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)  # Frame to hold the action buttons.
        btn_frame.pack(pady=10)  # Places the button frame at the bottom.

        # Combined Fetch + Analyze button (single control)
        self.fetch_analyze_button = tk.Button(
            btn_frame,
            text="Fetch & Analyze",
            command=lambda: self.open_fetch_tweets(do_analyze=True),
            font=("Arial", 12, "bold"),
            bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10, pady=5, highlightthickness=0
        )
        self.fetch_analyze_button.grid(row=0, column=0, padx=5)

    def _set_entry_placeholder(self):
        # put placeholder text and set gray color
        self.keyword_entry.delete(0, tk.END)
        self.keyword_entry.insert(0, self.placeholder_text)
        self.keyword_entry.config(fg=ENTRY_PLACEHOLDER)

    def _on_entry_focus_in(self, _event=None):
        # when focusing, if placeholder shown, clear and set black typing color
        if self.keyword_entry.get() == self.placeholder_text and self.keyword_entry.cget("fg") == ENTRY_PLACEHOLDER:
            self.keyword_entry.delete(0, tk.END)
            self.keyword_entry.config(fg=ENTRY_FG)

    def _on_entry_focus_out(self, _event=None):
        # when leaving, if empty, restore placeholder
        if not self.keyword_entry.get().strip():
            self._set_entry_placeholder()

    def init_charts_tab(self):
        # Create frame for charts
        self.charts_frame = tk.Frame(self.charts_tab, bg=LIGHT_GRAY_BG)
        self.charts_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Create notebook for different time windows
        self.charts_notebook = ttk.Notebook(self.charts_frame)
        self.charts_notebook.pack(expand=True, fill=tk.BOTH)
        
        # Create frames for each time window
        self.chart_frames = {}
        for window in ['24h', '30d', '60d']:
            frame = ttk.Frame(self.charts_notebook)
            self.charts_notebook.add(frame, text=f'Last {window}')
            self.chart_frames[window] = frame

    def append_output(self, output, tag=None):
        """
        Append a message to the output text box with an optional tag for styling.
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")  # Add a timestamp
        try:
            # Prefix timestamp
            self.output_text.insert(tk.END, f"[{ts}] ", "muted")
            if tag == 'separator':
                self.output_text.insert(tk.END, "—" * 50 + "\n", tag)  # Add a horizontal separator
            elif tag == 'title':
                self.output_text.insert(tk.END, f"🔹 {output}\n", tag)  # Add a blue bullet for titles
            elif tag == 'pos':
                self.output_text.insert(tk.END, f"✅ {output}\n", tag)  # Add a green checkmark for positive
            elif tag == 'neg':
                self.output_text.insert(tk.END, f"❌ {output}\n", tag)  # Add a red cross for negative
            elif tag == 'neutral':
                self.output_text.insert(tk.END, f"⚪ {output}\n", tag)  # Add a white circle for neutral
            else:
                self.output_text.insert(tk.END, output + "\n", tag)  # Default behavior

            self.output_text.see(tk.END)  # Scroll to the bottom
        except Exception:
            # Fallback to simple insert in case of tag issues
            self.output_text.insert(tk.END, output + "\n")
            self.output_text.see(tk.END)

        # Also print to stdout for debugging
        print(output)

    # (Benjamin) Fetch tweets function
    # (Ayinde) Design output formatting for fetched tweets and analysis results
    def update_charts(self):
        """Update all sentiment charts with new data"""
        try:
            # Clear existing charts
            for frame in self.chart_frames.values():
                for widget in frame.winfo_children():
                    widget.destroy()
            
            # Create new charts
            charts = create_sentiment_charts()
            
            # Add charts to their respective frames
            for window, chart in charts.items():
                canvas = FigureCanvasTkAgg(chart, master=self.chart_frames[window])
                canvas.draw()
                canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
                
            self.notebook.select(self.charts_tab)  # Switch to charts tab
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to update charts: {e}")

    def open_fetch_tweets(self, do_analyze=False):
        """
        Fetch tweets based on the keyword entered by the user using fetch_tweets_for_ui.
        """
        kw = self.keyword_entry.get().strip()
        if not kw or (kw == self.placeholder_text and self.keyword_entry.cget("fg") == ENTRY_PLACEHOLDER):
            messagebox.showwarning("Input Error", "Please enter a movie keyword.")
            return

        # disable UI during fetch
        try:
            self.fetch_analyze_button.config(state=tk.DISABLED, bg="#BDBDBD")
        except Exception:
            pass

        self.append_output(f"🔍 Fetching tweets for: {kw} ...", "muted")
>>>>>>> f715db17172f8a51fe3fcbcc1e3593d1653be9f2

        # --- FETCHING TWEETS ---
        self.append_output(f"\n🔍 Searching for tweets related to: {keyword}...", "muted") # Log search progress.
        try:
<<<<<<< HEAD
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
=======
            # Try live fetch first; if it fails (credentials missing or API error), fall back to sample tweets
            result = fetch_tweets_for_ui(kw, count=50)
            if not result.get("success"):
                # fallback when credentials missing or API error
                self.append_output("Live fetch failed or credentials missing; falling back to sample tweets.", "muted")
                result = generate_sample_tweets(kw, count=6)

            if result and result.get("success"):
                raw = result.get("tweets", [])
                # normalize to plain text strings for analysis
                normalized = []
                for t in raw:
                    if isinstance(t, dict):
                        normalized.append(t.get('text') or t.get('full_text') or str(t))
                    else:
                        normalized.append(str(t))
                self.current_tweets = normalized
                self.current_keyword = kw
>>>>>>> f715db17172f8a51fe3fcbcc1e3593d1653be9f2

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

<<<<<<< HEAD
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
                
=======
                for i, text in enumerate(self.current_tweets, 1):
                    self.append_output(f"{i}. {text}")

                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                self.append_output("Tweets ready for analysis!", "muted")

                # Update charts with new data
                self.update_charts()
                # If caller requested analysis immediately after fetch, run it
                if do_analyze:
                    self.open_sentiment_analysis()
            else:
                self.append_output(f"{result.get('message', 'Failed to fetch tweets')}", "neg")
                self.current_tweets = []
>>>>>>> f715db17172f8a51fe3fcbcc1e3593d1653be9f2
        except Exception as e:
            self.append_output(f"Error during analysis or display: {e}", "neg") # Log error during analysis/display.
            messagebox.showerror("Analysis Error", f"Failed to analyze or display sentiment: {e}") # Show pop-up error.
            
        finally:
<<<<<<< HEAD
            # 4. End: Re-enable button
            self.combined_button.config(state=tk.NORMAL, bg=BTN_BG) # Re-enable button and restore color.
            self.append_output("\n--- PROCESS COMPLETE ---", "title") # Log process completion.
=======
            try:
                self.fetch_analyze_button.config(state=tk.NORMAL, bg=BTN_BG)
            except Exception:
                pass

    # (Jania) Sentiment analysis function
    def open_sentiment_analysis(self):
        """
        Analyze the currently fetched tweets and provide a comprehensive summary.
        """
        if not self.current_tweets:
            self.append_output("No tweets to analyze. Please fetch tweets first.", "neg")
            return

        self.append_output("Starting comprehensive sentiment analysis...", "title")
        self.append_output("", "separator")

        # Initialize counters
        total_score = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Analyze all tweets
        for tweet in self.current_tweets:
            sentiment, score, matched_words = analyze_sentiment(tweet.split())
            total_score += score

            if sentiment == "Positive":
                positive_count += 1
            elif sentiment == "Negative":
                negative_count += 1
            else:
                neutral_count += 1

        # Calculate positivity score
        total_tweets = len(self.current_tweets)
        positivity_score = (positive_count / total_tweets) * 100 if total_tweets > 0 else 0

        # Display comprehensive analysis
        self.append_output("Comprehensive Sentiment Analysis Results:", "title")
        self.append_output("", "separator")
        self.append_output(f"Total Tweets Analyzed: {total_tweets}", "muted")
        self.append_output(f"Positive Tweets: {positive_count}", "pos")
        self.append_output(f"Negative Tweets: {negative_count}", "neg")
        self.append_output(f"Neutral Tweets: {neutral_count}", "neutral")
        self.append_output(f"Overall Sentiment Score: {total_score}", "muted")
        self.append_output(f"Positivity Score: {positivity_score:.2f}%", "title")
        self.append_output("", "separator")

        # Display final message
        self.append_output("Sentiment analysis complete!", "title")
>>>>>>> f715db17172f8a51fe3fcbcc1e3593d1653be9f2
