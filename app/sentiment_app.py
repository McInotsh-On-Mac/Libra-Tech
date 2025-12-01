import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkinter.ttk import Notebook
import datetime  # for timestamps
import requests  # for api calls
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .sample_tweets import generate_sample_tweets  # Use sample tweets instead
from .fetch_tweets import fetch_tweets_for_ui  # Real API fetcher
from .chart_sentiment import create_sentiment_charts
from .analyze_sentiment import analyze_sentiment  # Import analyze_sentiment function

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

        # store last generated charts (window -> matplotlib.Figure)
        self.last_charts = {}

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
        # Create main container for charts tab
        self.charts_frame = tk.Frame(self.charts_tab, bg=LIGHT_GRAY_BG)
        self.charts_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Create button container FIRST at the bottom
        btn_container = tk.Frame(self.charts_frame, bg=LIGHT_GRAY_BG)
        btn_container.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Save Current Chart button
        self.save_current_btn = tk.Button(
            btn_container,
            text="Download Current Chart",
            command=self.save_current_chart,
            font=("Arial", 14, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            activeforeground=BTN_FG,
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3
        )
        self.save_current_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        # Save All Charts button
        self.save_all_btn = tk.Button(
            btn_container,
            text="Download All Charts",
            command=self.save_all_charts,
            font=("Arial", 14, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            activeforeground=BTN_FG,
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3
        )
        self.save_all_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        # Download Data button
        self.download_data_btn = tk.Button(
            btn_container,
            text="Download Chart Data (CSV)",
            command=self.download_chart_data,
            font=("Arial", 14, "bold"),
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE,
            activeforeground=BTN_FG,
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3
        )
        self.download_data_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # Create notebook for different time windows AFTER buttons
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
                self.output_text.insert(tk.END, f"{output}\n", tag)  # Add a green checkmark for positive
            elif tag == 'neg':
                self.output_text.insert(tk.END, f"{output}\n", tag)  # Add a red cross for negative
            elif tag == 'neutral':
                self.output_text.insert(tk.END, f"{output}\n", tag)  # Add a white circle for neutral
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
            # Store charts and canvases for saving
            self.last_charts = charts
            self.chart_canvases = {}
            
            # Add charts to their respective frames
            for window, chart in charts.items():
                canvas = FigureCanvasTkAgg(chart, master=self.chart_frames[window])
                canvas.draw()
                canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
                # Store canvas reference
                self.chart_canvases[window] = canvas
                
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

    def _get_selected_window_key(self):
        """Return the window key (e.g., '24h') for the currently selected charts tab."""
        try:
            tab_id = self.charts_notebook.select()
            tab_text = self.charts_notebook.tab(tab_id, "text")
            # tab_text is like 'Last 24h'
            if tab_text.lower().startswith('last'):
                return tab_text.split()[-1]
            return tab_text
        except Exception:
            return '24h'

    # Elali McNair
    def save_current_chart(self):
        """Download the currently selected chart to the Downloads folder."""
        if not getattr(self, 'last_charts', None):
            messagebox.showwarning("No Chart", "No chart available to download. Generate charts first.")
            return

        key = self._get_selected_window_key()
        canvas = getattr(self, 'chart_canvases', {}).get(key)
        
        if canvas is None:
            messagebox.showwarning("No Chart", f"No chart available for the selected tab ({key}).")
            return

        try:
            import gc
            from PIL import ImageGrab
            
            # Get Downloads folder path
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            filename = f"sentiment_{key}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(downloads_folder, filename)
            
            # Get the canvas widget
            widget = canvas.get_tk_widget()
            
            # Force update to ensure widget is fully rendered
            widget.update()
            
            # Get widget position and size
            x = widget.winfo_rootx()
            y = widget.winfo_rooty()
            width = widget.winfo_width()
            height = widget.winfo_height()
            
            img = None
            try:
                # Capture the widget area
                img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                img.save(path, 'PNG')
            finally:
                # Always close the image and force garbage collection
                if img:
                    img.close()
                gc.collect()
            
            # Defer the success message to avoid GUI conflicts
            self.master.after(100, lambda: messagebox.showinfo("Downloaded", f"Chart downloaded to:\n{path}"))
            print(f"Downloaded: {path}")
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"Error downloading chart:\n{error_detail}")
            self.master.after(100, lambda e=e: messagebox.showerror("Download Error", f"Failed to download chart:\n{str(e)}"))
    
    # Elali McNair
    def save_all_charts(self):
        """Download all generated charts to the Downloads folder as PNG files."""
        if not getattr(self, 'chart_canvases', None) or not self.chart_canvases:
            messagebox.showwarning("No Charts", "No charts available to download. Please generate charts first by clicking 'Fetch & Analyze'.")
            return

        # Start the download process with a queue
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        self._download_queue = list(self.chart_canvases.items())
        self._download_results = {'saved': 0, 'failures': [], 'folder': downloads_folder, 'timestamp': timestamp}
        
        # Start downloading the first chart
        self._download_next_chart()
    
    # Elali McNair
    def _download_next_chart(self):
        """Helper function to download charts one at a time with delays."""
        if not self._download_queue:
            # All done, show results
            self._show_download_results()
            return
        
        key, canvas = self._download_queue.pop(0)
        
        try:
            import gc
            from PIL import ImageGrab
            
            filename = f"sentiment_{key}_{self._download_results['timestamp']}.png"
            path = os.path.join(self._download_results['folder'], filename)
            
            # Get the canvas widget
            widget = canvas.get_tk_widget()
            
            # Switch to the tab to make it visible for capture
            for i, frame_key in enumerate(self.chart_frames.keys()):
                if frame_key == key:
                    self.charts_notebook.select(i)
                    break
            
            # Force update to ensure widget is fully rendered
            widget.update()
            self.master.update()
            
            # Get widget position and size
            x = widget.winfo_rootx()
            y = widget.winfo_rooty()
            width = widget.winfo_width()
            height = widget.winfo_height()
            
            img = None
            try:
                # Capture the widget area
                img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                img.save(path, 'PNG')
            finally:
                # Always close the image and force garbage collection
                if img:
                    img.close()
                gc.collect()
            
            self._download_results['saved'] += 1
            print(f"Downloaded: {path}")
        except Exception as e:
            print(f"Failed to download {key}: {e}")
            import traceback
            traceback.print_exc()
            self._download_results['failures'].append((key, str(e)))
        
        # Schedule next download after a delay to avoid overwhelming the GUI
        self.master.after(300, self._download_next_chart)
    
    # Elali McNair
    def _show_download_results(self):
        """Show the final results of downloading all charts."""
        results = self._download_results
        if results['failures']:
            msg = f"Downloaded {results['saved']} chart(s) to Downloads folder.\nFailed: {', '.join([f[0] for f in results['failures']])}"
            messagebox.showwarning("Partial Success", msg)
        else:
            messagebox.showinfo("Downloaded", f"All {results['saved']} charts downloaded successfully to:\n{results['folder']}")
    
    # Elali McNair
    def download_chart_data(self):
        """Download raw chart data as CSV files to the Downloads folder."""
        try:
            import csv
            from .chart_sentiment import fetch_sentiment_data_from_db
            
            # Fetch the data from database
            data = fetch_sentiment_data_from_db(60)
            
            if data.empty:
                messagebox.showwarning("No Data", "No sentiment data available to download. Please fetch and analyze tweets first.")
                return
            
            # Get Downloads folder path
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"sentiment_data_{timestamp}.csv"
            path = os.path.join(downloads_folder, filename)
            
            # Calculate net sentiment for the export
            data['net_sentiment'] = data['positive_count'] - data['negative_count']
            
            # Select and order columns for export
            export_columns = ['timestamp', 'sentiment', 'tweet_count', 'positive_count', 
                            'negative_count', 'neutral_count', 'net_sentiment']
            export_data = data[export_columns]
            
            # Write to CSV
            export_data.to_csv(path, index=False)
            
            # Defer the success message to avoid GUI conflicts
            self.master.after(100, lambda: messagebox.showinfo("Downloaded", f"Chart data downloaded to:\n{path}\n\nRows: {len(export_data)}"))
            print(f"Downloaded data: {path} ({len(export_data)} rows)")
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"Error downloading chart data:\n{error_detail}")
            messagebox.showerror("Download Error", f"Failed to download chart data:\n{str(e)}")

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