"""
Genereert low-fidelity wireframes (PNG) van de twee hoofdschermen van het
dashboard, voor sectie 4.5 van het ontwerpdocument.

Draaien met:   python docs/make_wireframes.py
De PNG's komen in dezelfde map (docs/).
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # geen scherm nodig, we slaan alleen op
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUTPUT_DIR = Path(__file__).resolve().parent

# Wireframe-kleuren: bewust grijstinten, want een wireframe gaat over indeling.
LINE = "#666666"
FILL = "#ECECEC"
PLACEHOLDER = "#F6F6F6"
ACCENT = "#C0392B"  # alleen voor de rode falenmarkering


def new_canvas():
    """Maakt een leeg liggend vel met een coördinatenstelsel van 0..100."""
    figure, ax = plt.subplots(figsize=(8.5, 11))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.invert_yaxis()  # zo telt y van boven (0) naar beneden (100)
    ax.axis("off")
    return figure, ax


def box(ax, x, y, w, h, text="", *, fill=FILL, align="left", style="round", text_color="#333333", size=11):
    """Tekent één rechthoek met optioneel een label erin."""
    shape = FancyBboxPatch if style == "round" else Rectangle
    kwargs = {"boxstyle": "round,pad=0,rounding_size=0.6"} if style == "round" else {}
    ax.add_patch(shape((x, y), w, h, facecolor=fill, edgecolor=LINE, linewidth=1.2, **kwargs))
    if text:
        tx = x + 1.5 if align == "left" else x + w / 2
        ax.text(tx, y + h / 2, text, ha=align, va="center", color=text_color, fontsize=size)


def label(ax, x, y, text, *, size=11, weight="normal", color="#333333"):
    """Plaatst losse tekst (zonder kader)."""
    ax.text(x, y, text, ha="left", va="center", fontsize=size, weight=weight, color=color)


def sidebar(ax, active):
    """Tekent het linkermenu dat Streamlit automatisch toont, met het actieve scherm."""
    box(ax, 0, 0, 22, 100, fill="#F0F0F0", style="square")
    label(ax, 2, 6, "MENU", size=12, weight="bold")
    for index, name in enumerate(["Start", "Trendweergave", "Vergelijking"]):
        y = 14 + index * 7
        is_active = name == active
        box(ax, 2, y, 18, 5, name, fill="#D7D7D7" if is_active else "white",
            text_color="#000000", size=10)


def chart_placeholder(ax, x, y, w, h, caption, *, failure_line=False, legend=False):
    """Een grijs grafiekvlak met een onderschrift (de NFE-3 toelichting)."""
    box(ax, x, y, w, h, fill=PLACEHOLDER, style="square")
    ax.text(x + w / 2, y + h / 2, "[ grafiek ]", ha="center", va="center", color="#AAAAAA", fontsize=10)
    if failure_line:
        fx = x + w * 0.82
        ax.plot([fx, fx], [y + 1, y + h - 1], color=ACCENT, linestyle="--", linewidth=1.4)
        ax.text(fx, y - 0.8, "falenmoment", ha="center", va="bottom", color=ACCENT, fontsize=7)
    if legend:
        box(ax, x + w - 16, y + 1.5, 14, 6, "legenda:\nlager + faulttype", fill="white", size=7)
    ax.text(x, y + h + 2, caption, ha="left", va="center", color="#777777", fontsize=8)


def save(figure, name):
    path = OUTPUT_DIR / name
    figure.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Opgeslagen: {path}")


def build_trend_screen():
    """Wireframe van Scherm 1 — Trendweergave."""
    figure, ax = new_canvas()
    sidebar(ax, active="Trendweergave")

    label(ax, 26, 5, "Trendweergave", size=18, weight="bold")
    label(ax, 26, 10, "Bekijk hoe één lager slijt over zijn levensduur.", size=10, color="#777777")

    box(ax, 26, 14, 34, 5, "Belastingsconditie        ▾", fill="white")
    box(ax, 62, 14, 34, 5, "Lager        ▾", fill="white")
    box(ax, 26, 21, 70, 5, "(i)  Faulttype van dit lager: Outer race", fill="#E8F0FE")

    label(ax, 26, 29, "Trendverloop", size=13, weight="bold")
    chart_placeholder(ax, 26, 31, 70, 11, "RMS — gemiddeld trillingsniveau", failure_line=True)
    chart_placeholder(ax, 26, 47, 70, 11, "Kurtosis — pieken in het signaal", failure_line=True)
    chart_placeholder(ax, 26, 63, 70, 11, "Crest factor — verhouding piek/RMS", failure_line=True)

    label(ax, 26, 79, "Ruw trillingssignaal", size=13, weight="bold")
    box(ax, 26, 82, 70, 4, "Meetmoment (minuut)   ◀——●——▶", fill="white", size=9)
    chart_placeholder(ax, 26, 88, 70, 9, "Ruwe meting van het gekozen meetmoment")
    save(figure, "wireframe_scherm1_trendweergave.png")


def build_comparison_screen():
    """Wireframe van Scherm 2 — Vergelijkingsweergave."""
    figure, ax = new_canvas()
    sidebar(ax, active="Vergelijking")

    label(ax, 26, 5, "Vergelijkingsweergave", size=18, weight="bold")
    label(ax, 26, 10, "Vergelijk meerdere lagers onder dezelfde conditie.", size=10, color="#777777")

    box(ax, 26, 14, 70, 5, "Belastingsconditie        ▾", fill="white")
    box(ax, 26, 21, 70, 6, "Lagers om te vergelijken:  [ Bearing1_1 ✕ ] [ Bearing1_2 ✕ ]   ▾", fill="white", size=9)

    chart_placeholder(ax, 26, 31, 70, 16, "RMS — alle gekozen lagers, elk een eigen kleur", legend=True)
    chart_placeholder(ax, 26, 53, 70, 16, "Kurtosis — alle gekozen lagers", legend=True)
    chart_placeholder(ax, 26, 75, 70, 16, "Crest factor — alle gekozen lagers", legend=True)
    save(figure, "wireframe_scherm2_vergelijkingsweergave.png")


if __name__ == "__main__":
    build_trend_screen()
    build_comparison_screen()
