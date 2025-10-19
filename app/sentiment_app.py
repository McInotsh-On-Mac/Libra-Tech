<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
import datetime  # For timestamps
import requests  # For API calls
from .fetch_tweets import fetch_tweets_for_ui
=======

import tkinter as tk # Imports the main library for creating graphical windows.
from tkinter import messagebox # Imports a tool for simple alert messages.
from .fetch_tweets import fetch_tweets_for_ui

>>>>>>> b2a9e4a631c046e5b7822d6a9580239fbc7eddbe

# Define Brand Colors (For a professional, branded look)
BRAND_DARK_BLUE = "#1A237E"  # Original brand blue (still used for title)
LIGHT_GRAY_BG = "#F0F0F0"  # Standard background color

# New high-contrast UI tokens
BTN_BG = "#304FFE"  # Bright blue button
BTN_BG_ACTIVE = "#1E40FF"  # Darker on press
BTN_FG = "#000000"  # Black text for readability
BTN_FG_DISABLED = "#333333"  # Dim black when disabled
ENTRY_BG = "#FFFFFF"  # White input background
ENTRY_FG = "#000000"  # Black typing
ENTRY_PLACEHOLDER = "#8A8A8A"  # Gray placeholder
SELECTION_BG = "#CCE0FF"
SELECTION_FG = "#000000"
CARET_COLOR = "#000000"


class SentimentAnalysisApp:
    # TODO(Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page.
    def __init__(self, master):
        # Window setup
        self.master = master
        self.master.title("Libra Technology: Sentiment Analysis")
        self.master.geometry("800x600")  # Increased size for better accessibility
        self.master.configure(bg=LIGHT_GRAY_BG)

        # Main frame
        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Title
        tk.Label(
            self.frame,
            text="Libra Technology: Movie Sentiment Analysis Tool",
            font=("Helvetica", 18, "bold"),
            bg=LIGHT_GRAY_BG,
            fg=BRAND_DARK_BLUE,
        ).pack(pady=10)

        # Keyword entry box
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=10)
        tk.Label(
            keyword_frame,
            text="Enter Movie Keyword:",
            font=("Arial", 14),
            bg=LIGHT_GRAY_BG,
            fg=BRAND_DARK_BLUE,
        ).pack(side=tk.LEFT, padx=5)
        self.keyword_entry = tk.Entry(
            keyword_frame,
            font=("Arial", 14),
            width=30,
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=CARET_COLOR,
        )
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # Output text box with scrollbar
        text_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=15,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set,
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG,
            insertbackground=CARET_COLOR,
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Buttons
        button_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        button_frame.pack(pady=10)
        self.fetch_button = tk.Button(
            button_frame,
            text="Fetch Tweets",
            command=self.open_fetch_tweets,
            font=("Arial", 14, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            padx=20,
            pady=10,
        )
        self.fetch_button.pack(side=tk.LEFT, padx=10)
        self.analyze_button = tk.Button(
            button_frame,
            text="Analyze Sentiment",
            command=self.open_sentiment_analysis,
            font=("Arial", 14, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            padx=20,
            pady=10,
        )
        self.analyze_button.pack(side=tk.LEFT, padx=10)

    def append_output(self, output):
        """
        Function to add status or result text to the output box.
        """
        self.output_text.insert(tk.END, output + "\n")
        self.output_text.see(tk.END)
        print(output)  # Also prints the text to the developer's console

    def open_fetch_tweets(self):
        """
        Fetch tweets based on the keyword entered by the user.
        """
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a movie keyword.")
            return

        self.append_output(f"Fetching tweets for: {keyword} ...")
        try:
            result = fetch_tweets_for_ui(keyword, count=10)
            if result["success"]:
                self.append_output("Fetched Tweets:")
                for tweet in result["tweets"]:
                    self.append_output(tweet)
            else:
                self.append_output(result["message"])
        except Exception as e:
            self.append_output(f"Error: {e}")

    def open_sentiment_analysis(self):
        """
        Placeholder function for analyzing sentiment.
        """
        self.append_output("Analyzing sentiment... (Functionality not yet implemented)")