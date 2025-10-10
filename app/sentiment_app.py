import tkinter as tk
from tkinter import messagebox
from .db import get_db_connection


class SentimentAnalysisApp:
    # TODO(Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page.
    def __init__(self, master):
        self.master = master
        self.master.title("Tweetables: Sentiment Analysis")
        self.master.geometry("600x450")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Tweetables: Movie Sentiment Analysis Tool", font=("Helvetica", 16, "bold"), bg="#ADD8E6").pack(pady=10)
        
        # --- keyword entry box ---
        keyword_frame = tk.Frame(self.frame, bg="#ADD8E6")
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
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
        btn_frame = tk.Frame(self.frame, bg="#ADD8E6")
        btn_frame.pack(pady=10)
        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.search_button.grid(row=0, column=0, padx=5)
        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.analysis_button.grid(row=0, column=1, padx=5)
    
def append_output(self, output):
        # TODO(Ayinde): Make sure output is user-friendly and clear.
        self.output_text.insert(tk.END, output + '\n')
        self.output_text.see(tk.END)
        print(output)

def open_fetch_tweets(self):
    # TODO(Ben): (Backend Tweets/Sentiment API): Implement fetching tweets from DB/API and displaying in UI.
    pass

def open_sentiment_analysis(self):
    # TODO(Ben): (Sentiment Analysis Logic): Implement logic to analyze sentiment and store/retrieve results in DB.
    # TODO(Testing Point-Anthony): (UI Integration): Ensure UI displays results from analysis.
    pass