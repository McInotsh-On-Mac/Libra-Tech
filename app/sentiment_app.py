#Ayinde Hooks - Sentiment Analysis UI with Enhanced Accessibility
# basic gui libs
import tkinter as tk
from tkinter import messagebox
import datetime  # for timestamps
import requests  # for api calls 

# brand + accessibility colors
BRAND_DARK_BLUE = "#1A237E"   # original brand blue (still used for title)
LIGHT_GRAY_BG   = "#F0F0F0"   # window bg

# new high-contrast ui tokens
BTN_BG           = "#304FFE"   # bright blue button
BTN_BG_ACTIVE    = "#1E40FF"   # darker on press
BTN_FG           = "#000000"   # black text for readability
BTN_FG_DISABLED  = "#333333"   # dim black when disabled
ENTRY_BG         = "#FFFFFF"   # white input bg
ENTRY_FG         = "#000000"   # black typing
ENTRY_PLACEHOLDER= "#8A8A8A"   # gray placeholder
SELECTION_BG     = "#CCE0FF"
SELECTION_FG     = "#000000"
CARET_COLOR      = "#000000"

class SentimentAnalysisApp:
    # TODO(Ayinde): (Fetch Tweets Page UI Redesign): Improve UI/UX for tweet/sentiment page.
    def __init__(self, master):
        # window setup
        self.master = master
        self.master.title("Libra Technology: Sentiment Analysis")
        self.master.geometry("600x450")
        self.master.configure(bg=LIGHT_GRAY_BG)

        # main frame
        self.frame = tk.Frame(master, bg=LIGHT_GRAY_BG, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # title
        tk.Label(
            self.frame,
            text="Libra Technology: Movie Sentiment Analysis Tool",
            font=("Helvetica", 16, "bold"),
            bg=LIGHT_GRAY_BG,
            fg=BRAND_DARK_BLUE
        ).pack(pady=10)

        # keyword row (label + entry)
        keyword_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        keyword_frame.pack(pady=5)
        tk.Label(
            keyword_frame, text="Enter Movie Keyword:", font=("Arial", 12), bg=LIGHT_GRAY_BG
        ).pack(side=tk.LEFT, padx=5)

        self.placeholder_text = "e.g., Dune 2, Inside Out 2, Oppenheimer"
        self.keyword_entry = tk.Entry(keyword_frame, font=("Arial", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # entry accessibility: colors, caret, selection
        self.keyword_entry.configure(
            bg=ENTRY_BG,
            fg=ENTRY_FG,
            insertbackground=CARET_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG
        )
        # show placeholder initially
        self._set_entry_placeholder()
        # wire focus handlers for placeholder logic
        self.keyword_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.keyword_entry.bind("<FocusOut>", self._on_entry_focus_out)

        # output text area + scrollbar
        text_frame = tk.Frame(self.frame)
        text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            height=12,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # make output box readable too
        self.output_text.configure(
            bg="#FFFFFF", fg="#111111",
            insertbackground=CARET_COLOR,
            selectbackground=SELECTION_BG,
            selectforeground=SELECTION_FG
        )

        # text tags for formatting and sentiment colors
        self.output_text.tag_configure("muted", foreground="#666666")
        self.output_text.tag_configure("pos", foreground="#1B5E20")
        self.output_text.tag_configure("neg", foreground="#E65100")
        self.output_text.tag_configure("title", font=("Arial", 12, "bold"))

        # buttons row
        btn_frame = tk.Frame(self.frame, bg=LIGHT_GRAY_BG)
        btn_frame.pack(pady=10)

        # high-contrast fetch button
        self.search_button = tk.Button(
            btn_frame,
            text="Fetch Tweets",
            command=self.open_fetch_tweets,
            font=("Arial", 12, "bold"),
            bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10, pady=5, highlightthickness=0
        )
        self.search_button.grid(row=0, column=0, padx=5)

        # high-contrast analyze button
        self.analysis_button = tk.Button(
            btn_frame,
            text="Analyze Sentiment",
            command=self.open_sentiment_analysis,
            font=("Arial", 12, "bold"),
            bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            disabledforeground=BTN_FG_DISABLED,
            padx=10, pady=5, highlightthickness=0
        )
        self.analysis_button.grid(row=0, column=1, padx=5)

        # keep tweets + quick sentiment tags
        self._tweets = []

    def _set_entry_placeholder(self):
        # put placeholder text and set gray color
        self.keyword_entry.delete(0, tk.END)
        self.keyword_entry.insert(0, self.placeholder_text)
        self.keyword_entry.config(fg=ENTRY_PLACEHOLDER)

    def _on_entry_focus_in(self, _event=None):
        # when focusing, if placeholder shown, clear and set black typing color
        if self.keyword_entry.get() == self.placeholder_text and self.keyword_entry.cget("fg") == ENTRY_PLACEHOLDER:
            self.keyword_entry.delete(0, tk.END)
            self.keyword_entry.config(fg=ENTRY_FG)

    def _on_entry_focus_out(self, _event=None):
        # when leaving, if empty, restore placeholder
        if not self.keyword_entry.get().strip():
            self._set_entry_placeholder()

    def append_output(self, output, tag=None):
        # TODO(Ayinde): Make sure output is user-friendly and clear.
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{ts}] ", "muted")
        self.output_text.insert(tk.END, output + "\n", tag if tag else ())
        self.output_text.see(tk.END)
        print(output)

    # ... (open_fetch_tweets and open_sentiment_analysis methods remain as stubs)

    def open_fetch_tweets(self):
        # TODO(Ben): (Backend Tweets/Sentiment API): Implement fetching tweets from DB/API and displaying in UI.
        kw = self.keyword_entry.get().strip()
        if not kw or (kw == self.placeholder_text and self.keyword_entry.cget("fg") == ENTRY_PLACEHOLDER):
            messagebox.showinfo("missing keyword", "type a movie keyword first.")
            return

        # dynamic ui: disable during fetch
        self.search_button.config(state=tk.DISABLED)
        self.analysis_button.config(state=tk.DISABLED)

        # clear old output and add section header
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"results for: {kw}\n", "title")
        self.output_text.insert(tk.END, "—" * max(10, len(kw) + 14) + "\n", "muted")

        # mock data (no api pulls)
        mock = [
            f"loved {kw}, cinematography was insane!",
            f"{kw} was mid tbh.",
            f"the soundtrack totally carried {kw}.",
            f"i'd rewatch {kw} just for the visuals.",
            f"{kw} pacing was boring at times."
        ]

        def classify(text):
            # tiny keyword-based sentiment
            t = text.lower()
            pos_keys = ["loved", "carried", "rewatch", "insane", "amazing", "great", "fire"]
            neg_keys = ["mid", "boring", "bad", "trash", "weak"]
            if any(k in t for k in pos_keys) and not any(k in t for k in neg_keys):
                return "pos"
            if any(k in t for k in neg_keys) and not any(k in t for k in pos_keys):
                return "neg"
            return "pos" if "!" in t else "neg"

        # render each tweet
        self._tweets = []
        for i, line in enumerate(mock, start=1):
            tag = classify(line)
            badge = "positive" if tag == "pos" else "negative"
            self.append_output(f"tweet {i} • {badge}", tag)
            self.append_output(f"  {line}")
            self.output_text.insert(tk.END, "-" * 40 + "\n", "muted")
            self._tweets.append((line, tag))

        self.append_output(f"fetched {len(self._tweets)} items", "muted")

        # re-enable ui after fetch
        self.search_button.config(state=tk.NORMAL)
        self.analysis_button.config(state=tk.NORMAL)

    def open_sentiment_analysis(self):
        # TODO(Ben): (Sentiment Analysis Logic): Implement logic to analyze sentiment and store/retrieve results in DB.
        # TODO(Testing Point-Anthony): (UI Integration): Ensure UI displays results from analysis.
        if not self._tweets:
            messagebox.showinfo("no data", "fetch tweets first.")
            return

        # dynamic ui: disable during analysis
        self.search_button.config(state=tk.DISABLED)
        self.analysis_button.config(state=tk.DISABLED)

        # compute simple summary
        pos = sum(1 for _, tag in self._tweets if tag == "pos")
        neg = sum(1 for _, tag in self._tweets if tag == "neg")
        total = max(1, pos + neg)
        score = round((pos - neg) / total, 2)

        # section header
        self.output_text.insert(tk.END, "\nAnalysis Summary:\n", "title")
        self.output_text.insert(tk.END, "—" * 16 + "\n", "muted")

        # numbers + verdict
        verdict = "Overall Positive" if score > 0 else "Overall Negative" if score < 0 else "mixed/neutral"
        verdict_tag = "pos" if score >= 0 else "neg"
        self.append_output(f"Positives={pos}, Negatives={neg}, Score={score}", verdict_tag)

        # simple ascii bar
        bar_len = 24
        pos_blocks = int((pos / total) * bar_len)
        bar = f"[{'▮' * pos_blocks}{'▯' * (bar_len - pos_blocks)}]  {int((pos/total)*100)}% positive"
        self.append_output(bar, "muted")

        # verdict line
        self.append_output(verdict, verdict_tag)

        # re-enable ui
        self.search_button.config(state=tk.NORMAL)
        self.analysis_button.config(state=tk.NORMAL)

# standard entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAnalysisApp(root)
    root.mainloop()
