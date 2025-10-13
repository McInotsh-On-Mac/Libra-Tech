import tkinter as tk
from tkinter import messagebox
import psycopg2
import os
from .sentiment_app import SentimentAnalysisApp
from .db import get_db_connection

# Define Brand Colors 
BRAND_DARK_BLUE = "#1A237E" # This dark blue color is used for primary text and buttons.
BRAND_TEAL_ACCENT = "#008B8B" # This teal/green color is used for accents.
LIGHT_GRAY_BG = "#F0F0F0" # This new light gray color is used for all backgrounds.

class LoginScreen:
    # TODO(Ryan): (Login Page UI Redesign) should improve layout, style, and user experience here
    def __init__(self, master):  # This function runs when the Login window is created.
        self.master = master # 'master' is the main window object provided by tkinter.
        self.master.title("LIBRA TECHNOLOGIES: Secure Login") # Sets the title text at the top of the window.
        self.master.geometry("400x350") # Sets the starting size of the window (width x height).
        self.master.configure(bg=LIGHT_GRAY_BG) # Sets the entire window's background color to light gray.

        # Branding Header
        # Creates the main title with the brand's name and color.
        tk.Label(master, text="LIBRA TECHNOLOGIES", font=("Segoe UI", 18, "bold"), bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(pady=(20, 5))
        # Creates a subtitle for the current screen, using the accent color.
        tk.Label(master, text="Secure Login", font=("Segoe UI", 12), bg=LIGHT_GRAY_BG, fg=BRAND_TEAL_ACCENT).pack(pady=(0, 15))

        # Create a container (frame) to hold the username and password fields.
        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        self.frame.pack(expand=True)

        # Username Input
        tk.Label(self.frame, text="Username:", font=("Segoe UI", 11), bg=LIGHT_GRAY_BG).grid(row=0, column=0, sticky="w", pady=5) 
        self.username_entry = tk.Entry(self.frame, font=("Segoe UI", 12), width =25, relief=tk.FLAT, bd=2)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        # Password Input
        tk.Label(self.frame, text="Password:", font=("Segoe UI", 11), bg=LIGHT_GRAY_BG).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.frame, font=("Segoe UI", 12), show="*") # Hides characters when typing a password.
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)


        # A label for showing error messages or success status.
        self.message_label = tk.Label(self.frame, text="", fg="red", bg=LIGHT_GRAY_BG, font=("Arial", 10))
        self.message_label.grid(row=2, columnspan=2, pady=5)


        # Login Button (Styled with Brand Blue)
        self.login_button = tk.Button(self.frame, text="Login", command=self.validate_login, font=("Segoe UI", 12), 
                                      bg=BRAND_DARK_BLUE, fg="white", activebackground="#2C3A8E", padx=20, pady=5, relief=tk.FLAT)
        self.login_button.grid(row=3, columnspan=2, pady=(20,10))


        # Sign Up Button (Styled with Gray)
        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup, font=("Segoe UI", 12), 
                                       bg="#CCCCCC", fg="black", activebackground="#BBBBBB", padx=20, pady=5, relief=tk.FLAT)
        self.signup_button.grid(row=4, columnspan=2, pady=5)


    def validate_login(self):
        # TODO(Sebastian): (Backend: User Authentication API) should handle authentication logic here
        username = self.username_entry.get()
        password = self.password_entry.get()


        if self.check_credentials(username, password):
            self.message_label.config(text="Login successful!", fg="green")
            self.open_sentiment_analysis()
        else:
            self.message_label.config(text="Username or password is wrong", fg="red")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


    def check_credentials(self, username, password):
        # TODO(Sebastian): update this logic to check db and implement proper security (password hashing, etc.)
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    stored_user, stored_pass = line.strip().split(",")
                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            return False
        return False


    def open_signup(self): # This function handles opening the separate Sign Up window.
        # TODO(Ryan): (Login Page UI Redesign) can improve signup window UI/UX
        signup_window = tk.Toplevel(self.master) # Creates a new window on top of the main one.
        signup_window.title("Sign Up")
        signup_window.geometry("350x200")
        signup_window.configure(bg=LIGHT_GRAY_BG) # Sets the new window's background color.


        frame = tk.Frame(signup_window, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        frame.pack(expand=True)


        tk.Label(frame, text="New Username:", font=("Arial", 12), bg=LIGHT_GRAY_BG).grid(row=0, column=0, sticky="w", pady=5)
        new_username = tk.Entry(frame, font=("Arial", 12))
        new_username.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="New Password:", font=("Arial", 12), bg=LIGHT_GRAY_BG).grid(row=1, column=0, sticky="w", pady=5)
        new_password = tk.Entry(frame, font=("Arial", 12), show="*")
        new_password.grid(row=1, column=1, pady=5, padx=10)


        def save_credentials():
            # TODO(Sebastian): should handle user creation logic with db integration and password hashing
            username = new_username.get()
            password = new_password.get()
            if not username or not password:
                return
            try:
                with open("users.txt", "r") as file:
                    for line in file:
                        stored_user, _ = line.strip().split(",")
                        if stored_user == username:
                            tk.messagebox.showerror("Error", "Username already exists.")
                            return
                       
            except FileNotFoundError:
                pass


            with open("users.txt", "a") as file:
                file.write(f"{username},{password}\n")
            signup_window.destroy()


        signup_button = tk.Button(frame, text="Sign Up", command=save_credentials, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        signup_button.grid(row=2, columnspan=2, pady=10)


    def open_sentiment_analysis(self):
        self.master.destroy()
        root = tk.Tk()
        app = SentimentAnalysisApp(root)
        root.mainloop()
