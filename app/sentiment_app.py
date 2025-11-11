import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .fetch_tweets import fetch_tweets_for_ui
from .analyze_sentiment import analyze_tweets
from .ui_theme import (
    COLORS,
    FONTS,
    apply_placeholder,
    configure_root_window,
    create_accent_bar,
    create_glass_card,
    create_input,
    create_neon_button,
    get_entry_value,
    hero_subtitle,
    hero_title,
    info_chip,
)


class SentimentAnalysisApp:
    """Command center for fetching tweets and visualizing sentiment."""

    def __init__(self, master):
        self.master = master
        configure_root_window(
            self.master,
            "Libra Technologies · Sentiment Radar",
            size="1200x840",
        )

        self.current_tweets = []
        self.current_keyword = ""

        surface = tk.Frame(self.master, bg=COLORS["bg"], padx=70, pady=50)
        surface.pack(fill="both", expand=True)

        card = create_glass_card(surface)
        card.pack(expand=True, fill="both")

        header = tk.Frame(card, bg=COLORS["card"])
        header.pack(fill="x")
        hero_title(header, "Sentiment Radar").pack(anchor="w")
        hero_subtitle(
            header,
            "Scan live Twitter chatter for any title or topic.",
            muted=False,
        ).pack(anchor="w")
        create_accent_bar(header).pack(anchor="w", pady=(10, 0))

        control = tk.Frame(card, bg=COLORS["card"])
        control.pack(fill="x", pady=(24, 12))

        tk.Label(
            control,
            text="KEYWORD OR TITLE",
            font=("Inter", 11, "bold"),
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="w")
        keyword_row = tk.Frame(control, bg=COLORS["card"])
        keyword_row.pack(fill="x", pady=(6, 0))

        self.keyword_entry = create_input(keyword_row, width=38)
        self.keyword_entry.pack(side=tk.LEFT, fill="x", expand=True)
        apply_placeholder(self.keyword_entry, "e.g. Dune Part Two trailer", is_password=False)

        self.combined_button = create_neon_button(keyword_row, "Deploy Scan", self.fetch_and_analyze)
        self.combined_button.pack(side=tk.LEFT, padx=(12, 0))

        console_frame = tk.Frame(card, bg=COLORS["card"])
        console_frame.pack(fill="both", expand=True, pady=(20, 0))

        scrollbar = tk.Scrollbar(console_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            console_frame,
            wrap=tk.WORD,
            font=FONTS["mono"],
            bg=COLORS["console_bg"],
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            insertbackground=COLORS["text_primary"],
            yscrollcommand=scrollbar.set,
        )
        self.output_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.output_text.yview)

        self.output_text.tag_config("pos", foreground=COLORS["success"], font=FONTS["mono"])
        self.output_text.tag_config("neg", foreground=COLORS["danger"], font=FONTS["mono"])
        self.output_text.tag_config("title", foreground=COLORS["cyan"], font=("Inter", 12, "bold"))
        self.output_text.tag_config("muted", foreground=COLORS["text_secondary"], font=FONTS["mono"])

        helper = tk.Label(
            card,
            text="Tip: short, specific keywords return the sharpest signal. Re-run scans anytime.",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
        )
        helper.pack(fill="x", pady=(14, 4))
        info_chip(card, "Data refreshes on every scan · Results stay local to your machine").pack(anchor="w", pady=(0, 4))

        self.chart_frame = tk.Frame(card, bg=COLORS["card"])
        self.chart_frame.pack(fill="x", pady=(10, 0))
        self.chart_canvas: Optional[FigureCanvasTkAgg] = None
        self._render_chart({"Positive": 0, "Negative": 0, "Neutral": 0})

    def append_output(self, output: str, tag=None):
        """Append text to the console and mirror it to stdout for logging."""
        self.output_text.insert(tk.END, output + "\n", tag)
        self.output_text.see(tk.END)
        print(output)

    def fetch_and_analyze(self):
        """Fetch tweets and immediately analyze their sentiment."""
        self.output_text.delete("1.0", tk.END)

        keyword = get_entry_value(self.keyword_entry).strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword before proceeding.")
            return

        self._set_button_state(disabled=True)
        self.append_output("≡ INITIALIZING RADAR ≡", "title")

        self.append_output(f'\n🔍 Deploying sweep for "{keyword}"…', "muted")
        try:
            result = fetch_tweets_for_ui(keyword, count=10)
            tweets = result.get("tweets", [])

            if not result.get("success") or not tweets:
                self.append_output("Scan returned no usable tweets. Refine your keyword and retry.", "neg")
                self._set_button_state(disabled=False)
                return

            self.current_tweets = tweets
            self.current_keyword = keyword
            self.append_output(f"Inbound stream established: {len(tweets)} tweets pulled.", "pos")

        except Exception as e:
            self.append_output(f"Scan error: {e}", "neg")
            messagebox.showerror("Fetch Error", f"Failed to fetch tweets: {e}")
            self._set_button_state(disabled=False)
            return

        self.append_output(f"\n🎬 Parsing sentiment for {len(self.current_tweets)} tweets…", "muted")
        analysis_result = None
        try:
            analysis_result = analyze_tweets(self.current_tweets, self.current_keyword)

            if not analysis_result.get("success"):
                self.append_output(f"Analysis failed: {analysis_result.get('message', 'Unknown error')}", "neg")
                self._set_button_state(disabled=False)
                return

            self.append_output("\n🔬 MICRO VIEW (TWEET DETAIL)", "title")

            for i, detail in enumerate(analysis_result.get("detailed_results", [])):
                tweet_number = i + 1
                sentiment = detail["sentiment"]
                score = detail["score"]
                raw_text = detail["text"]
                cleaned_text = detail["cleaned_text"]
                matched_words = detail.get("matched_words", [])
                matched_set = set(matched_words)

                sentiment_tag = "pos" if sentiment == "Positive" else "neg" if sentiment == "Negative" else "muted"

                self.output_text.insert(
                    tk.END,
                    f"Tweet {tweet_number} ({sentiment}, Score: {score}):\n",
                    sentiment_tag,
                )
                self.output_text.insert(tk.END, f"  RAW: {raw_text}\n", "muted")

                self.output_text.insert(tk.END, "  WORDS: ")
                cleaned_tokens = cleaned_text.split()

                for word in cleaned_tokens:
                    if word in matched_set:
                        if sentiment == "Positive":
                            self.output_text.insert(tk.END, f"{word} ", "pos")
                        elif sentiment == "Negative":
                            self.output_text.insert(tk.END, f"{word} ", "neg")
                        else:
                            self.output_text.insert(tk.END, f"{word} ", "muted")
                    else:
                        self.output_text.insert(tk.END, f"{word} ", "muted")

                details = detail.get("matched_word_details") or []
                if details:
                    detail_line = ", ".join(f"{d['token']}({d['score']})" for d in details)
                    self.output_text.insert(tk.END, f"\n  SCORED: {detail_line}", "muted")

                self.output_text.insert(tk.END, "\n" + "—" * 50 + "\n", "muted")

            counts = analysis_result.get("sentiment_counts", {})
            pos = counts.get("Positive", 0)
            neg = counts.get("Negative", 0)
            neutral = counts.get("Neutral", 0)
            total = pos + neg + neutral

            score = round((pos - neg) / max(1, total), 2)
            verdict_tag = "pos" if score > 0 else "neg" if score < 0 else "muted"

            self.append_output("\n📊 RADAR SUMMARY", "title")
            self.append_output(f"Total Signals Analyzed: {total}", "muted")
            self.append_output(f"Positive Mentions: {pos}", "pos")
            self.append_output(f"Negative Mentions: {neg}", "neg")
            self.append_output(f"Net Sentiment Score: {score}", verdict_tag)
            self.output_text.insert(tk.END, "—" * 50 + "\n", "muted")
            self._render_chart({"Positive": pos, "Negative": neg, "Neutral": neutral})

        except Exception as e:
            self.append_output(f"Analysis error: {e}", "neg")
            messagebox.showerror("Analysis Error", f"Failed to analyze or display sentiment: {e}")

        finally:
            self.append_output("\n≡ RADAR CYCLE COMPLETE ≡", "title")
            self._set_button_state(disabled=False)

    def _set_button_state(self, disabled: bool) -> None:
        if disabled:
            self.combined_button.config(state=tk.DISABLED, fg=COLORS["text_secondary"], bg=COLORS["card_muted"])
            self.combined_button._hover_colors = (COLORS["card_muted"], COLORS["card_muted"])  # type: ignore[attr-defined]
        else:
            self.combined_button.config(state=tk.NORMAL, fg=COLORS["bg"], bg=COLORS["teal"])
            self.combined_button._hover_colors = (COLORS["teal"], COLORS["teal_hover"])  # type: ignore[attr-defined]

    def _render_chart(self, counts: Dict[str, int]) -> None:
        """Render or update the sentiment distribution chart."""
        labels = ["Positive", "Neutral", "Negative"]
        values = [counts.get("Positive", 0), counts.get("Neutral", 0), counts.get("Negative", 0)]
        colors = [COLORS["success"], COLORS["cyan"], COLORS["danger"]]

        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        fig = Figure(figsize=(4.8, 2.4), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(labels, values, color=colors)
        max_value = max(values)
        ax.set_ylim(0, max(1, max_value * 1.25 if max_value else 1))

        ax.set_title("Sentiment Distribution", color=COLORS["text_primary"], fontsize=11, pad=12)
        ax.tick_params(axis="x", colors=COLORS["text_secondary"])
        ax.tick_params(axis="y", colors=COLORS["text_secondary"])
        ax.set_facecolor(COLORS["card"])
        fig.patch.set_facecolor(COLORS["card"])

        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (max_value * 0.05 if max_value else 0.1),
                str(value),
                ha="center",
                color=COLORS["text_primary"],
                fontsize=10,
            )

        fig.tight_layout()
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="x", expand=False)
