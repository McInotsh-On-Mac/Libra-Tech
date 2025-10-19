import tkinter as tk
from tkinter import messagebox
from .fetch_tweets import fetch_tweets_for_ui

# Define Brand Colors (For a professional, branded look)
BRAND_DARK_BLUE = "#1A237E"
LIGHT_GRAY_BG = "#F0F0F0"

class SentimentAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Libra Technology: Sentiment Analysis")
        self.master.geometry("600x450")
        self.master.configure(bg=LIGHT_GRAY_BG)

        # Store fetched tweets in memory
        self.current_tweets = []
        self.current_keyword = ""

        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Main Title (Branded)
        tk.Label(self.frame, text="Libra Technology: Movie Sentiment Analysis Tool", 
                 font=("Helvetica", 16, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(pady=10)
        
        # --- keyword entry box ---
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), 
                 bg=LIGHT_GRAY_BG).pack(side=tk.LEFT, padx=5)
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # --- output text box with scrollbar ---
        text_frame = tk.Frame(self.frame)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Arial", 12), yscrollcommand=scrollbar.set)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        # --- buttons ---
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        btn_frame.pack(pady=10)

        # Fetch Tweets Button (Branded)
        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets, 
                                       font=("Arial", 12, "bold"), bg=BRAND_DARK_BLUE, fg="white", 
                                       activebackground="#2C3A8E", padx=10, pady=5)
        self.search_button.grid(row=0, column=0, padx=5)

        # Analyze Sentiment Button (Branded) - Initially disabled
        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis, 
                                        font=("Arial", 12, "bold"), bg="#666666", fg="white", 
                                        activebackground="#2C3A8E", padx=10, pady=5, state='disabled')
        self.analysis_button.grid(row=0, column=1, padx=5)
        
    def append_output(self, output):
        self.output_text.insert(tk.END, output + '\n')
        self.output_text.see(tk.END)
        print(output)
    
    def open_fetch_tweets(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a movie keyword.")
            return

        # Disable fetch button during operation
        self.search_button.config(state='disabled')
        self.analysis_button.config(state='disabled', bg="#666666")

        self.append_output(f"🔍 Fetching tweets for: {keyword} ...")
        
        try:
            result = fetch_tweets_for_ui(keyword, count=4)
            
            if result['success']:
                # Store tweets for analysis
                self.current_tweets = result['tweets']
                self.current_keyword = keyword
                
                self.append_output(f"✅ Successfully fetched {len(self.current_tweets)} tweets!")
                self.append_output("=" * 60)
                self.append_output("📝 FETCHED TWEETS:")
                
                for i, tweet in enumerate(self.current_tweets, 1):
                    self.append_output(f"{i}. {tweet}")
                    
                self.append_output("=" * 60)
                self.append_output("✅ Tweets ready for analysis!")
                
                # Enable analysis button
                self.analysis_button.config(state='normal', bg=BRAND_DARK_BLUE)
                
            else:
                self.append_output(f"❌ {result['message']}")
                self.current_tweets = []
                
        except Exception as e:
            self.append_output(f"❌ Error: {e}")
            self.current_tweets = []
        finally:
            # Re-enable fetch button
            self.search_button.config(state='normal')

    def open_sentiment_analysis(self):
        if not self.current_tweets:
            messagebox.showwarning("No Tweets", "Please fetch tweets first before analyzing sentiment.")
            return

        try:
            # Disable button during analysis
            self.analysis_button.config(state='disabled')
            
            self.append_output(f"🎬 Analyzing sentiment for {len(self.current_tweets)} tweets about '{self.current_keyword}'...")
            
            # Import sentiment analysis function
            from .analyze_sentiment import analyze_tweets_directly
            
            # Analyze the current tweets directly
            analysis_result = analyze_tweets_directly(self.current_tweets, self.current_keyword)
            
            if analysis_result['success']:
                self.append_output("=" * 60)
                self.append_output("📊 SENTIMENT ANALYSIS RESULTS")
                self.append_output("=" * 60)
                
                # Display summary
                if 'summary' in analysis_result:
                    self.append_output(analysis_result['summary'])
                
                # Ask if user wants detailed results
                if len(self.current_tweets) > 5:
                    show_details = messagebox.askyesno(
                        "Show Details", 
                        f"Analyzed {len(self.current_tweets)} tweets. Would you like to see detailed analysis for each tweet?\n\n(Click 'No' to see only the summary)"
                    )
                else:
                    show_details = True
                
                if show_details:
                    self.append_output("\n🔍 DETAILED ANALYSIS:")
                    self.append_output("=" * 40)
                    
                    for i, result in enumerate(analysis_result['detailed_results'], 1):
                        self.append_output(f"Tweet {i}: {result['sentiment']} (Score: {result['score']:.2f})")
                        self.append_output(f"   Text: {result['text']}")
                        if result.get('matched_words'):
                            self.append_output(f"   Key words: {', '.join(result['matched_words'])}")
                        self.append_output("")
                
                # Show final summary
                counts = analysis_result.get('sentiment_counts', {})
                self.append_output("=" * 60)
                self.append_output("🎯 FINAL SUMMARY:")
                self.append_output(f"   🎬 Movie: {self.current_keyword}")
                self.append_output(f"   📊 Total tweets analyzed: {len(self.current_tweets)}")
                self.append_output(f"   😊 Positive: {counts.get('Positive', 0)}")
                self.append_output(f"   😐 Neutral: {counts.get('Neutral', 0)}")
                self.append_output(f"   😞 Negative: {counts.get('Negative', 0)}")
                
                # Overall sentiment
                max_sentiment = max(counts.items(), key=lambda x: x[1]) if counts else ("Neutral", 0)
                self.append_output(f"   🎯 Overall sentiment: {max_sentiment[0]}")
                self.append_output("=" * 60)
                
            else:
                self.append_output(f"❌ Analysis failed: {analysis_result['message']}")
                
        except ImportError as ie:
            self.append_output(f"❌ Import error: {ie}")
            messagebox.showerror("Import Error", f"Could not import sentiment analysis: {ie}")
        except Exception as e:
            self.append_output(f"❌ Error during analysis: {e}")
            messagebox.showerror("Analysis Error", f"Failed to analyze sentiment: {e}")
        finally:
            # Re-enable button
            self.analysis_button.config(state='normal')