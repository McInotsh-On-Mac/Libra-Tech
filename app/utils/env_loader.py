# app/utils/env_loader.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def _candidate_env_paths():
    """
    Yield candidate .env paths in order of preference:
      1) external .env in current working directory
      2) .env next to the running executable (PyInstaller uses _MEIPASS or sys.executable path)
      3) .env next to this source file (useful in development)
    """
    # cwd first (allows desktop shortcut Start in or user-provided .env)
    cwd = Path(os.getcwd())
    yield cwd / ".env"

    # If running frozen (PyInstaller) try the exe directory and _MEIPASS
    if getattr(sys, "frozen", False):
        # sys._MEIPASS is where PyInstaller extracts files for onefile
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            yield Path(meipass) / ".env"
        exe_dir = Path(sys.executable).parent
        yield exe_dir / ".env"

    # fallback: project / package directory
    pkg_dir = Path(__file__).parent.parent  # app/utils -> app
    yield pkg_dir / ".env"
    yield Path(__file__).parent / ".env"

def load_env(override=False):
    """
    Load environment variables from the first existing .env found.
    - override: if True, variables from .env will overwrite existing os.environ.
    The function always leaves existing environment variables intact unless override=True.
    If no .env is found the function does nothing (app should rely on real env vars).
    """
    found = None
    for p in _candidate_env_paths():
        try:
            p = p.resolve()
        except Exception:
            p = p
        if p.is_file():
            found = p
            break

    if found:
        load_dotenv(dotenv_path=str(found), override=override)
        # small debug print to console/log; safe to remove later
        print(f"Loaded .env from: {found}")
        return True

    # no .env found; still OK — rely on environment variables
    print("No .env found in candidates; using environment variables if present.")
    return False
