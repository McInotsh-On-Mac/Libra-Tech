import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Python 3.7 or higher is required.")
        return False
    print(f"Python {sys.version.split()[0]} detected")
    return True

def create_batch_launcher():
    """Create platform-specific launcher."""
    system = platform.system()
    
    if system == "Windows":
        # Create ONLY ONE Windows batch file in root directory
        with open("LibraTech.bat", "w") as f:
            f.write("""@echo off
echo Starting Libra-Tech Sentiment Analysis App...
cd /d "%~dp0"
if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)
call venv\\Scripts\\activate
python run.py
if errorlevel 1 (
    echo Application exited with an error.
    pause
)
""")
        print("Created LibraTech.bat launcher for Windows")
        
    elif system == "Darwin":  # macOS
        # Create macOS app bundle structure
        app_dir = "LibraTech.app/Contents/MacOS"
        os.makedirs(app_dir, exist_ok=True)
        
        # Create Info.plist
        with open("LibraTech.app/Contents/Info.plist", "w") as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>LibraTech</string>
    <key>CFBundleIdentifier</key>
    <string>com.libratech.sentimentanalysis</string>
    <key>CFBundleName</key>
    <string>LibraTech</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>""")
        
        # Create executable
        with open(f"{app_dir}/LibraTech", "w") as f:
            f.write(f"""#!/bin/bash
cd "{os.getcwd()}"
./launcher.sh
""")
        
        os.chmod(f"{app_dir}/LibraTech", 0o755)
        print("Created LibraTech.app for macOS")
        
        # Create desktop command file
        desktop_command = os.path.expanduser("~/Desktop/LibraTech.command")
        with open(desktop_command, "w") as f:
            f.write(f"""#!/bin/bash
cd "{os.getcwd()}"
./launcher.sh
""")
        os.chmod(desktop_command, 0o755)
        print("Created LibraTech.command on desktop")
        
    else:  # Linux
        # Create desktop entry
        desktop_file = os.path.expanduser("~/Desktop/LibraTech.desktop")
        with open(desktop_file, "w") as f:
            f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=LibraTech Sentiment Analysis
Comment=Sentiment Analysis on X (Twitter)
Exec={os.getcwd()}/launcher.sh
Icon={os.getcwd()}/assets/icons/icon.png
Terminal=true
Categories=Application;
""")
        os.chmod(desktop_file, 0o755)
        print("Created desktop entry for Linux")

def create_shortcuts_folder():
    """Create organized shortcuts folder with instructions."""
    os.makedirs("desktop_shortcuts", exist_ok=True)
    
    # Create README for manual shortcut creation
    with open("desktop_shortcuts/README.md", "w") as f:
        f.write("""# Desktop Shortcuts

This folder contains templates and instructions for creating desktop shortcuts manually.

## Automatic Installation
Run the appropriate installer for your platform:
- **Windows**: `install.bat`
- **macOS/Linux**: `install.sh`

The installer will automatically create desktop shortcuts.

## Manual Shortcut Creation

### Windows
1. Right-click on desktop
2. Choose "New" > "Shortcut"
3. Browse to and select `LibraTech.bat` in the project root
4. Name it "LibraTech Sentiment Analysis"

### macOS
1. The installer creates `LibraTech.command` on your desktop
2. Or drag `LibraTech.app` to your Applications folder

### Linux
1. Copy `LibraTech.desktop` to your desktop
2. Make it executable: `chmod +x ~/Desktop/LibraTech.desktop`
3. Or copy to `~/.local/share/applications/` for app menu
""")
    
    # Create Linux desktop entry template
    with open("desktop_shortcuts/LibraTech.desktop", "w") as f:
        f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=LibraTech Sentiment Analysis
Comment=Sentiment Analysis on X (Twitter)
Exec={os.getcwd()}/launcher.sh
Icon={os.getcwd()}/assets/icons/icon.png
Terminal=true
Categories=Application;
""")

def main():
    """Main setup function."""
    print("Setting up Libra-Tech for easy launching...")
    
    if not check_python_version():
        return False
    
    create_batch_launcher()
    create_shortcuts_folder()
    
    print("\nSetup completed!")
    print("\nYou can now launch the app by:")
    
    system = platform.system()
    if system == "Windows":
        print("   • Double-clicking LibraTech.bat")
    elif system == "Darwin":
        print("   • Double-clicking LibraTech.app")
        print("   • Double-clicking LibraTech.command on your desktop")
    else:
        print("   • Double-clicking LibraTech.desktop on your desktop")
    
    print("   • Running ./launcher.sh in terminal")
    
    return True

if __name__ == "__main__":
    main()