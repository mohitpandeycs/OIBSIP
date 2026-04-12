"""Trends page for the BMI Calculator GUI.

Displays BMI trend visualization using Matplotlib embedded in Tkinter,
with a line chart of BMI over time, category color bands, and
summary statistics cards.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from ..database.models import BMIRecord
from .styles import (
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, CATEGORY_COLORS,
    PADDING_XS, PADDING_SM, PADDING_MD, PADDING_LG, PADDING_XL,
)


class TrendsPage(tk.Frame):
    """Page displaying BMI trend charts and statistics.

    Attributes:
        app: Reference to the root BMIApp instance for shared state.
    """

    def __init__(self, parent: tk.Widget, app: "BMIApp") -> None:
        super().__init__(parent)
        self.app = app
        self._build_ui()
        self.apply_theme()

    def _build_ui(self) -> None:
        """Build all trends page UI components."""
        self._container = tk.Frame(self)
        self._container.pack(fill=tk.BOTH, expand=True, padx=PADDING_XL, pady=PADDING_XL)

        # ── Header ────────────────────────────────────────────────────
        self._header_label = tk.Label(
            self._container, text="📈 BMI Trends", font=FONT_TITLE, anchor="w",
        )
        self._header_label.pack(fill=tk.X, pady=(0, PADDING_MD))

        # ── Statistics Cards ───────────────────────────────────────────
        self._stats_frame = tk.Frame(self._container)
        self._stats_frame.pack(fill=tk.X, pady=(0, PADDING_LG))

        self._stat_labels: dict[str, tk.Label] = {}
        self._stat_cards: list[tk.Frame] = []
        stat_items = ["Average BMI", "Min BMI", "Max BMI", "Records", "Trend"]

        for item in stat_items:
            card = tk.Frame(self._stats_frame, padx=PADDING_MD, pady=PADDING_MD)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING_SM))

            title_lbl = tk.Label(card, text=item, font=FONT_SMALL, anchor="center")
            title_lbl.pack(fill=tk.X)

            value_lbl = tk.Label(card, text="--", font=FONT_HEADING, anchor="center")
            value_lbl.pack(fill=tk.X, pady=(PADDING_XS, 0))

            self._stat_labels[item] = value_lbl
            self._stat_cards.append(card)

        # ── Chart Area ─────────────────────────────────────────────────
        self._chart_frame = tk.Frame(self._container)
        self._chart_frame.pack(fill=tk.BOTH, expand=True)

        self._chart_placeholder = tk.Label(
            self._chart_frame,
            text="📊 Select a user and add records to see trends",
            font=FONT_HEADING,
            anchor="center",
        )

        # ── No User Message ───────────────────────────────────────────
        self._no_user_label = tk.Label(
            self,
            text="👤 Please select a user from the Dashboard to view trends.",
            font=FONT_HEADING,
            anchor="center",
        )

    # ── Chart Rendering ───────────────────────────────────────────────

    def _render_chart(self) -> None:
        """Render the BMI trend chart using Matplotlib."""
        if not self.app.current_user:
            return

        records = self.app.db.get_user_records(self.app.current_user.user_id)
        if len(records) < 2:
            self._chart_placeholder.pack(fill=tk.BOTH, expand=True)
            self._chart_placeholder.configure(
                text="📊 Need at least 2 records to show trends"
            )
            return

        self._chart_placeholder.pack_forget()

        try:
            import matplotlib
            matplotlib.use("TkAgg")
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            import matplotlib.dates as mdates
        except ImportError:
            self._chart_placeholder.pack(fill=tk.BOTH, expand=True)
            self._chart_placeholder.configure(
                text="Matplotlib is required for charts.\nInstall with: pip install matplotlib"
            )
            return

        # Clear previous chart
        for widget in self._chart_frame.winfo_children():
            widget.destroy()

        # Prepare data (records are DESC, we need ASC for the chart)
        records_asc = list(reversed(records))
        dates = []
        bmis = []
        for rec in records_asc:
            try:
                dt = datetime.fromisoformat(rec.timestamp)
                dates.append(dt)
            except (ValueError, TypeError):
                continue
            bmis.append(rec.bmi)

        if len(dates) < 2:
            self._chart_placeholder.pack(fill=tk.BOTH, expand=True)
            self._chart_placeholder.configure(text="Not enough valid data to plot")
            return

        # Create figure
        p = self.app.theme.palette
        fig = Figure(figsize=(8, 4.5), dpi=100, facecolor=p.bg_primary)
        ax = fig.add_subplot(111)
        ax.set_facecolor(p.bg_card)

        # Category bands
        ax.axhspan(0, 18.5, alpha=0.12, color=CATEGORY_COLORS["Underweight"])
        ax.axhspan(18.5, 25.0, alpha=0.12, color=CATEGORY_COLORS["Normal"])
        ax.axhspan(25.0, 30.0, alpha=0.12, color=CATEGORY_COLORS["Overweight"])
        ax.axhspan(30.0, max(bmis) + 5, alpha=0.12, color=CATEGORY_COLORS["Obese"])

        # Category boundary lines
        for boundary, label in [(18.5, "Underweight"), (25.0, "Normal"), (30.0, "Overweight")]:
            ax.axhline(y=boundary, color=p.fg_muted, linestyle="--", linewidth=0.8, alpha=0.6)
            ax.text(dates[0], boundary + 0.3, label, color=p.fg_muted, fontsize=8, alpha=0.8)

        # Plot BMI line
        ax.plot(dates, bmis, color=p.accent, linewidth=2.5, marker="o", markersize=6,
                markerfacecolor=p.accent, markeredgecolor=p.fg_primary, markeredgewidth=1.5)

        # Fill area under curve
        ax.fill_between(dates, bmis, alpha=0.15, color=p.accent)

        # Styling
        ax.set_xlabel("Date", color=p.fg_secondary, fontsize=11)
        ax.set_ylabel("BMI", color=p.fg_secondary, fontsize=11)
        ax.set_title(f"BMI Trend — {self.app.current_user.name}",
                     color=p.fg_primary, fontsize=14, fontweight="bold", pad=12)
        ax.tick_params(colors=p.fg_muted, labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(p.border)
        ax.spines["left"].set_color(p.border)

        # Format x-axis dates
        fig.autofmt_xdate()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

        fig.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self._chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ── Statistics Update ──────────────────────────────────────────────

    def _update_statistics(self) -> None:
        """Update the statistics cards with current user data."""
        if not self.app.current_user:
            for lbl in self._stat_labels.values():
                lbl.configure(text="--")
            return

        stats = self.app.db.get_bmi_statistics(self.app.current_user.user_id)

        self._stat_labels["Average BMI"].configure(text=f"{stats['average_bmi']:.1f}")
        self._stat_labels["Min BMI"].configure(text=f"{stats['min_bmi']:.1f}")
        self._stat_labels["Max BMI"].configure(text=f"{stats['max_bmi']:.1f}")
        self._stat_labels["Records"].configure(text=str(stats["total_records"]))

        trend = stats["trend_direction"]
        trend_icons = {"improving": "📉 Improving", "declining": "📈 Declining", "stable": "➡ Stable"}
        self._stat_labels["Trend"].configure(text=trend_icons.get(trend, trend))

    # ── Public Methods ────────────────────────────────────────────────

    def refresh(self) -> None:
        """Refresh the page data (called on page switch)."""
        if self.app.current_user:
            self._no_user_label.pack_forget()
            self._container.pack(fill=tk.BOTH, expand=True)
            self._update_statistics()
            self._render_chart()
        else:
            self._container.pack_forget()
            self._no_user_label.pack(fill=tk.BOTH, expand=True, padx=PADDING_XL, pady=PADDING_XL)

    def apply_theme(self) -> None:
        """Apply the current theme to all trends page widgets."""
        p = self.app.theme.palette

        self.configure(bg=p.bg_primary)
        self._container.configure(bg=p.bg_primary)
        self._header_label.configure(bg=p.bg_primary, fg=p.fg_primary)
        self._chart_placeholder.configure(bg=p.bg_primary, fg=p.fg_muted)
        self._no_user_label.configure(bg=p.bg_primary, fg=p.fg_muted)

        self._stats_frame.configure(bg=p.bg_primary)
        for card in self._stat_cards:
            card.configure(bg=p.bg_card, highlightbackground=p.card_border,
                           highlightthickness=1)
            for child in card.winfo_children():
                if isinstance(child, tk.Label):
                    if child in self._stat_labels.values():
                        child.configure(bg=p.bg_card, fg=p.accent)
                    else:
                        child.configure(bg=p.bg_card, fg=p.fg_secondary)