# app/api_config_screen.py

import tkinter as tk
from tkinter import messagebox
import os
from pathlib import Path

# Brand Colors
BRAND_DARK_BLUE = "#1A237E"
BRAND_TEAL_ACCENT = "#008B8B"
LIGHT_GRAY_BG = "#F0F0F0"
WHITE_TEXT = "#FFFFFF"

class APIConfigScreen:
    """Screen for configuring Twitter API credentials after login"""
    
    def __init__(self, master, on_continue_callback):
        self.master = master
        self.on_continue = on_continue_callback
        self.master.title("LIBRA TECHNOLOGIES: API Configuration")
        self.master.geometry("900x750")
        self.master.configure(bg=LIGHT_GRAY_BG)
        
        # Get path to .env file
        self.env_path = Path(__file__).parent.parent / '.env'
        
        # Center the form
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        
        # Main frame
        main_frame = tk.Frame(self.master, bg=LIGHT_GRAY_BG, padx=40, pady=40)
        main_frame.grid(row=1, column=1)
        
        # Header
        tk.Label(
            main_frame, 
            text="LIBRA TECHNOLOGIES", 
            font=("Segoe UI", 24, "bold"), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE
        ).pack(pady=(20, 10))
        
        tk.Label(
            main_frame, 
            text="Twitter API Configuration", 
            font=("Segoe UI", 16), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_TEAL_ACCENT
        ).pack(pady=(0, 20))
        
        # Instructions
        instructions = (
            "Please enter your Twitter API credentials below.\n"
            "These will be securely stored for accessing Twitter data.\n\n"
            "If you don't have credentials yet, visit:\n"
            "https://developer.twitter.com/en/portal/dashboard"
        )
        tk.Label(
            main_frame,
            text=instructions,
            font=("Segoe UI", 11),
            bg=LIGHT_GRAY_BG,
            fg="#333333",
            justify=tk.LEFT
        ).pack(pady=(0, 20))
        
        # Input fields frame
        input_frame = tk.LabelFrame(
            main_frame, 
            text="API Credentials", 
            font=("Segoe UI", 14, "bold"), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE, 
            padx=20, 
            pady=20
        )
        input_frame.pack(pady=(10, 20), padx=20, fill="both", expand=True)
        
        # Check if credentials already exist
        existing_creds = self.load_existing_credentials()
        
        # API Key
        tk.Label(
            input_frame, 
            text="API Key:", 
            font=("Segoe UI", 12), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE
        ).grid(row=0, column=0, sticky="w", pady=10)
        self.api_key_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=50, relief=tk.FLAT, bd=2)
        self.api_key_entry.grid(row=0, column=1, pady=10, padx=10)
        if existing_creds.get('API_KEY'):
            self.api_key_entry.insert(0, existing_creds['API_KEY'])
        
        # API Secret
        tk.Label(
            input_frame, 
            text="API Secret:", 
            font=("Segoe UI", 12), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE
        ).grid(row=1, column=0, sticky="w", pady=10)
        self.api_secret_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=50, relief=tk.FLAT, bd=2, show="*")
        self.api_secret_entry.grid(row=1, column=1, pady=10, padx=10)
        if existing_creds.get('API_SECRET'):
            self.api_secret_entry.insert(0, existing_creds['API_SECRET'])
        
        # Access Token
        tk.Label(
            input_frame, 
            text="Access Token:", 
            font=("Segoe UI", 12), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE
        ).grid(row=2, column=0, sticky="w", pady=10)
        self.access_token_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=50, relief=tk.FLAT, bd=2)
        self.access_token_entry.grid(row=2, column=1, pady=10, padx=10)
        if existing_creds.get('ACCESS_TOKEN'):
            self.access_token_entry.insert(0, existing_creds['ACCESS_TOKEN'])
        
        # Access Secret
        tk.Label(
            input_frame, 
            text="Access Secret:", 
            font=("Segoe UI", 12), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE
        ).grid(row=3, column=0, sticky="w", pady=10)
        self.access_secret_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=50, relief=tk.FLAT, bd=2, show="*")
        self.access_secret_entry.grid(row=3, column=1, pady=10, padx=10)
        if existing_creds.get('ACCESS_SECRET'):
            self.access_secret_entry.insert(0, existing_creds['ACCESS_SECRET'])
        
        # Bearer Token
        tk.Label(
            input_frame, 
            text="Bearer Token:", 
            font=("Segoe UI", 12), 
            bg=LIGHT_GRAY_BG, 
            fg=BRAND_DARK_BLUE
        ).grid(row=4, column=0, sticky="w", pady=10)
        self.bearer_token_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=50, relief=tk.FLAT, bd=2)
        self.bearer_token_entry.grid(row=4, column=1, pady=10, padx=10)
        if existing_creds.get('BEARER_TOKEN'):
            self.bearer_token_entry.insert(0, existing_creds['BEARER_TOKEN'])
        
        # Status message
        self.status_label = tk.Label(
            main_frame, 
            text="", 
            font=("Segoe UI", 11), 
            bg=LIGHT_GRAY_BG
        )
        self.status_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=LIGHT_GRAY_BG)
        button_frame.pack(pady=(10, 10))
        
        # Save button
        self.save_button = tk.Button(
            button_frame, 
            text="Save Credentials", 
            command=self.save_credentials,
            font=("Segoe UI", 14, "bold"),
            bg=BRAND_TEAL_ACCENT, 
            fg=BRAND_DARK_BLUE, 
            activebackground=WHITE_TEXT, 
            padx=30, 
            pady=10, 
            relief=tk.FLAT
        )
        self.save_button.grid(row=0, column=0, padx=20)
        
        # Continue button
        self.continue_button = tk.Button(
            button_frame, 
            text="Continue to App", 
            command=self.continue_to_app,
            font=("Segoe UI", 14, "bold"),
            bg="#CCCCCC", 
            fg=BRAND_DARK_BLUE, 
            activebackground=WHITE_TEXT, 
            padx=30, 
            pady=10, 
            relief=tk.FLAT
        )
        self.continue_button.grid(row=0, column=1, padx=20)
        
        # Skip button (if credentials already exist)
        if existing_creds:
            self.status_label.config(
                text="✓ Existing credentials found. You can update them or continue.",
                fg="green"
            )
    
    def load_existing_credentials(self):
        """Load existing credentials from .env file if they exist"""
        creds = {}
        try:
            if self.env_path.exists():
                with open(self.env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            if key in ['API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'ACCESS_SECRET', 'BEARER_TOKEN']:
                                creds[key] = value
        except Exception as e:
            print(f"Error loading existing credentials: {e}")
        return creds
    
    def save_credentials(self):
        """Save credentials to .env file"""
        # Get values from entries
        api_key = self.api_key_entry.get().strip()
        api_secret = self.api_secret_entry.get().strip()
        access_token = self.access_token_entry.get().strip()
        access_secret = self.access_secret_entry.get().strip()
        bearer_token = self.bearer_token_entry.get().strip()
        
        # Validate all fields are filled
        if not all([api_key, api_secret, access_token, access_secret, bearer_token]):
            self.status_label.config(
                text="Please fill in all fields",
                fg="red"
            )
            messagebox.showerror("Validation Error", "All credential fields are required.")
            return
        
        try:
            # Read existing .env content to preserve other variables
            existing_lines = []
            existing_keys = set()
            
            if self.env_path.exists():
                with open(self.env_path, 'r') as f:
                    for line in f:
                        stripped = line.strip()
                        if stripped and not stripped.startswith('#') and '=' in stripped:
                            key = stripped.split('=', 1)[0]
                            if key not in ['API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'ACCESS_SECRET', 'BEARER_TOKEN']:
                                existing_lines.append(line)
                                existing_keys.add(key)
                        elif stripped.startswith('#') or not stripped:
                            existing_lines.append(line)
            
            # Write updated .env file
            with open(self.env_path, 'w') as f:
                # Write existing non-API credentials
                for line in existing_lines:
                    f.write(line)
                
                # Write new API credentials
                f.write(f"\n# Twitter API Credentials\n")
                f.write(f"API_KEY={api_key}\n")
                f.write(f"API_SECRET={api_secret}\n")
                f.write(f"ACCESS_TOKEN={access_token}\n")
                f.write(f"ACCESS_SECRET={access_secret}\n")
                f.write(f"BEARER_TOKEN={bearer_token}\n")
            
            self.status_label.config(
                text="✓ Credentials saved successfully!",
                fg="green"
            )
            
            # Reload environment variables immediately
            from dotenv import load_dotenv
            load_dotenv(override=True)
            
            messagebox.showinfo(
                "Success", 
                "API credentials have been saved successfully!\n\n"
                "You can now continue to the application."
            )
            
        except Exception as e:
            self.status_label.config(
                text=f"Error saving credentials: {str(e)}",
                fg="red"
            )
            messagebox.showerror("Error", f"Failed to save credentials:\n{str(e)}")
    
    def continue_to_app(self):
        """Continue to the main sentiment analysis app"""
        # Check if credentials exist
        if not self.load_existing_credentials():
            response = messagebox.askyesno(
                "No Credentials",
                "No API credentials found. Do you want to continue anyway?\n\n"
                "Note: The app may not function properly without valid credentials."
            )
            if not response:
                return
        
        # Call the callback to open the main app
        self.master.destroy()
        if self.on_continue:
            self.on_continue()