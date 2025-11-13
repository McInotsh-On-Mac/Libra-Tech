# run.py

# Step 0: Force PyInstaller to include the utils package
import app.utils.env_loader  

# Step 1: Load environment variables
from app.utils.env_loader import load_env
load_env()  # Must be called before any Twitter or DB code that uses .env

# Step 2: Import the rest of the application
import tkinter as tk
from app.login_screen import LoginScreen

# Step 3: Main function
def main():
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Change directory to the location of the executable
import os
os.chdir(r"C:\Users\bjher\Libra-Tech\dist")

# Execute the compiled Python file
os.system("run.exe")
