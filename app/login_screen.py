import tkinter as tk
from tkinter import messagebox
import psycopg2
import os
from .sentiment_app import SentimentAnalysisApp
from .db import get_db_connection




class LoginScreen:
    # TODO(Ryan): (Login Page UI Redesign) should improve layout, style, and user experience here
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("350x300")
        self.master.configure(bg="#ADD8E6")

        self.frame = tk.Frame(master, bg="#ADD8E6", padx=20, pady=20)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        self.message_label = tk.Label(self.frame, text="", fg="red", bg="#ADD8E6", font=("Arial", 10))
        self.message_label.grid(row=2, columnspan=2, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.validate_login, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.login_button.grid(row=3, columnspan=2, pady=10)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
        self.signup_button.grid(row=4, columnspan=2, pady=10)

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

    def open_signup(self):
        # TODO(Ryan): (Login Page UI Redesign) can improve signup window UI/UX
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")
        signup_window.geometry("350x200")
        signup_window.configure(bg="#ADD8E6")

        frame = tk.Frame(signup_window, bg="#ADD8E6", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="New Username:", font=("Arial", 12), bg="#ADD8E6").grid(row=0, column=0, sticky="w", pady=5)
        new_username = tk.Entry(frame, font=("Arial", 12))
        new_username.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="New Password:", font=("Arial", 12), bg="#ADD8E6").grid(row=1, column=0, sticky="w", pady=5)
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