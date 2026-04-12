"""History page for the BMI Calculator GUI.

Displays a scrollable table of BMI records for the current user
with date filtering, record deletion, and CSV export functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from ..database.models import BMIRecord
from .styles import (
    FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL,
    FONT_BUTTON, FONT_INPUT, CATEGORY_COLORS,
    PADDING_XS, PADDING_SM, PADDING_MD, PADDING_LG, PADDING_XL,
)


class HistoryPage(tk.Frame):
    """Page displaying historical BMI records for the current user.

    Attributes:
        app: Reference to the root BMIApp instance for shared state.
    """

    def __init__(self, parent: tk.Widget, app: "BMIApp") -> None:
        super().__init__(parent)
        self.app = app
        self._build_ui()
        self.apply_theme()

    def _build_ui(self) -> None:
        """Build all history page UI components."""
        self._container = tk.Frame(self)
        self._container.pack(fill=tk.BOTH, expand=True, padx=PADDING_XL, pady=PADDING_XL)

        # ── Header ────────────────────────────────────────────────────
        header_frame = tk.Frame(self._container)
        header_frame.pack(fill=tk.X, pady=(0, PADDING_MD))

        self._header_label = tk.Label(
            header_frame, text="📋 BMI History", font=FONT_TITLE, anchor="w",
        )
        self._header_label.pack(side=tk.LEFT)

        # ── Filter Bar ────────────────────────────────────────────────
        filter_card = tk.Frame(self._container)
        filter_card.pack(fill=tk.X, pady=(0, PADDING_MD))

        self._filter_label = tk.Label(
            filter_card, text="📅 Filter by Date:", font=FONT_BODY_BOLD, anchor="w",
        )
        self._filter_label.pack(side=tk.LEFT, padx=(0, PADDING_MD))

        self._from_label = tk.Label(
            filter_card, text="From:", font=FONT_BODY, anchor="w",
        )
        self._from_label.pack(side=tk.LEFT, padx=(0, PADDING_XS))

        self._from_entry = tk.Entry(filter_card, font=FONT_INPUT, width=12)
        self._from_entry.pack(side=tk.LEFT, padx=(0, PADDING_SM))

        self._to_label = tk.Label(
            filter_card, text="To:", font=FONT_BODY, anchor="w",
        )
        self._to_label.pack(side=tk.LEFT, padx=(PADDING_SM, PADDING_XS))

        self._to_entry = tk.Entry(filter_card, font=FONT_INPUT, width=12)
        self._to_entry.pack(side=tk.LEFT, padx=(0, PADDING_MD))

        self._filter_btn = tk.Button(
            filter_card, text="Apply", font=FONT_SMALL, cursor="hand2",
            command=self._apply_filter,
        )
        self._filter_btn.pack(side=tk.LEFT, padx=(0, PADDING_SM))

        self._clear_filter_btn = tk.Button(
            filter_card, text="Clear", font=FONT_SMALL, cursor="hand2",
            command=self._clear_filter,
        )
        self._clear_filter_btn.pack(side=tk.LEFT)

        self._export_btn = tk.Button(
            filter_card, text="📁 Export CSV", font=FONT_SMALL, cursor="hand2",
            command=self._export_csv,
        )
        self._export_btn.pack(side=tk.RIGHT)

        # ── Treeview Table ────────────────────────────────────────────
        table_frame = tk.Frame(self._container)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("date", "weight", "height", "bmi", "category")
        self._tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse",
            height=15,
        )

        self._tree.heading("date", text="Date")
        self._tree.heading("weight", text="Weight (kg)")
        self._tree.heading("height", text="Height (m)")
        self._tree.heading("bmi", text="BMI")
        self._tree.heading("category", text="Category")

        self._tree.column("date", width=180, anchor=tk.W)
        self._tree.column("weight", width=110, anchor=tk.CENTER)
        self._tree.column("height", width=110, anchor=tk.CENTER)
        self._tree.column("bmi", width=90, anchor=tk.CENTER)
        self._tree.column("category", width=130, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ── Delete Button ─────────────────────────────────────────────
        btn_frame = tk.Frame(self._container)
        btn_frame.pack(fill=tk.X, pady=(PADDING_MD, 0))

        self._delete_btn = tk.Button(
            btn_frame, text="🗑  Delete Selected", font=FONT_BUTTON, cursor="hand2",
            command=self._delete_selected,
        )
        self._delete_btn.pack(side=tk.LEFT)

        # ── No User Message ───────────────────────────────────────────
        self._no_user_label = tk.Label(
            self, text="👤 Please select a user from the Dashboard to view history.",
            font=FONT_HEADING, anchor="center",
        )

    # ── Data Loading ──────────────────────────────────────────────────

    def _load_records(self, start_date: str = None, end_date: str = None) -> None:
        """Load BMI records from the database into the treeview."""
        for item in self._tree.get_children():
            self._tree.delete(item)

        if not self.app.current_user:
            return

        records = self.app.db.get_user_records(
            self.app.current_user.user_id, start_date=start_date, end_date=end_date,
        )

        for rec in records:
            try:
                dt = datetime.fromisoformat(rec.timestamp)
                display_date = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                display_date = rec.timestamp

            tag = rec.category.lower()
            self._tree.insert("", tk.END, iid=str(rec.record_id), values=(
                display_date,
                f"{rec.weight_kg:.1f}",
                f"{rec.height_m:.2f}",
                f"{rec.bmi:.2f}",
                rec.category,
            ), tags=(tag,))

        for cat, color in CATEGORY_COLORS.items():
            self._tree.tag_configure(cat.lower(), foreground=color)

    # ── Event Handlers ────────────────────────────────────────────────

    def _apply_filter(self) -> None:
        start = self._from_entry.get().strip() or None
        end = self._to_entry.get().strip() or None
        self._load_records(start_date=start, end_date=end)

    def _clear_filter(self) -> None:
        self._from_entry.delete(0, tk.END)
        self._to_entry.delete(0, tk.END)
        self._load_records()

    def _delete_selected(self) -> None:
        selected = self._tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a record to delete.")
            return

        record_id = int(selected[0])
        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this BMI record?",
        )
        if confirm:
            self.app.db.delete_record(record_id)
            self._load_records()

    def _export_csv(self) -> None:
        if not self.app.current_user:
            messagebox.showwarning("No User", "Please select a user first.")
            return

        from ..utils.export import CSVExporter

        records = self.app.db.get_user_records(self.app.current_user.user_id)
        if not records:
            messagebox.showinfo("No Data", "No records to export.")
            return

        filepath = CSVExporter.export(records, self.app.current_user.name)
        if filepath:
            messagebox.showinfo("Exported", f"Records exported to:\n{filepath}")
        else:
            messagebox.showwarning("Cancelled", "Export was cancelled.")

    # ── Public Methods ────────────────────────────────────────────────

    def refresh(self) -> None:
        if self.app.current_user:
            self._no_user_label.pack_forget()
            self._container.pack(fill=tk.BOTH, expand=True)
            self._load_records()
        else:
            self._container.pack_forget()
            self._no_user_label.pack(fill=tk.BOTH, expand=True, padx=PADDING_XL, pady=PADDING_XL)

    def apply_theme(self) -> None:
        p = self.app.theme.palette

        self.configure(bg=p.bg_primary)
        self._container.configure(bg=p.bg_primary)
        self._header_label.configure(bg=p.bg_primary, fg=p.fg_primary)
        self._no_user_label.configure(bg=p.bg_primary, fg=p.fg_muted)

        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background=p.bg_card,
                         foreground=p.fg_primary,
                         fieldbackground=p.bg_card,
                         font=FONT_BODY,
                         rowheight=32,
                         borderwidth=0)
        style.configure("Treeview.Heading",
                         background=p.bg_secondary,
                         foreground=p.fg_primary,
                         font=FONT_BODY_BOLD,
                         borderwidth=0)
        style.map("Treeview",
                   background=[("selected", p.accent)],
                   foreground=[("selected", "#FFFFFF")])
        style.map("Treeview.Heading",
                   background=[("active", p.bg_card)])

        # Walk through container children for theming
        for widget in self._container.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=p.bg_primary)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=p.bg_primary, fg=p.fg_secondary)
                    elif isinstance(child, tk.Button):
                        child.configure(bg=p.bg_card, fg=p.fg_primary,
                                        activebackground=p.accent_hover, bd=0)
                    elif isinstance(child, tk.Entry):
                        child.configure(bg=p.bg_input, fg=p.fg_primary,
                                        insertbackground=p.fg_primary,
                                        relief=tk.FLAT,
                                        highlightbackground=p.input_border,
                                        highlightthickness=1,
                                        highlightcolor=p.input_focus)