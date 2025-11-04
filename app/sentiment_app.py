import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Notebook
import datetime  # for timestamps
import requests  # for api calls
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .sample_tweets import generate_sample_tweets  # Use sample tweets instead
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
ENTRY_FG         = "#000000"   # black typing
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

        # title
        tk.Label(
            self.frame,
            text="Libra Technology: Movie Sentiment Analysis Tool",
            font=("Helvetica", 18, "bold"),
            bg=LIGHT_GRAY_BG,
            fg=BRAND_DARK_BLUE
        ).pack(pady=10)

        # keyword row (label + entry)
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=5)
        tk.Label(
            keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg=LIGHT_GRAY_BG
        ).pack(side=tk.LEFT, padx=5)

        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # entry accessibility: colors, caret, selection
        self.keyword_entry.configure(
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=CARET_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG
        )
        # show placeholder initially
        self._set_entry_placeholder()
        # wire focus handlers for placeholder logic
        self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out)

        # output text area + scrollbar
        text_frame = tk.Frame(self.frame)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=12,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # make output box readable too
        self.output_text.configure(
            bg="#FFFFFF", fg="#111111",
            insertbackground=CARET_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG
        )

        # text tags for formatting and sentiment colors
        self.output_text.tag_configure("muted", foreground="#666666")
        self.output_text.tag_configure("pos", foreground="#1B5E20")
        self.output_text.tag_configure("neg", foreground="#E65100")
        self.output_text.tag_configure("title", font=("Arial", 12, "bold"))

        # buttons row
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        btn_frame.pack(pady=10)

        # high-contrast fetch button
        self.search_button = tk.Button(
            btn_frame,
            text="Fetch Tweets",
            command=self.open_fetch_tweets,
            font=("Arial", 12, "bold"),
            bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10, pady=5, highlightthickness=0
        )
        self.search_button.grid(row=0, column=0, padx=5)

        # high-contrast analyze button
        self.analysis_button = tk.Button(
            btn_frame,
            text="Analyze Sentiment",
            command=self.open_sentiment_analysis,
            font=("Arial", 12, "bold"),
            bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10, pady=5, highlightthickness=0
        )
        # start disabled until tweets fetched
        self.analysis_button.config(state=tk.DISABLED, bg="#BDBDBD")
        self.analysis_button.grid(row=0, column=1, padx=5)

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
        Add timestamped output to the UI text box.
        Supports optional text tag for color or style.
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        try:
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

    def open_fetch_tweets(self):
        """
        Fetch tweets based on the keyword entered by the user using fetch_tweets_for_ui.
        """
        kw = self.keyword_entry.get().strip()
        if not kw or (kw == self.placeholder_text and self.keyword_entry.cget("fg") == ENTRY_PLACEHOLDER):
            messagebox.showwarning("Input Error", "Please enter a movie keyword.")
            return

        # disable UI during fetch
        self.search_button.config(state=tk.DISABLED)
        self.analysis_button.config(state=tk.DISABLED, bg="#BDBDBD")

        self.append_output(f"🔍 Fetching tweets for: {kw} ...", "muted")

        try:
            result = generate_sample_tweets(kw, count=6)  # Use sample tweets instead

            if result.get("success"):
                self.current_tweets = result.get("tweets", [])
                self.current_keyword = kw

                self.append_output(f"Successfully fetched {len(self.current_tweets)} tweets!", "muted")
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                self.append_output("FETCHED TWEETS:", "title")

                for i, tweet in enumerate(self.current_tweets, 1):
                    # if tweet is a dict, try to extract text
                    if isinstance(tweet, dict):
                        text = tweet.get("text") or tweet.get("full_text") or str(tweet)
                    else:
                        text = str(tweet)
                    self.append_output(f"{i}. {text}")

                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                self.append_output("Tweets ready for analysis!", "muted")

                # enable analyze button
                self.analysis_button.config(state=tk.NORMAL, bg=BTN_BG)
                
                # Update charts with new data
                self.update_charts()
            else:
                self.append_output(f"{result.get('message', 'Failed to fetch tweets')}", "neg")
                self.current_tweets = []
        except Exception as e:
            self.append_output(f"Error fetching tweets: {e}", "neg")
            self.current_tweets = []
        finally:
            self.search_button.config(state=tk.NORMAL)

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
            self.analysis_button.config(state=tk.DISABLED, bg="#BDBDBD")
            self.append_output(f"🎬 Analyzing sentiment for {len(self.current_tweets)} tweets about '{self.current_keyword}'...", "muted")

            # import analyze_tweets
            from .analyze_sentiment import analyze_tweets

            # call analysis
            analysis_result = analyze_tweets(self.current_tweets, self.current_keyword)

            if analysis_result.get("success"):
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")
                self.append_output("📊 SENTIMENT ANALYSIS RESULTS", "title")
                self.output_text.insert(tk.END, "—" * 60 + "\n", "muted")

                # ask whether or notto show detailed results
                if len(self.current_tweets) > 5:
                    show_details = messagebox.askyesno(
                        "Show Details",
                        f"Analyzed {len(self.current_tweets)} tweets. Would you like to see detailed analysis for each tweet?\n\n(Click 'No' to see only the summary)"
                    )
                else:
                    show_details = True

                if show_details and analysis_result.get("detailed_results"):
                    self.append_output("\n🔍 DETAILED ANALYSIS:", "title")
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
            self.append_output(f"Error during analysis: {e}", "neg")
            messagebox.showerror("Analysis Error", f"Failed to analyze sentiment: {e}")
        finally:
            # re-enable analyze button
            self.analysis_button.config(state=tk.NORMAL, bg=BTN_BG)


# standard entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAnalysisApp(root)
    root.mainloop()