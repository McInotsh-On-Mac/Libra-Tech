import tkinter as tk # Imports the main library for creating graphical windows (GUI).
import threading # Imports a tool to run slow tasks (like fetching data) in the background so the window doesn't freeze.
import subprocess # Imports a tool to run other Python scripts or programs from within this one.
import os # Imports a tool to interact with the computer's operating system (like file paths).
import sys # Imports a tool to access system-specific settings and parameters.
import tkinter.messagebox # Imports a tool to display simple pop-up alert messages.


class LoginScreen: # Defines the blueprint for creating the initial Login window.
    # The __init__ function is what runs automatically when a LoginScreen object is created.
    def __init__(self, master):
        self.master = master # 'master' is the main window provided by tkinter.
        self.master.title("Login") # Sets the title text that appears at the top of the window.
        self.master.geometry("400x350") # Sets the starting size of the window to 400 pixels wide by 350 pixels tall.
        self.master.configure(bg="#F0F0F0") #Background color is light gray instead of light blue
        
        # Define the brand colors based on the Libra-Tech logo for consistent design.
        BRAND_DARK_BLUE = "#1A237E" # This dark blue color is used for primary text and buttons.
        BRAND_TEAL_ACCENT = "#008B8B" # This teal/green color is used for accents.

        # Create a large title label for the application name.
        tk.Label(master, text="LIBRA TECHNOLOGIES", font=("Segoe UI", 18, "bold"), bg="#F0F0F0", fg=BRAND_DARK_BLUE).pack(pady=(20, 5)) # Place it at the top with branding colors.
        # Create a subtitle label to describe the current screen.
        tk.Label(master, text="Secure Login", font=("Segoe UI", 12), bg="#F0F0F0", fg=BRAND_TEAL_ACCENT).pack(pady=(0, 15)) # Place it below the main title.

        # Create a container (frame) to hold the username and password fields.
        self.frame = tk.Frame(master, bg="#F0F0F0", padx=30, pady=30)
        self.frame.pack(expand=True)

        # Username Input
        # Label that says "Username: "
        tk.Label(self.frame, text="Username:", font=("Segoe UI", 11), bg="#F0F0F0").grid(row=0, column=0, sticky="w", pady=5)   
        # The box where the user types their username.
        self.username_entry = tk.Entry(self.frame, font=("Segoe UI", 12), width =25, relief=tk.FLAT, bd=2)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        # Password Input
        # Label that says "Password: "
        tk.Label(self.frame, text="Password:", font=("Segoe UI", 11), bg="#F0F0F0").grid(row=1, column=0, sticky="w", pady=5)
        # The box where the user types their Password using show="*" to hide characters.
        self.password_entry = tk.Entry(self.frame, font=("Segoe UI", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        # A label for showing error messages or success status.
        # Background color is updated to match the new light gray scheme.
        self.message_label = tk.Label(self.frame, text="", fg="red", bg="#F0F0F0", font=("Arial", 10))
        self.message_label.grid(row=2, columnspan=2, pady=5) # Spans both columns beneath the inputs.

        #Login Button
        self.login_button = tk.Button(self.frame, text="Login", command=self.validate_login, font=("Segoe UI", 12), bg=BRAND_DARK_BLUE, fg="white", activebackground="#2C3A8E", padx=20, pady=5, relief=tk.FLAT) # Calls validate_login when clicked styled with brand color and white text.
        self.login_button.grid(row=3, columnspan=2, pady=(20,10))

        #Sign Up Button
        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup, font=("Segoe UI", 12), bg="#CCCCCC", fg="black", activebackground="#BBBBBB", padx=20, pady=5, relief=tk.FLAT)
        self.signup_button.grid(row=4, columnspan=2, pady=5)

    # This function runs when the user clicks the "Log In" button.
    def validate_login(self):
        username = self.username_entry.get().strip() # Gets the text from the username box and removes any extra spaces.
        password = self.password_entry.get().strip() # Gets the text from the password box and removes any extra spaces.

        # 1. Clear previous messages
        self.message_label.config(text="") # Clears any old error messages from the screen.

         # 2. Check for empty fields
        if not username or not password: # Checks if either the username or password box is empty.
            self.message_label.config(text="Username and/or Password cannot be empty.", fg="red") # Shows a required error message.
            self.password_entry.delete(0, tk.END) # Clears the password box for security.
            return # Stops the login process.
        
        # 3. Check for minimum password length (minimum 8 characters is standard)
        if len(password) < 8: # Checks if the password has less than 8 characters.
            self.message_label.config(text="Password must be at least 8 characters long.", fg="red") # Shows an error if it's too short.
            self.password_entry.delete(0, tk.END) # Clears the password box.
            return # Stops the login process.

        # 4. Connect to Backend API (Simulated)
        # This line calls the new function that simulates talking to the server's authentication API.
        if self.simulate_backend_login(username, password):
            self.message_label.config(text="Login successful!", fg="green") # Shows success message.
            self.open_sentiment_analysis() # If successful, opens the main application screen.
        else:
            # This runs if the simulated API call fails (invalid credentials).
            self.message_label.config(text="Invalid credentials. Please try again.", fg="red") # Shows a generic failure message.
            # Only clears the password entry for better user experience.
            self.password_entry.delete(0, tk.END)

    # This new method replaces the old file-based check (Goal 3: Connect to new API).
    def simulate_backend_login(self, username, password):
        # Define the credentials the new server API expects to accept.
        MOCK_SUCCESS_USER = "apitester"
        MOCK_SUCCESS_PASS = "StrongPass8"
        # Checks if the entered credentials match the mock successful credentials.
        if username == MOCK_SUCCESS_USER and password == MOCK_SUCCESS_PASS:
            # If they match, a successful login response from the server is simulated.
            return True
        # 2. Fallback: Check local users.txt file for signed-up users (Legacy Check)
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    # Strip any extra whitespace from the line and split by comma
                    stored_user, stored_password = line.strip().split(",", 1)
                    
                    # Check if the entered credentials match a stored account
                    if stored_user.strip() == username and stored_password.strip() == password:
                        return True # Successful local file login
        except FileNotFoundError:
            # If the file doesn't exist, nobody can log in except the mock user.
            pass

        # 3. If neither check succeeds
        return False

    # This function handles opening the separate Sign Up window.
    def open_signup(self):
        signup_window = tk.Toplevel(self.master) # Creates a new window on top of the main one.
        signup_window.title("Sign Up") # Sets the window title.
        signup_window.geometry("350x200")
        signup_window.configure(bg="#F0F0F0") # Use the light gray background color for the Sign Up window.

        #Styles the button
        BRAND_DARK_BLUE = "#1A237E"
        
        frame = tk.Frame(signup_window, bg="#F0F0F0", padx=20, pady=20) # Creates a frame container inside the new window.
        frame.pack(expand=True)

         # Labels and input boxes for the new user's credentials.
        tk.Label(frame, text="New Username:", font=("Arial", 12), bg="#F0F0F0").grid(row=0, column=0, sticky="w", pady=5)
        new_username = tk.Entry(frame, font=("Arial", 12))
        new_username.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="New Password:", font=("Arial", 12), bg="#F0F0F0").grid(row=1, column=0, sticky="w", pady=5)
        new_password = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password.grid(row=1, column=1, pady=5, padx=10)

        def save_credentials():
            username = new_username.get().strip()
            password = new_password.get().strip()
            
            if not username or not password: # Stops if fields are empty.
                tk.messagebox.showerror("Error", "All fields are required.")
                return 
            
            # Check password length (Must match login screen security)
            if len(password) < 8:
                tk.messagebox.showerror("Error", "Password must be at least 8 characters long.")
                return
            
            try:
                # Opens the users file to check if the username already exists.
                with open("users.txt", "r") as file:
                    for line in file:
                        stored_user, _ = line.strip().split(",")
                        if stored_user == username:
                            tk.messagebox.showerror("Error", "Username already exists.")
                            return
                        
            except FileNotFoundError:
                pass
                # Saves the new user's details to the 'users.txt' file.
                with open("users.txt", "a") as file:
                    file.write(f"{username},{password}\n")
                tk.messagebox.showinfo("Success", "Account created successfully!")
                signup_window.destroy() # Closes the sign-up window after saving.

        signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg=BRAND_DARK_BLUE, fg="white", padx=10, pady=5)
        signup_button.grid(row=2, columnspan=2, pady=10)

    # Function that runs after successful login.
    def open_sentiment_analysis(self):
        self.master.destroy() # Closes the current login window.
        root = tk.Tk() # Creates a new main window for the application.
        app = SentimentAnalysisApp(root) # Initializes the main application screen.
        root.mainloop() # Starts the main application loop.

