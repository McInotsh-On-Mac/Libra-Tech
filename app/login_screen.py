import tkinter as tk # Tkinter is used to build graphical user interfaces (GUIs) in Python.
from tkinter import messagebox #Used to show popup messages (like alerts).
import psycopg2 # Import the psycopg2 library to connect and interact with PostgreSQL databases.
import os #Lets Python interact with the operating system (like reading files or paths).
import bcrypt # Ssafely encrypts and checks passwords.
from .sentiment_app import SentimentAnalysisApp #Allows the program to open that app after a successful login.
from .db import get_db_connection # Import the function that connects to the database from another file in this project.

# ---------------------- VISUAL DESIGN SETTINGS ----------------------

# Define Brand Colors 
BRAND_DARK_BLUE = "#1A237E"  # This dark blue color is used for primary text and buttons.
BRAND_TEAL_ACCENT = "#008B8B"  # This teal/green color is used for accents.
LIGHT_GRAY_BG = "#F0F0F0"  # This new light gray color is used for all backgrounds.
WHITE_TEXT = "#FFFFFF"  # White text for better contrast on dark backgrounds.

# (Ryan): (Login Page UI Redesign)
class LoginScreen:
    def __init__(self, master):  # This function runs when the Login window is created.
        self.master = master # Save the window reference for use in other parts of the class.
        self.master.title("LIBRA TECHNOLOGIES: Secure Login")  # Sets the title text at the top of the window.
        self.master.geometry("1000x700")  # Increased the window size for better visibility.
        self.master.configure(bg=LIGHT_GRAY_BG)  # Sets the entire window's background color to light gray.

        # (Ryan): Center the login form in the middle of the page
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        # (Ryan): Create the main frame for the login form
        login_frame = tk.Frame(self.master, bg=LIGHT_GRAY_BG, padx=40, pady=40)
        login_frame.grid(row=1, column=1)

        # (Ryan): Add a header with branding
        tk.Label(login_frame, text="LIBRA TECHNOLOGIES", font=("Segoe UI", 24, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(pady=(20, 10))
        tk.Label(login_frame, text="Secure Login Portal", font=("Segoe UI", 16), bg=LIGHT_GRAY_BG, fg=BRAND_TEAL_ACCENT).pack(pady=(0, 30))

        # (Ryan): Group input fields in a bordered frame
        input_frame = tk.LabelFrame(login_frame, text="Login Details", font=("Segoe UI", 14, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE, padx=20, pady=20)
        input_frame.pack(pady=(10, 30), padx=20, fill="both", expand=True)

        # (Ryan): Add username input field
        tk.Label(input_frame, text="Username:", font=("Segoe UI", 14), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=30, relief=tk.FLAT, bd=2)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        # (Ryan): Add password input field
        tk.Label(input_frame, text="Password:", font=("Segoe UI", 14), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).grid(row=1, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(input_frame, font=("Segoe UI", 14), show="*", relief=tk.FLAT, bd=2)  # Hides characters when typing a password
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # (Ryan): Add a message label for status updates
        self.message_label = tk.Label(login_frame, text="", fg="red", bg=LIGHT_GRAY_BG, font=("Arial", 12))
        self.message_label.pack(pady=10)

        # (Ryan): Add buttons in a separate frame
        button_frame = tk.Frame(login_frame, bg=LIGHT_GRAY_BG)
        button_frame.pack(pady=(10, 10))

        # (Ryan): Style the login button with a contrasting color
        self.login_button = tk.Button(button_frame, text="Login", command=self.validate_login, font=("Segoe UI", 14, "bold"),
                                      bg=BRAND_TEAL_ACCENT, fg="#1A237E", activebackground=WHITE_TEXT, padx=30, pady=10, relief=tk.FLAT)
        self.login_button.grid(row=0, column=0, padx=20)

        # (Ryan): Style the sign-up button
        self.signup_button = tk.Button(button_frame, text="Sign Up", command=self.open_signup, font=("Segoe UI", 14, "bold"),
                                       bg="#CCCCCC", fg="#1A237E", activebackground=WHITE_TEXT, padx=30, pady=10, relief=tk.FLAT)
        self.signup_button.grid(row=0, column=1, padx=20)

    # ---------------------- LOGIN VALIDATION FUNCTION ----------------------

    # (Sebastian): Validates the login credentials entered by the user
    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.check_credentials(username, password):
            self.message_label.config(text="Login successful!", fg="green")
            self.open_sentiment_analysis()  # Open the sentiment analysis app on success
        else:
            self.message_label.config(text="Invalid username or password", fg="red")
            self.username_entry.delete(0, tk.END)  # Clear the username field
            self.password_entry.delete(0, tk.END)  # Clear the password field

    # ---------------------- DATABASE CREDENTIAL CHECK FUNCTION ----------------------

    # (Sebastian): Checks the provided username and password against the database
    def check_credentials(self, username, password):
        try:
            conn = get_db_connection()  # Establish a connection to the database
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username = %s", (username,))
            row = cur.fetchone()  # Fetch the stored password for the given username
            cur.close()
            conn.close()

            if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
                return True  # Return True if the password matches
        except Exception as e:
            print("Database error:", e)
            self.message_label.config(text="Database error", fg="red")  # Display an error message
        return False  # Return False if credentials are invalid or an error occurs

    # ---------------------- SIGN-UP WINDOW FUNCTION ----------------------

    # (Sebastian): Opens a new window for user sign-up
    def open_signup(self):
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("350x200")
        signup_window.configure(bg=LIGHT_GRAY_BG)

        frame = tk.Frame(signup_window, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        frame.pack(expand=True)

        # Username input field
        tk.Label(frame, text="New Username:", font=("Arial", 12), bg=LIGHT_GRAY_BG).grid(row=0, column=0, sticky="w", pady=5)
        new_username_entry = tk.Entry(frame, font=("Arial", 12))
        new_username_entry.grid(row=0, column=1, pady=5, padx=10)

        # Password input field
        tk.Label(frame, text="New Password:", font=("Arial", 12), bg=LIGHT_GRAY_BG).grid(row=1, column=0, sticky="w", pady=5)
        new_password_entry = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password_entry.grid(row=1, column=1, pady=5, padx=10)

        # (Sebastian): Saves the new user credentials to the database
        def save_credentials():
            username = new_username_entry.get()
            password = new_password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return

            try:
                database_connection = get_db_connection()
                database_cursor = database_connection.cursor()

                # Check if the username already exists
                database_cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                if database_cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists.")
                else:
                    # Hash the password before storing it
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                    # Insert the new user into the database
                    database_cursor.execute(
                        "INSERT INTO users (username, password) VALUES (%s, %s)",
                        (username, hashed_password.decode('utf-8'))
                    )
                    database_connection.commit()
                    messagebox.showinfo("Success", "Sign up successful! You can now log in.")
                    signup_window.destroy()

                database_cursor.close()
                database_connection.close()
            except Exception as e:
                print("Database error:", e)
                messagebox.showerror("Error", "Database error")

        # Sign-up button
        signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        signup_button.grid(row=2, columnspan=2, pady=10)

    # ---------------------- OPEN SENTIMENT ANALYSIS APP ----------------------

    # (Sebastian): Opens the sentiment analysis app after a successful login
    def open_sentiment_analysis(self):
        self.master.destroy()
        root = tk.Tk()
        app = SentimentAnalysisApp(root)
        root.mainloop()