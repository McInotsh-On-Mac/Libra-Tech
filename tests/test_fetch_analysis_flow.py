# Anthony Powell
# - Implements placeholder behavior for the keyword Entry
# - append_output writes to a Text widget and prints to stdout
# - open_fetch_tweets validates input, calls fetch_tweets_for_ui, and stores tweets
# - open_sentiment_analysis warns when there are no tweets
try:
    import tkinter as tk  # real tkinter used when running the GUI
except Exception:
    tk = None  # tests will monkeypatch sentiment_app.tk

from tkinter import messagebox
from .fetch_tweets import fetch_tweets_for_ui

BRAND_DARK_BLUE = "#1A237E"
LIGHT_GRAY_BG = "#F0F0F0"
BTN_BG = "#304FFE"
BTN_BG_ACTIVE = "#1E40FF"
BTN_FG = "#000000"
ENTRY_BG = "#FFFFFF"
ENTRY_FG = "#000000"
ENTRY_PLACEHOLDER = "#8A8A8A"
SELECTION_BG = "#CCE0FF"
SELECTION_FG = "#000000"
CARET_COLOR = "#000000"


class SentimentAnalysisApp:
    def __init__(self, master):
        self.master = master
        # Window setup (safe if master is a simple object in tests)
        try:
            self.master.title("Libra Technology: Sentiment Analysis")
            self.master.geometry("800x600")
            self.master.configure(bg=LIGHT_GRAY_BG)
        except Exception:
            pass

        # Data
        self.current_tweets = []
        self.current_keyword = ""

        # UI widgets (tk will be patched in tests)
        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(
            self.frame,
            text="Libra Technology: Movie Sentiment Analysis Tool",
            font=("Helvetica", 18, "bold"),
            bg=LIGHT_GRAY_BG,
            fg=BRAND_DARK_BLUE,
        ).pack(pady=10)

        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg=LIGHT_GRAY_BG).pack(
            side=tk.LEFT, padx=5
        )

        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # Bind focus handlers where available
        try:
            self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)
            self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out)
        except Exception:
            # fake widgets in tests may accept bind but ignore; ignore failures otherwise
            pass

        # Set placeholder initially
        self._set_entry_placeholder()

        # Output area
        self.output_text = tk.Text(self.frame, wrap=tk.WORD, bg=ENTRY_BG, fg=ENTRY_FG)
        # configure scrollbar if desired (tests use fake Scrollbar)
        try:
            scrollbar = tk.Scrollbar(self.frame, orient=tk.Y, command=self.output_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.output_text.configure(yscrollcommand=scrollbar.set)
        except Exception:
            pass
        self.output_text.pack(expand=True, fill=tk.BOTH, pady=(10, 0))

    def _set_entry_placeholder(self):
        try:
            current = self.keyword_entry.get()
        except Exception:
            current = ""
        # If empty or None, insert placeholder
        if not current:
            try:
                self.keyword_entry.delete(0, tk.END)
            except Exception:
                pass
            try:
                self.keyword_entry.insert(0, self.placeholder_text)
            except Exception:
                # some fake Entry implementations expect different signatures
                try:
                    self.keyword_entry.insert("0", self.placeholder_text)
                except Exception:
                    pass

    def _on_entry_focus_in(self, _event=None):
        try:
            val = self.keyword_entry.get()
        except Exception:
            val = ""
        if val == self.placeholder_text:
            try:
                self.keyword_entry.delete(0, tk.END)
            except Exception:
                try:
                    self.keyword_entry.delete(0, "end")
                except Exception:
                    # fallback: set to empty via insert
                    try:
                        self.keyword_entry.insert(0, "")
                    except Exception:
                        pass

    def _on_entry_focus_out(self, _event=None):
        try:
            val = self.keyword_entry.get()
        except Exception:
            val = ""
        if not val:
            self._set_entry_placeholder()

    def append_output(self, output: str):
        # Write to the Text widget if available and also print to stdout for test capture
        try:
            self.output_text.insert(tk.END, str(output) + "\n")
            # ensure the text area scrolls to the end if yview exists
            try:
                self.output_text.see(tk.END)
            except Exception:
                pass
        except Exception:
            # If Text not available in test, ignore
            pass
        print(output)

    def open_fetch_tweets(self):
        # Read keyword, validate
        try:
            raw = self.keyword_entry.get()
        except Exception:
            raw = ""
        keyword = (raw or "").strip()
        if not keyword or keyword == self.placeholder_text:
            try:
                messagebox.showwarning("Input Error", "Please enter a keyword before fetching tweets.")
            except Exception:
                pass
            return

        # Call fetch_tweets_for_ui (tests may monkeypatch this)
        try:
            result = fetch_tweets_for_ui(keyword, count=4)
        except Exception as e:
            try:
                messagebox.showwarning("Fetch Error", f"Failed to fetch tweets: {e}")
            except Exception:
                pass
            return

        if not isinstance(result, dict) or not result.get("success"):
            try:
                messagebox.showwarning("Fetch Error", "Fetching tweets failed or returned no results.")
            except Exception:
                pass
            return

        tweets = result.get("tweets", [])
        # store and report
        self.current_tweets = tweets
        self.current_keyword = keyword
        self.append_output(f"Fetched {len(tweets)} tweets for '{keyword}'.")

    def open_sentiment_analysis(self):
        # Require tweets to be present
        if not self.current_tweets:
            try:
                messagebox.showwarning("No Tweets", "No tweets to analyze. Please fetch tweets first.")
            except Exception:
                pass
            return

        # Minimal placeholder analysis step
        count = len(self.current_tweets)
        self.append_output(f"Analyzing {count} tweets for '{self.current_keyword}'.")