# Defines the blueprint for the main application (where the user analyzes tweets).
class SentimentAnalysisApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Libra Technology: Sentiment Analysis")
        self.master.geometry("600x450")
        self.master.configure(bg="#F0F0F0")

        self.frame = tk.Frame(master, bg="#F0F0F0", padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Libra Technology: Movie Sentiment Analysis Tool", font=("Helvetica", 16, "bold"), bg="#F0F0F0").pack(pady=10)
        
        # --- keyword entry box ---
        keyword_frame = tk.Frame(self.frame, bg="#F0F0F0")
        keyword_frame.pack(pady=5)
        tk.Label(keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg="#F0F0F0").pack(side=tk.LEFT, padx=5)
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
        btn_frame = tk.Frame(self.frame, bg="#F0F0F0")
        btn_frame.pack(pady=10)
        self.search_button = tk.Button(btn_frame, text="Fetch Tweets", command=self.open_fetch_tweets, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.search_button.grid(row=0, column=0, padx=5)
        self.analysis_button = tk.Button(btn_frame, text="Analyze Sentiment", command=self.open_sentiment_analysis, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.analysis_button.grid(row=0, column=1, padx=5)
    
    # Function to add text to the output box and print it to the console.
    def append_output(self, output):
        self.output_text.insert(tk.END, output + '\n') # Puts the text into the output box.
        self.output_text.see(tk.END) # Automatically scrolls the box to the bottom to see new text.
        print(output) # Also prints the output to the terminal where the script is running.

    # Function to start the tweet fetching process in a new thread (to prevent the GUI from freezing).
    def open_fetch_tweets(self):
        threading.Thread(target=self.run_fetch_tweets).start()
    # Function that manages the thread for running the external tweet fetching script.
    def run_fetch_tweets(self):

        def fetch(): # The actual work done in the background thread.
            keyword = self.keyword_entry.get() # get the keyword entered by the user
            # Use 'after(0, ...)' to safely update the GUI with a status message.
            self.master.after(0, self.append_output, "Fetching tweets for sentiment analysis...")
            # Builds the full path to the 'fetch_tweets.py' script.
            script_path = os.path.join(os.path.dirname(__file__), "fetch_tweets.py")
            try:
                #pass the keyword as an argument to the script
                process = subprocess.Popen(
                    [sys.executable, script_path, keyword], #pass keyword here 
                    stdout=subprocess.PIPE, # Captures the normal output of the script.
                    stderr=subprocess.PIPE, # Captures any error messages from the script.
                    text=True # Ensures the output is handled as human-readable text.
                )

                #read output line by line 
                for line in process.stdout:
                    self.master.after(0, self.append_output, line.strip())

                #Capture errors and display them in GUI
                errors = process.stderr.read()
                if errors:
                    self.master.after(0, self.append_output, f"Error:\n{errors}")

                return_code = process.wait() # Waits for the script to completely finish running.
                self.master.after(0, self.append_output, f"Tweet fetching completed with return code: {return_code}")
                                
            except Exception as e: # Catches any unexpected problems during this process.
                self.master.after(0, self.append_output, f"Exception occurred: {e}")
    
        #run 'fetch' in a new thread
        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

    # Function to start the sentiment analysis process in a new thread.
    def open_sentiment_analysis(self):
        threading.Thread(target=self.run_sentiment_analysis).start()

    # Function that manages the thread for running the external sentiment analysis script.
    def run_sentiment_analysis(self):
        
        def analyze(): # The work done in the background thread.
            self.master.after(0, self.append_output, "Cleaning tweets and preparing for sentiment analysis...")
            script_path = os.path.join(os.path.dirname(__file__), "analyze_sentiment.py")

            try:
                # Starts the external Python script for analysis.
                process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Reads and displays the script's output line by line as it runs.
                for line in process.stdout:
                    self.master.after(0, self.append_output, line.strip())

                # Captures and displays any errors after the script finishes.
                errors = process.stderr.read()
                if errors:
                    self.master.after(0, self.append_output, f"Error:\n{errors}")
                
                return_code = process.wait()
                self.master.after(0, self.append_output, f"Sentiment cleaning completed with return code: {return_code}")
            
            except Exception as e:
                self.master.after(0, self.append_output, f"Exception occured: {e}")

        # Run the cleaning script in a new thread so GUI doesn't freeze
        thread = threading.Thread(target=analyze, daemon=True)
        thread.start()

# This block of code ensures the application starts correctly when the file is run.
if __name__ == "__main__":
    root = tk.Tk() # Creates the very first main window object.
    login = LoginScreen(root) # Creates an instance of the LoginScreen to display.
    root.mainloop() # Starts the tkinter event loop, which keeps the window open and responsive.