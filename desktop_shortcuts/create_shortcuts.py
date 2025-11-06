#!/usr/bin/env python3
"""
LibraTech Desktop Shortcut Creator

This script creates desktop shortcuts for LibraTech Sentiment Analysis App
on Windows, macOS, and Linux platforms.

Usage: python create_shortcuts.py
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_project_root():
    """Get the absolute path to the project root directory."""
    # Get the parent directory of desktop_shortcuts folder
    return Path(__file__).parent.parent.absolute()

def create_windows_shortcut():
    """Create Windows desktop shortcut."""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "LibraTech Sentiment Analysis.lnk")
        target = str(get_project_root() / "LibraTech.bat")
        wDir = str(get_project_root())
        icon = str(get_project_root() / "assets" / "icons" / "icon.ico")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.Description = "LibraTech Sentiment Analysis on X (Twitter)"
        
        # Set icon if it exists
        if os.path.exists(icon):
            shortcut.IconLocation = icon
            
        shortcut.save()
        print("✅ Windows desktop shortcut created successfully!")
        return True
        
    except ImportError:
        print("⚠️  Windows shortcut creation requires 'pywin32' and 'winshell' packages.")
        print("Install with: pip install pywin32 winshell")
        return False
    except Exception as e:
        print(f"❌ Error creating Windows shortcut: {e}")
        return False

def create_macos_shortcut():
    """Create macOS desktop shortcut."""
    try:
        project_root = get_project_root()
        desktop_path = Path.home() / "Desktop" / "LibraTech.command"
        
        # Create command file
        with open(desktop_path, 'w') as f:
            f.write(f"""#!/bin/bash
# LibraTech Sentiment Analysis Launcher
cd "{project_root}"
./launcher.sh
""")
        
        # Make executable
        os.chmod(desktop_path, 0o755)
        
        print("✅ macOS desktop shortcut created successfully!")
        print(f"📁 Shortcut location: {desktop_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating macOS shortcut: {e}")
        return False

def create_linux_shortcut():
    """Create Linux desktop shortcut."""
    try:
        project_root = get_project_root()
        desktop_path = Path.home() / "Desktop" / "LibraTech.desktop"
        icon_path = project_root / "assets" / "icons" / "icon.png"
        
        # Desktop entry content
        desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=LibraTech Sentiment Analysis
Comment=Sentiment Analysis on X (Twitter)
Exec={project_root}/launcher.sh
Icon={icon_path if icon_path.exists() else 'applications-development'}
Terminal=true
Categories=Application;Development;
StartupNotify=true
"""
        
        # Write desktop file
        with open(desktop_path, 'w') as f:
            f.write(desktop_entry)
        
        # Make executable
        os.chmod(desktop_path, 0o755)
        
        # Also create in applications directory for app menu
        apps_dir = Path.home() / ".local" / "share" / "applications"
        apps_dir.mkdir(parents=True, exist_ok=True)
        
        app_path = apps_dir / "LibraTech.desktop"
        with open(app_path, 'w') as f:
            f.write(desktop_entry)
        os.chmod(app_path, 0o755)
        
        print("✅ Linux desktop shortcut created successfully!")
        print(f"📁 Desktop shortcut: {desktop_path}")
        print(f"📁 Application menu: {app_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Linux shortcut: {e}")
        return False

def check_prerequisites():
    """Check if required files exist."""
    project_root = get_project_root()
    required_files = {
        'run.py': project_root / 'run.py',
        'launcher script': project_root / 'launcher.sh' if platform.system() != 'Windows' else project_root / 'LibraTech.bat'
    }
    
    missing_files = []
    for name, path in required_files.items():
        if not path.exists():
            missing_files.append(f"{name} ({path})")
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        print("\nPlease run the installation script first:")
        print("   • Windows: install.bat")
        print("   • macOS/Linux: ./install.sh")
        return False
    
    return True

def create_icon_if_missing():
    """Create a simple icon if none exists."""
    project_root = get_project_root()
    icons_dir = project_root / "assets" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a simple PNG icon using text if PIL is available
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple 64x64 icon
        img = Image.new('RGBA', (64, 64), (26, 35, 126, 255))  # BRAND_DARK_BLUE
        draw = ImageDraw.Draw(img)
        
        # Draw "LT" text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((16, 20), "LT", fill=(0, 139, 139, 255), font=font)  # BRAND_TEAL_ACCENT
        
        icon_path = icons_dir / "icon.png"
        img.save(icon_path)
        print(f"✅ Created simple icon: {icon_path}")
        
    except ImportError:
        # Create placeholder icon info
        icon_info = icons_dir / "icon_info.txt"
        with open(icon_info, 'w') as f:
            f.write("""Icon Files Needed:

For best results, place the following icon files in this directory:
• icon.ico (Windows)
• icon.icns (macOS) 
• icon.png (Linux/Universal)

Icon should be 64x64 pixels or larger.
You can create icons from PNG files using online converters.
""")

def main():
    """Main function to create platform-appropriate shortcuts."""
    print("🔧 LibraTech Desktop Shortcut Creator")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        return False
    
    # Create icon if missing
    create_icon_if_missing()
    
    # Detect platform and create appropriate shortcut
    system = platform.system()
    
    if system == "Windows":
        print("🪟 Detected Windows - Creating desktop shortcut...")
        success = create_windows_shortcut()
    elif system == "Darwin":
        print("🍎 Detected macOS - Creating desktop shortcut...")
        success = create_macos_shortcut()
    elif system == "Linux":
        print("🐧 Detected Linux - Creating desktop shortcut...")
        success = create_linux_shortcut()
    else:
        print(f"❌ Unsupported platform: {system}")
        return False
    
    if success:
        print("\n🎉 Shortcut creation completed!")
        print("\n📋 You can now:")
        print("   • Double-click the desktop shortcut to launch LibraTech")
        print("   • Or run the launcher script directly from the project folder")
        
        if system == "Linux":
            print("   • Find LibraTech in your application menu")
    else:
        print("\n❌ Shortcut creation failed.")
        print("You can still launch the app using:")
        if system == "Windows":
            print("   • Double-click LibraTech.bat in the project folder")
        else:
            print("   • Run ./launcher.sh from the project folder")
    
    return success

def interactive_mode():
    """Interactive mode for user choices."""
    print("\n🔧 LibraTech Shortcut Creator - Interactive Mode")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Create desktop shortcut")
        print("2. Check prerequisites")
        print("3. Create icon files")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            main()
        elif choice == "2":
            if check_prerequisites():
                print("✅ All prerequisites are met!")
            else:
                print("❌ Some prerequisites are missing.")
        elif choice == "3":
            create_icon_if_missing()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()