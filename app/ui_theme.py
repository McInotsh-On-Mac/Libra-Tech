"""Shared UI helpers for the Libra Technologies Tkinter experience."""

import tkinter as tk
from typing import Dict, Optional, Tuple

# Brand palette inspired by Libra logo
COLORS: Dict[str, str] = {
    "bg": "#020712",
    "bg_alt": "#07142b",
    "card": "#0c1e3a",
    "card_muted": "#122a4f",
    "border": "#133a7c",
    "teal": "#20e3b2",
    "teal_hover": "#13b692",
    "cyan": "#14cfe0",
    "magenta": "#3947ff",
    "text_primary": "#f5f8ff",
    "text_secondary": "#9bb5d8",
    "danger": "#ff7b9c",
    "success": "#3dd598",
    "console_bg": "#050d1f",
}

FONTS = {
    "display": ("SF Pro Display", 26, "bold"),
    "headline": ("SF Pro Display", 18, "bold"),
    "body": ("Inter", 12),
    "button": ("Inter", 12, "bold"),
    "mono": ("JetBrains Mono", 11),
}


def configure_root_window(root: tk.Tk, title: str, size: str = "1100x760") -> None:
    root.title(title)
    root.geometry(size)
    root.configure(bg=COLORS["bg"])
    root.minsize(900, 640)


def create_glass_card(master: tk.Misc, padding: Tuple[int, int] = (40, 40)) -> tk.Frame:
    frame = tk.Frame(master, bg=COLORS["card"], padx=padding[0], pady=padding[1])
    frame.configure(highlightthickness=1, highlightbackground=COLORS["border"], bd=0)
    return frame


def create_neon_button(master: tk.Misc, text: str, command, primary: bool = True) -> tk.Button:
    if primary:
        bg = COLORS["teal"]
        hover = COLORS["teal_hover"]
        fg = COLORS["bg"]
    else:
        bg = COLORS["card_muted"]
        hover = COLORS["border"]
        fg = COLORS["text_primary"]

    btn = tk.Button(
        master,
        text=text,
        command=command,
        font=FONTS["button"],
        bg=bg,
        fg=fg,
        activebackground=hover,
        activeforeground=fg,
        relief=tk.FLAT,
        bd=0,
        padx=24,
        pady=12,
        cursor="hand2",
    )
    _add_hover_state(btn, bg, hover)
    return btn


def _add_hover_state(widget: tk.Widget, normal: str, hover: str) -> None:
    widget._hover_colors = (normal, hover)  # type: ignore[attr-defined]

    def _enter(_event):
        widget.configure(bg=widget._hover_colors[1])  # type: ignore[attr-defined]

    def _leave(_event):
        widget.configure(bg=widget._hover_colors[0])  # type: ignore[attr-defined]

    widget.bind("<Enter>", _enter)
    widget.bind("<Leave>", _leave)


