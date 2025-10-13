import tkinter as tk
from login_screen import LoginScreen 
# You will likely need to import the SentimentAnalysisApp here as well, 
# but for now, we only need the LoginScreen to start.

if __name__ == "__main__":
    # Create the main window instance provided by Tkinter
    root = tk.Tk()
    
    # Initialize the LoginScreen, which starts the application
    app = LoginScreen(root)
    
    # Start the Tkinter event loop, which keeps the window open and responsive
    root.mainloop()