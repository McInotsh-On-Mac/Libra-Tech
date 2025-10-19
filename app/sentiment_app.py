import tkinter as tk
from tkinter import messagebox
import datetime  # For timestamps
import requests  # For API calls
from .fetch_tweets import fetch_tweets_for_ui

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

        # Keyword entry box with placeholder
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=5)
        tk.Label(
            keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg=LIGHT_GRAY_BG
        ).pack(side=tk.LEFT, padx=5)

        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # Entry accessibility: colors, caret, selection
        self.keyword_entry.configure(
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=CARET_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG,
        )
        # Show placeholder initially
        self._set_entry_placeholder()
        # Wire focus handlers for placeholder logic
        self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out)

        # Output text area with scrollbar
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
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Make output box readable too
        self.output_text.configure(
            bg="#FFFFFF",
            fg="#111111",
            insertbackground=CARET_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG,
        )

        # Text tags for formatting and sentiment colors
        self.output_text.tag_configure("muted", foreground="#666666")
        self.output_text.tag_configure("pos", foreground="#1B5E20")
        self.output_text.tag_configure("neg", foreground="#E65100")
        self.output_text.tag_configure("title", font=("Arial", 12, "bold"))

        # Buttons row
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        btn_frame.pack(pady=10)

        # High-contrast fetch button
        self.search_button = tk.Button(
            btn_frame,
            text="Fetch Tweets",
            command=self.open_fetch_tweets,
            font=("Arial", 12, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10,
            pady=5,
            highlightthickness=0,
        )
        self.search_button.grid(row=0, column=0, padx=5)

        # High-contrast analyze button
        self.analysis_button = tk.Button(
            btn_frame,
            text="Analyze Sentiment",
            command=self.open_sentiment_analysis,
            font=("Arial", 12, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10,
            pady=5,
            highlightthickness=0,
        )
        self.analysis_button.grid(row=0, column=1, padx=5)

        # Keep tweets + quick sentiment tags
        self._tweets = []

    def _set_entry_placeholder(self):
        # Put placeholder text and set gray color
        self.keyword_entry.delete(0, tk.END)
        self.keyword_entry.insert(0, self.placeholder_text)
        self.keyword_entry.config(fg=ENTRY_PLACEHOLDER)

    def _on_entry_focus_in(self, _event=None):
        # When focusing, if placeholder shown, clear and set black typing color
        if self.keyword_entry.get() == self.placeholder_text and self.keyword_entry.cget("fg") == ENTRY_PLACEHOLDER:
            self.keyword_entry.delete(0, tk.END)
            self.keyword_entry.config(fg=ENTRY_FG)

    def _on_entry_focus_out(self, _event=None):
        # When leaving, if empty, restore placeholder
        if not self.keyword_entry.get().strip():
            self._set_entry_placeholder()

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
        if not keyword or keyword == self.placeholder_text:
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