def create_input(
    master: tk.Misc,
    width: Optional[int] = None,
    show: Optional[str] = None,
    full_width: bool = False,
) -> tk.Entry:
    resolved = width if width is not None else (1 if full_width else 32)
    entry = tk.Entry(
        master,
        width=resolved,
        font=FONTS["body"],
        bg=COLORS["console_bg"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["text_primary"],
        relief=tk.FLAT,
        bd=0,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["teal"],
        disabledbackground=COLORS["card_muted"],
        disabledforeground=COLORS["text_secondary"],
    )
    if show:
        entry.config(show=show)
    return entry


def apply_placeholder(entry: tk.Entry, text: str, *, is_password: bool = False, mask: str = "•") -> None:
    if getattr(entry, "_placeholder_initialized", False):
        return

    default_fg = entry.cget("fg")
    placeholder_fg = COLORS["text_secondary"]
    entry.insert(0, text)
    entry.config(fg=placeholder_fg)

    original_show = entry.cget("show")
    mask_char = original_show or mask
    if is_password:
        entry.config(show="")

    entry._placeholder_initialized = True  # type: ignore[attr-defined]
    entry._placeholder_text = text  # type: ignore[attr-defined]
    entry._placeholder_fg = default_fg  # type: ignore[attr-defined]
    entry._placeholder_is_password = is_password  # type: ignore[attr-defined]
    entry._placeholder_mask = mask_char  # type: ignore[attr-defined]
    entry._placeholder_active = True  # type: ignore[attr-defined]

    def _on_focus_in(_event):
        if entry._placeholder_active:  # type: ignore[attr-defined]
            entry.delete(0, tk.END)
            entry.config(fg=default_fg)
            if is_password:
                entry.config(show=mask_char)
            entry._placeholder_active = False  # type: ignore[attr-defined]

    def _on_focus_out(_event):
        ensure_placeholder(entry)

    entry.bind("<FocusIn>", _on_focus_in, add="+")
    entry.bind("<FocusOut>", _on_focus_out, add="+")


def ensure_placeholder(entry: tk.Entry) -> None:
    text = getattr(entry, "_placeholder_text", None)
    if text is None or entry.get():
        return
    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.config(fg=COLORS["text_secondary"])
    if getattr(entry, "_placeholder_is_password", False):
        entry.config(show="")
    entry._placeholder_active = True  # type: ignore[attr-defined]


def clear_placeholder(entry: tk.Entry) -> None:
    if getattr(entry, "_placeholder_active", False):
        entry.delete(0, tk.END)
        entry.config(fg=getattr(entry, "_placeholder_fg", entry.cget("fg")))
        if getattr(entry, "_placeholder_is_password", False):
            entry.config(show=getattr(entry, "_placeholder_mask", "•"))
        entry._placeholder_active = False  # type: ignore[attr-defined]


def get_entry_value(entry: tk.Entry) -> str:
    if getattr(entry, "_placeholder_active", False):
        return ""
    return entry.get()


def create_logo_badge(master: tk.Misc, size: int = 130, background: Optional[str] = None) -> tk.Canvas:
    bg = background or COLORS["card"]
    canvas = tk.Canvas(master, width=size, height=size, bg=bg, highlightthickness=0, bd=0)
    padding = 6
    canvas.create_oval(padding, padding, size - padding, size - padding, fill=COLORS["magenta"], outline="")
    canvas.create_arc(padding, padding, size - padding, size - padding, start=90, extent=180, fill=COLORS["teal"], outline="")
    canvas.create_text(size // 2, size // 2, text="L", font=("SF Pro Display", int(size * 0.45), "bold"), fill=COLORS["text_primary"])
    return canvas


def hero_title(master: tk.Misc, text: str) -> tk.Label:
    return tk.Label(master, text=text, font=FONTS["display"], bg=master["bg"], fg=COLORS["text_primary"])


def hero_subtitle(master: tk.Misc, text: str, muted: bool = False) -> tk.Label:
    color = COLORS["text_secondary"] if muted else COLORS["cyan"]
    return tk.Label(master, text=text, font=("Inter", 13), bg=master["bg"], fg=color)


def info_chip(master: tk.Misc, text: str) -> tk.Label:
    return tk.Label(
        master,
        text=text,
        font=("Inter", 11),
        bg=COLORS["card_muted"],
        fg=COLORS["text_primary"],
        padx=14,
        pady=8,
        bd=0,
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
    )


def status_label(master: tk.Misc) -> tk.Label:
    return tk.Label(master, text="", font=FONTS["body"], bg=master["bg"], fg=COLORS["text_secondary"])


def create_accent_bar(master: tk.Misc, width: int = 240, height: int = 4) -> tk.Canvas:
    canvas = tk.Canvas(master, width=width, height=height, bg=master["bg"], highlightthickness=0, bd=0)
    gradient = [COLORS["magenta"], COLORS["cyan"], COLORS["teal"]]
    segment = width / len(gradient)
    for idx, color in enumerate(gradient):
        canvas.create_rectangle(int(idx * segment), 0, int((idx + 1) * segment), height, fill=color, outline="")
    return canvas
