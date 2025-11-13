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

# brand + accessibility colors
BRAND_DARK_BLUE = "#1A237E"   # original brand blue (still used for title)
LIGHT_GRAY_BG   = "#F0F0F0"   # window bg

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
        # main frame
        self.frame = tk.Frame(self.analysis_tab, bg=LIGHT_GRAY_BG, padx=30, pady=20)  # Increased horizontal padding
        self.frame.pack(expand=True, fill=tk.BOTH)

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

        # placeholder and focus handlers
        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"
        self._set_entry_placeholder()
        self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out)

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
        """Append a timestamped message to the output text box and stdout.
        Optional tkinter text tag may be provided for coloring.
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        try:
            # prefix timestamp
            self.output_text.insert(tk.END, f"[{ts}] ", "muted")
            if tag:
                self.output_text.insert(tk.END, output + "\n", tag)
            else:
                self.output_text.insert(tk.END, output + "\n")
            self.output_text.see(tk.END)
        except Exception:
            # fall back to simple insert in case of tag issues
            self.output_text.insert(tk.END, output + "\n")
            self.output_text.see(tk.END)
        # also print to stdout for logs
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

        self.append_output(f"Fetching tweets for: {kw} ...", "muted")

        try:
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

                self.append_output(f"Successfully fetched {len(self.current_tweets)} tweets!", "muted")
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                self.append_output("FETCHED TWEETS:", "title")

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
        except Exception as e:
            self.append_output(f"Error fetching tweets: {e}", "neg")
            self.current_tweets = []
        finally:
            try:
                self.fetch_analyze_button.config(state=tk.NORMAL, bg=BTN_BG)
            except Exception:
                pass

    # (Jania) Sentiment analysis function
    def open_sentiment_analysis(self):
        """
        Analyze the currently fetched tweets using analyze_tweets.
        """
        if not self.current_tweets:
            messagebox.showwarning("No Tweets", "Please fetch tweets first before analyzing sentiment.")
            return

        try:
            # disable button during analysis
            try:
                self.fetch_analyze_button.config(state=tk.DISABLED, bg="#BDBDBD")
            except Exception:
                pass
            self.append_output(f"Analyzing sentiment for {len(self.current_tweets)} tweets about '{self.current_keyword}'...", "muted")

            # import analyze_tweets
            from .analyze_sentiment import analyze_tweets

            # call analysis
            analysis_result = analyze_tweets(self.current_tweets, self.current_keyword)

            if analysis_result.get("success"):
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                self.append_output("SENTIMENT ANALYSIS RESULTS", "title")
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")

                # Decide whether to show detailed results; avoid modal dialogs in this environment
                show_details = True if len(self.current_tweets) <= 5 else False

                if show_details and analysis_result.get("detailed_results"):
                    self.append_output("\nDETAILED ANALYSIS:", "title")
                    self.output_text.insert(tk.END, "—" * 40 + "\n", "muted")

                    for i, res in enumerate(analysis_result["detailed_results"], 1):
                        sentiment = res.get("sentiment", "Unknown")
                        score = res.get("score", 0.0)
                        text = res.get("text", "")
                        matched = res.get("matched_words", [])
                        tag = "pos" if sentiment.lower().startswith("pos") else "neg" if sentiment.lower().startswith("neg") else None
                        self.append_output(f"Tweet {i}: {sentiment} (Score: {score:.2f})", tag)
                        self.append_output(f"   Text: {text}")
                        if matched:
                            self.append_output(f"   Key words: {', '.join(matched)}")
                        self.append_output("")

                # style: color-coded and sentiment scale ---
                counts = analysis_result.get("sentiment_counts", {})
                # map common keys to pos/neg
                pos = counts.get("Positive", 0) + counts.get("positive", 0) + counts.get("Pos", 0)
                neg = counts.get("Negative", 0) + counts.get("negative", 0) + counts.get("Neg", 0)
                # fallback: if detailed_results exist, derive counts there
                if pos == 0 and neg == 0 and analysis_result.get("detailed_results"):
                    for d in analysis_result["detailed_results"]:
                        s = (d.get("sentiment") or "").lower()
                        if s.startswith("pos"):
                            pos += 1
                        elif s.startswith("neg"):
                            neg += 1

                total = max(1, pos + neg)
                score = round((pos - neg) / total, 2)

                # header
                self.output_text.insert(tk.END, "\n", ())
                self.output_text.insert(tk.END, "Analysis Summary:\n", "title")
                self.output_text.insert(tk.END, "—" * 16 + "\n", "muted")

                # numbers + verdict (color coded)
                verdict = "Overall Positive" if score > 0 else "Overall Negative" if score < 0 else "mixed/neutral"
                verdict_tag = "pos" if score >= 0 else "neg"
                self.append_output(f"Positives={pos}, Negatives={neg}, Score={score}", verdict_tag)

                # ascii/visual bar
                bar_len = 24
                pos_blocks = int((pos / total) * bar_len) if total > 0 else 0
                pos_blocks = max(0, min(bar_len, pos_blocks))
                bar = f"[{'▮' * pos_blocks}{'▯' * (bar_len - pos_blocks)}]  {int((pos/total)*100)}% positive"
                self.append_output(bar, "muted")

                # verdict line color-coded
                self.append_output(verdict, verdict_tag)

                # end separator
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                
                # Update charts after analysis
                self.update_charts()
            else:
                self.append_output(f"Analysis failed: {analysis_result.get('message', 'Unknown error')}", "neg")
        except ImportError as ie:
            self.append_output(f"Import error: {ie}", "neg")
            messagebox.showerror("Import Error", f"Could not import sentiment analysis: {ie}")
        except Exception as e:
            self.append_output(f"Error during analysis or display: {e}", "neg") # Log error during analysis/display.
            messagebox.showerror("Analysis Error", f"Failed to analyze or display sentiment: {e}") # Show pop-up error.
            
        finally:
            # Re-enable combined button and restore color.
            try:
                self.fetch_analyze_button.config(state=tk.NORMAL, bg=BTN_BG)
            except Exception:
                pass
            self.append_output("\n--- PROCESS COMPLETE ---", "title")