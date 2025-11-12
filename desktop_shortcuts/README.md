# Desktop Shortcuts

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
