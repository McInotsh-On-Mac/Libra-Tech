
import tkinter as tk # Imports the main library for creating graphical windows.
from tkinter import messagebox # Imports a tool for simple alert messages.

# Define Brand Colors (For a professional, branded look)
BRAND_DARK_BLUE = "#1A237E" # Primary color for buttons and titles.
LIGHT_GRAY_BG = "#F0F0F0" # Standard background color.

class SentimentAnalysisApp: # Defines the blueprint for the main application window.
    # TODO(Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page. # Note for the developer team.
    def __init__(self, master): # This function runs when the main app window is created.
        self.master = master
        self.master.title("Libra Technology: Sentiment Analysis") # Sets the window title.
        self.master.geometry("600x450") # Sets the starting size of the window.
        self.master.configure(bg=LIGHT_GRAY_BG) # Sets the entire window's background color.

        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20) # Creates a container frame for the elements.
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Main Title (Branded)
        tk.Label(self.frame, text="Libra Technology: Movie Sentiment Analysis Tool", 
                 font=("Helvetica", 16, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(pady=10) # Displays the branded title.
        
        # --- keyword entry box ---
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG) # Frame to hold the input area.
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), 
                 bg=LIGHT_GRAY_BG).pack(side=tk.LEFT, padx=5) # Label prompting for the movie keyword.
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30) # The text box for the user to type in.
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # --- output text box with scrollbar ---
        text_frame = tk.Frame(self.frame) # Frame to hold the large text display area.
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame) # Vertical scroll bar for long text output.
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Arial", 12), yscrollcommand=scrollbar.set) # The main output box for messages and results.
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview) # Connects the scrollbar to the text box.
        
        # --- buttons ---
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG) # Frame to hold the action buttons.
        btn_frame.pack(pady=10)

        # Fetch Tweets Button (Branded)
        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets, 
                                       font=("Arial", 12, "bold"), bg=BRAND_DARK_BLUE, fg="white", 
                                       activebackground="#2C3A8E", padx=10, pady=5) # Button to start data fetching.
        self.search_button.grid(row=0, column=0, padx=5)

        # Analyze Sentiment Button (Branded)
        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis, 
                                        font=("Arial", 12, "bold"), bg=BRAND_DARK_BLUE, fg="white", 
                                        activebackground="#2C3A8E", padx=10, pady=5) # Button to start data analysis.
        self.analysis_button.grid(row=0, column=1, padx=5)
        
    
    def append_output(self, output): # Function to add status or result text to the output box.
        # TODO(Ayinde): Make sure output is user-friendly and clear. # Note for the developer team.
        self.output_text.insert(tk.END, output + '\n') # Adds the text to the end of the output box.
        self.output_text.see(tk.END) # Scrolls the output box down to show the newest text.
        print(output) # Also prints the text to the developer's console.
    
    # ... (open_fetch_tweets and open_sentiment_analysis methods remain as stubs)
    
    def open_fetch_tweets(self): # Function for when the "Fetch Tweets" button is clicked.
        keyword = self.keyword_entry.get().strip()

        if not keyword:
            messagebox.showwarning("Input Required", "Please enter a keyword to search for tweets.")
            return
        
        try:
            # Disable button during fetch to prevent multiple clicks
            self.search_button.config(state='disabled')
            self.append_output(f"Fetching tweets for keyword: '{keyword}'...")
            
            # Import and call the UI-friendly fetch function
            from .fetch_tweets import fetch_tweets_for_ui
            
            # Call the fetch function and get results
            result = fetch_tweets_for_ui(keyword, count=10)
            
            # Display results based on success/failure
            if result['success']:
                self.append_output(result['message'])
                self.append_output("-" * 50)
                
                # Display each tweet with numbering
                for i, tweet in enumerate(result['tweets'], 1):
                    self.append_output(f"{i}. {tweet}")
                    self.append_output("")  # Add empty line for readability
                    
                self.append_output("-" * 50)
                self.append_output(f"Total tweets fetched: {result['count']}")
            else:
                self.append_output(result['message'])
                
        except ImportError as ie:
            error_msg = f"Import error: {str(ie)}"
            self.append_output(error_msg)
            messagebox.showerror("Import Error", error_msg)
        except Exception as e:
            error_msg = f"Error fetching tweets: {str(e)}"
            self.append_output(error_msg)
            messagebox.showerror("Error", f"Failed to fetch tweets: {str(e)}")
        finally:
            # Re-enable button after operation completes
            self.search_button.config(state='normal')

    def open_sentiment_analysis(self): # Placeholder function for when the "Analyze Sentiment" button is clicked.
        # TODO(Ben): (Sentiment Analysis Logic): Implement logic to analyze sentiment and store/retrieve results in DB. # Note for the developer team.
        # TODO(Testing Point-Anthony): (UI Integration): Ensure UI displays results from analysis. # Note for the developer team.
        pass # Currently does nothing until the analysis script is fully linked.