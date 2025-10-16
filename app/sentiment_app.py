# Import core tkinter GUI library and the messagebox helper for pop-up alerts
import tkinter as tk
from tkinter import messagebox
import datetime  # Used for timestamps on each output line

# --- BRAND / STYLE COLORS ---
BRAND_DARK_BLUE = "#1A237E"   # Primary accent color
BRAND_ACCENT = "#2C3A8E"      # Hover color for buttons
LIGHT_GRAY_BG = "#F0F0F0"     # Background color for the window
CARD_BG = "#FFFFFF"           # Card background color (white panels)
TEXT_MUTED = "#555555"        # Subtle gray text for details
TEXT_OK = "#1B5E20"           # Green for positive messages
TEXT_WARN = "#E65100"         # Orange for warnings/negatives
TEXT_INFO = "#0D47A1"         # Blue for informational lines

# --- MAIN APPLICATION CLASS ---
class SentimentAnalysisApp:
    def __init__(self, master, demo=True):  # Initialize class with Tk root and demo flag
        self.demo = demo                    # Whether app is in demo mode (no API calls)
        self.master = master                # Store reference to the main Tk window
        self.master.title("Libra Technology: Sentiment Analysis")  # Window title
        self.master.geometry("720x540")     # Set window size
        self.master.configure(bg=LIGHT_GRAY_BG)  # Background color of root window
        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"  # Hint text

        # Main container frame inside the root window
        container = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=16, pady=16)
        container.pack(expand=True, fill=tk.BOTH)  # Expand to fill all available space

        # --- HEADER SECTION ---
        header = tk.Frame(container, bg=LIGHT_GRAY_BG)
        header.pack(fill=tk.X)  # Stretches horizontally
        left = tk.Frame(header, bg=LIGHT_GRAY_BG)
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Left-aligned header info

        # App title
        tk.Label(left, text="Libra Technology", font=("Helvetica", 18, "bold"),
                 bg=LIGHT_GRAY_BG, fg=BRAND_DARK_BLUE).pack(anchor="w")
        # Subtitle
        tk.Label(left, text="Movie Sentiment Analysis Tool",
                 font=("Helvetica", 11), bg=LIGHT_GRAY_BG, fg=TEXT_MUTED).pack(anchor="w")

        # Demo mode indicator (right-aligned label)
        right = tk.Frame(header, bg=LIGHT_GRAY_BG)
        right.pack(side=tk.RIGHT)
        if self.demo:  # If demo mode is active, show orange tag
            tk.Label(right, text="DEMO MODE • no API calls", font=("Arial", 10, "bold"),
                     bg="#FFF4E5", fg="#8A4B00", padx=8, pady=4, relief=tk.GROOVE).pack()

        # --- MAIN CONTENT CARD ---
        card = tk.Frame(container, bg=CARD_BG, padx=14, pady=14)
        card.pack(fill=tk.BOTH, expand=True, pady=12)

        # Input row for keyword entry
        input_row = tk.Frame(card, bg=CARD_BG)
        input_row.pack(fill=tk.X, pady=(0,8))
        tk.Label(input_row, text="Movie keyword", font=("Arial", 12), bg=CARD_BG).pack(side=tk.LEFT)
        self.keyword_entry = tk.Entry(input_row, font=("Arial", 12), width=34, fg="gray")
        self.keyword_entry.pack(side=tk.LEFT, padx=8)
        self.keyword_entry.insert(0, self.placeholder_text)  # Show placeholder text initially
        self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)   # Event: clear placeholder
        self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out) # Event: restore placeholder

        # --- BUTTON ROW ---
        btn_row = tk.Frame(card, bg=CARD_BG)
        btn_row.pack(fill=tk.X, pady=(0,8))

        # Fetch Tweets button
        self.fetch_btn = tk.Button(
            btn_row, text="Fetch Tweets", font=("Arial", 12, "bold"),
            bg=BRAND_DARK_BLUE, fg="white", activebackground=BRAND_ACCENT,
            padx=10, pady=6, command=self.open_fetch_tweets
        )
        self.fetch_btn.grid(row=0, column=0, padx=(0,6))

        # Analyze Sentiment button
        self.analyze_btn = tk.Button(
            btn_row, text="Analyze Sentiment", font=("Arial", 12, "bold"),
            bg=BRAND_DARK_BLUE, fg="white", activebackground=BRAND_ACCENT,
            padx=10, pady=6, command=self.open_sentiment_analysis, state=tk.DISABLED
        )
        self.analyze_btn.grid(row=0, column=1, padx=6)

        # Clear output button
        self.clear_btn = tk.Button(btn_row, text="Clear", font=("Arial", 11), command=self.clear_output)
        self.clear_btn.grid(row=0, column=2, padx=6)

        # Copy output button
        self.copy_btn = tk.Button(btn_row, text="Copy Output", font=("Arial", 11), command=self.copy_output)
        self.copy_btn.grid(row=0, column=3, padx=6)

        btn_row.grid_columnconfigure(4, weight=1)  # Flexible column spacing

        # --- OUTPUT TEXT AREA ---
        text_frame = tk.Frame(card, bg=CARD_BG)
        text_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the main text box where results will appear
        self.output_text = tk.Text(
            text_frame, wrap=tk.WORD, height=12, font=("Arial", 12),
            yscrollcommand=scrollbar.set, bg="#FAFAFA", relief=tk.FLAT
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Define color tags for styled text output
        self.output_text.tag_configure("muted", foreground=TEXT_MUTED)
        self.output_text.tag_configure("ok", foreground=TEXT_OK)
        self.output_text.tag_configure("warn", foreground=TEXT_WARN)
        self.output_text.tag_configure("info", foreground=TEXT_INFO)
        self.output_text.tag_configure("bold", font=("Arial", 12, "bold"))

        # --- STATUS BAR ---
        self.status = tk.StringVar(value="Ready")  # Holds bottom status message
        tk.Label(container, textvariable=self.status, anchor="w",
                 bg=LIGHT_GRAY_BG, fg=TEXT_MUTED, font=("Arial", 10)).pack(fill=tk.X, pady=(6,0))

        # --- SHORTCUTS ---
        self.master.bind("<Return>", lambda _: self.open_fetch_tweets())       # Press Enter to fetch
        self.master.bind("<Control-l>", lambda _: self.clear_output())         # Ctrl+L clears
        self.master.bind("<Control-Shift-C>", lambda _: self.copy_output())    # Ctrl+Shift+C copies

        # Initial greeting banner
        self._banner("Welcome", "Demo is enabled. No AI/API usage.", "info")

        # If demo mode: automatically run a demo after startup
        if self.demo:
            self.master.after(400, self._auto_demo)

    # --- EVENT HANDLERS ---
    def _auto_demo(self):  # Runs an automatic demo sequence
        self.keyword_entry.focus_set()
        self.keyword_entry.delete(0, tk.END)
        self.keyword_entry.config(fg="black")
        self.keyword_entry.insert(0, "Dune 2")  # Auto-fill demo keyword
        self.open_fetch_tweets()                # Simulate pressing Fetch
        self.master.after(900, self.open_sentiment_analysis)  # Simulate analysis after delay

    def _on_entry_focus_in(self, _):  # Clears placeholder on focus
        if self.keyword_entry.get() == self.placeholder_text and self.keyword_entry.cget("fg") == "gray":
            self.keyword_entry.delete(0, tk.END)
            self.keyword_entry.config(fg="black")

    def _on_entry_focus_out(self, _):  # Restores placeholder when field is empty
        if not self.keyword_entry.get().strip():
            self.keyword_entry.insert(0, self.placeholder_text)
            self.keyword_entry.config(fg="gray")

    # --- UTILITIES FOR OUTPUT ---
    def _ts(self):  # Generate timestamp for each line
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _append(self, text, tag=None):  # Add line to text box with optional tag color
        prefix = f"[{self._ts()}] "
        if tag:
            self.output_text.insert(tk.END, prefix, "muted")
            self.output_text.insert(tk.END, text + "\n", tag)
        else:
            self.output_text.insert(tk.END, prefix + text + "\n")
        self.output_text.see(tk.END)

    def _section(self, title):  # Prints section header in bold with divider
        self.output_text.insert(tk.END, "\n")
        self.output_text.insert(tk.END, f"{title}\n", "bold")
        self.output_text.insert(tk.END, "—" * max(8, len(title)) + "\n", "muted")

    def _banner(self, title, subtitle, tag="info"):  # Prints formatted section banner
        self._section(title)
        self._append(subtitle, tag=tag)

    def _set_busy(self, busy=True, note="Working…"):  # Disable UI while fetching/analyzing
        state = tk.DISABLED if busy else tk.NORMAL
        self.fetch_btn.config(state=state)
        self.analyze_btn.config(state=state if self.output_text.get("1.0", tk.END).strip() else tk.DISABLED)
        self.clear_btn.config(state=state)
        self.copy_btn.config(state=state)
        self.keyword_entry.config(state=state)
        self.status.set(note if busy else "Ready")
        self.master.config(cursor="watch" if busy else "")

    # --- BUTTON ACTIONS ---
    def clear_output(self):  # Clears output text area
        self.output_text.delete("1.0", tk.END)
        self.status.set("Cleared")
        self.analyze_btn.config(state=tk.DISABLED)

    def copy_output(self):  # Copies all output text to clipboard
        data = self.output_text.get("1.0", tk.END).strip()
        if not data:
            messagebox.showinfo("Nothing to copy", "Output is empty.")
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(data)
        self.status.set("Copied output to clipboard")

    def open_fetch_tweets(self):  # Handler for Fetch Tweets button
        kw = self.keyword_entry.get().strip()
        if not kw or (kw == self.placeholder_text and self.keyword_entry.cget("fg") == "gray"):
            messagebox.showinfo("Missing keyword", "Enter a movie keyword first.")
            return
        self._set_busy(True, f"Fetching demo data for '{kw}'…")
        self._section(f"Fetch: {kw}")
        self._append(f"Searching recent posts for '{kw}' (demo)", tag="info")
        self.master.after(350, lambda: self._mock_fetch(kw))  # Simulate short wait

    def _mock_fetch(self, kw):  # Simulated tweet results
        mock = [
            f"Loved {kw}, cinematography was insane!",
            f"{kw} was mid tbh.",
            f"The soundtrack totally carried {kw}.",
            f"I'd rewatch {kw} just for the visuals.",
        ]
        for line in mock:
            tone = "ok" if any(w in line.lower() for w in ["loved", "carried", "rewatch"]) else "warn"
            self._append(f"Tweet: {line}", tag=tone)
        self._append("Fetched 4 demo items", tag="muted")
        self.status.set("Fetched demo tweets")
        self._set_busy(False)
        self.analyze_btn.config(state=tk.NORMAL)

    def open_sentiment_analysis(self):  # Handler for Analyze Sentiment button
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("No data", "Fetch tweets first.")
            return
        self._set_busy(True, "Analyzing (demo)…")
        self._section("Analysis")
        self._append("Running quick sentiment check (demo)", tag="info")
        self.master.after(300, self._mock_analyze)  # Simulated analysis delay

    def _mock_analyze(self):  # Fake sentiment analysis logic
        lines = [l for l in self.output_text.get("1.0", tk.END).splitlines() if l.strip().startswith("Tweet:")]
        pos = sum(any(w in l.lower() for w in ["loved", "carried", "rewatch", "insane"]) for l in lines)
        neg = sum(any(w in l.lower() for w in ["mid", "boring", "bad"]) for l in lines)
        total = max(1, pos + neg)
        score = round((pos - neg) / total, 2)
        self._append(f"positives={pos}, negatives={neg}, score={score}", tag=("ok" if score >= 0 else "warn"))
        verdict = "Overall leaning positive" if score > 0 else "Overall leaning negative" if score < 0 else "Mixed/neutral"
        self._append(verdict, tag=("ok" if score > 0 else "warn" if score < 0 else "info"))
        self._set_busy(False)
        self.status.set("Analysis complete (demo)")

# --- MAIN PROGRAM START ---
if __name__ == "__main__":
    root = tk.Tk()                              # Create main window
    app = SentimentAnalysisApp(root, demo=True) # Create app instance in demo mode
    root.mainloop()                             # Run event loop until closed
