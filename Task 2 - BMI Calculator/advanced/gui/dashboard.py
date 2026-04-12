"""Dashboard page for the BMI Calculator GUI.

Contains the main BMI calculation form with user selection,
weight/height inputs, validation, result display with color-coded
category, and save-to-database functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from ..core.bmi_engine import BMIEngine, BMIResult
from ..core.validators import InputValidator
from ..database.models import UserRecord
from .styles import (
    Theme, FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY,
    FONT_BODY_BOLD, FONT_SMALL, FONT_BUTTON, FONT_INPUT,
    FONT_DISPLAY, FONT_DISPLAY_CATEGORY, CATEGORY_COLORS,
    PADDING_XS, PADDING_SM, PADDING_MD, PADDING_LG, PADDING_XL,
    CARD_PADDING,
)


class DashboardPage(tk.Frame):
    """Main dashboard page with BMI calculation form and result display.

    Attributes:
        app: Reference to the root BMIApp instance for shared state.
    """

    def __init__(self, parent: tk.Widget, app: "BMIApp") -> None:
        """Initialize the dashboard page.

        Args:
            parent: Parent widget to pack into.
            app: Reference to the root BMIApp for shared state access.
        """
        super().__init__(parent)
        self.app = app
        self._last_result: Optional[BMIResult] = None

        self._build_ui()
        self.apply_theme()

    def _build_ui(self) -> None:
        """Build all dashboard UI components."""
        # Main container with padding
        self._container = tk.Frame(self)
        self._container.pack(fill=tk.BOTH, expand=True, padx=PADDING_XL, pady=PADDING_XL)

        # ── Header ────────────────────────────────────────────────────
        self._header_label = tk.Label(
            self._container, text="BMI Calculator", font=FONT_TITLE, anchor="w",
        )
        self._header_label.pack(fill=tk.X, pady=(0, PADDING_LG))

        # ── Content Grid ──────────────────────────────────────────────
        self._content_frame = tk.Frame(self._container)
        self._content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Input Form
        self._build_input_form(self._content_frame)

        # Right: Result Display
        self._build_result_display(self._content_frame)

    def _build_input_form(self, parent: tk.Widget) -> None:
        """Build the input form section (left side)."""
        self._form_card = tk.Frame(parent)
        self._form_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING_MD))

        # ── User Selection ────────────────────────────────────────────
        self._user_section_label = tk.Label(
            self._form_card, text="👤 User", font=FONT_SUBHEADING, anchor="w",
        )
        self._user_section_label.pack(fill=tk.X, pady=(0, PADDING_SM))

        self._user_frame = tk.Frame(self._form_card)
        self._user_frame.pack(fill=tk.X, pady=(0, PADDING_LG))

        self._user_combo = ttk.Combobox(
            self._user_frame, state="readonly", font=FONT_INPUT, height=12,
        )
        self._user_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, PADDING_SM))

        self._add_user_btn = tk.Button(
            self._user_frame, text="+ New", font=FONT_SMALL, cursor="hand2",
            command=self._on_add_user,
        )
        self._add_user_btn.pack(side=tk.LEFT)

        # ── Weight Input ──────────────────────────────────────────────
        self._weight_label = tk.Label(
            self._form_card, text="⚖ Weight (kg)", font=FONT_SUBHEADING, anchor="w",
        )
        self._weight_label.pack(fill=tk.X, pady=(PADDING_MD, PADDING_XS))

        self._weight_entry = tk.Entry(
            self._form_card, font=FONT_INPUT,
        )
        self._weight_entry.pack(fill=tk.X, ipady=8, pady=(0, PADDING_XS))

        self._weight_hint = tk.Label(
            self._form_card, text="Range: 20 – 300 kg", font=FONT_SMALL, anchor="w",
        )
        self._weight_hint.pack(fill=tk.X, pady=(0, PADDING_MD))

        # ── Height Input ──────────────────────────────────────────────
        self._height_label = tk.Label(
            self._form_card, text="📏 Height (m)", font=FONT_SUBHEADING, anchor="w",
        )
        self._height_label.pack(fill=tk.X, pady=(PADDING_MD, PADDING_XS))

        self._height_entry = tk.Entry(
            self._form_card, font=FONT_INPUT,
        )
        self._height_entry.pack(fill=tk.X, ipady=8, pady=(0, PADDING_XS))

        self._height_hint = tk.Label(
            self._form_card, text="Range: 0.5 – 3.0 m", font=FONT_SMALL, anchor="w",
        )
        self._height_hint.pack(fill=tk.X, pady=(0, PADDING_LG))

        # ── Calculate Button ──────────────────────────────────────────
        self._calc_btn = tk.Button(
            self._form_card,
            text="🔍  Calculate BMI",
            font=FONT_BUTTON,
            cursor="hand2",
            command=self._on_calculate,
        )
        self._calc_btn.pack(fill=tk.X, ipady=10)

        # ── Save Button ───────────────────────────────────────────────
        self._save_btn = tk.Button(
            self._form_card,
            text="💾  Save Result",
            font=FONT_BUTTON,
            cursor="hand2",
            command=self._on_save,
            state=tk.DISABLED,
        )
        self._save_btn.pack(fill=tk.X, ipady=10, pady=(PADDING_SM, 0))

    def _build_result_display(self, parent: tk.Widget) -> None:
        """Build the result display section (right side)."""
        self._result_card = tk.Frame(parent, width=340)
        self._result_card.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(PADDING_MD, 0))
        self._result_card.pack_propagate(False)

        # Result title
        self._result_title = tk.Label(
            self._result_card, text="Your Result", font=FONT_HEADING, anchor="center",
        )
        self._result_title.pack(fill=tk.X, pady=(PADDING_LG, PADDING_MD))

        # BMI value display
        self._bmi_value_label = tk.Label(
            self._result_card, text="--", font=FONT_DISPLAY, anchor="center",
        )
        self._bmi_value_label.pack(fill=tk.X, pady=PADDING_MD)

        # Category label
        self._category_label = tk.Label(
            self._result_card, text="Enter values to calculate",
            font=FONT_DISPLAY_CATEGORY, anchor="center",
        )
        self._category_label.pack(fill=tk.X, pady=(0, PADDING_MD))

        # Explanation
        self._explanation_label = tk.Label(
            self._result_card, text="", font=FONT_BODY, anchor="center",
            wraplength=280, justify=tk.CENTER,
        )
        self._explanation_label.pack(fill=tk.X, padx=PADDING_MD, pady=(0, PADDING_LG))

        # BMI Scale reference
        self._scale_frame = tk.Frame(self._result_card)
        self._scale_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=(0, PADDING_LG))

        self._build_bmi_scale(self._scale_frame)

    def _build_bmi_scale(self, parent: tk.Widget) -> None:
        """Build a visual BMI category scale reference."""
        categories = [
            ("Underweight", "< 18.5", CATEGORY_COLORS["Underweight"]),
            ("Normal", "18.5 – 24.9", CATEGORY_COLORS["Normal"]),
            ("Overweight", "25 – 29.9", CATEGORY_COLORS["Overweight"]),
            ("Obese", "≥ 30", CATEGORY_COLORS["Obese"]),
        ]

        self._scale_labels = []
        for name, rng, color in categories:
            row = tk.Frame(parent)
            row.pack(fill=tk.X, pady=3)

            dot = tk.Label(row, text="●", font=("Segoe UI", 12), fg=color)
            dot.pack(side=tk.LEFT, padx=(0, PADDING_SM))

            lbl = tk.Label(row, text=f"{name}  ({rng})", font=FONT_BODY, anchor="w")
            lbl.pack(side=tk.LEFT)

            self._scale_labels.append((dot, lbl))

    # ── Event Handlers ────────────────────────────────────────────────

    def _on_add_user(self) -> None:
        """Open a dialog to add a new user."""
        dialog = tk.Toplevel(self)
        dialog.title("Add User")
        dialog.geometry("360x180")
        dialog.transient(self.app)
        dialog.grab_set()
        dialog.resizable(False, False)

        p = self.app.theme.palette
        dialog.configure(bg=p.bg_primary)

        tk.Label(
            dialog, text="Enter your name:", font=FONT_BODY,
            bg=p.bg_primary, fg=p.fg_primary,
        ).pack(pady=(PADDING_LG, PADDING_SM), padx=PADDING_MD)

        name_entry = tk.Entry(dialog, font=FONT_INPUT, width=30,
                              bg=p.bg_input, fg=p.fg_primary,
                              insertbackground=p.fg_primary,
                              relief=tk.FLAT,
                              highlightbackground=p.input_border,
                              highlightthickness=1,
                              highlightcolor=p.input_focus)
        name_entry.pack(padx=PADDING_MD, pady=PADDING_SM, ipady=6)
        name_entry.focus_set()

        def submit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid", "Name cannot be empty.", parent=dialog)
                return
            try:
                user_id = self.app.db.add_user(name)
                dialog.destroy()
                self._load_users()
                # Select the newly added user
                users = self.app.db.get_all_users()
                for u in users:
                    if u.user_id == user_id:
                        self.app.set_current_user(u)
                        break
                self._select_current_user()
            except ValueError as e:
                messagebox.showwarning("Invalid", str(e), parent=dialog)

        tk.Button(
            dialog, text="Add User", font=FONT_BUTTON, cursor="hand2",
            command=submit, bg=p.accent, fg="#FFFFFF",
            activebackground=p.accent_hover, bd=0,
        ).pack(pady=PADDING_MD, padx=PADDING_MD, fill=tk.X, ipady=6)

        name_entry.bind("<Return>", lambda e: submit())

    def _on_calculate(self) -> None:
        """Validate inputs, calculate BMI, and display the result."""
        # Validate weight
        weight_result = InputValidator.validate_weight(self._weight_entry.get())
        if not weight_result.is_valid:
            self._show_error(weight_result.error_message)
            return

        # Validate height
        height_result = InputValidator.validate_height(self._height_entry.get())
        if not height_result.is_valid:
            self._show_error(height_result.error_message)
            return

        # Calculate
        try:
            bmi_value = BMIEngine.calculate_bmi(weight_result.value, height_result.value)
            result = BMIEngine.classify_bmi(bmi_value)
        except (ValueError, TypeError) as e:
            self._show_error(str(e))
            return

        self._last_result = result
        self._display_result(result)
        self._save_btn.configure(state=tk.NORMAL)

    def _on_save(self) -> None:
        """Save the current BMI result to the database."""
        if not self._last_result:
            return

        if not self.app.current_user:
            messagebox.showwarning("No User", "Please select or create a user before saving.")
            return

        weight_result = InputValidator.validate_weight(self._weight_entry.get())
        height_result = InputValidator.validate_height(self._height_entry.get())

        if not weight_result.is_valid or not height_result.is_valid:
            messagebox.showwarning("Invalid", "Please recalculate before saving.")
            return

        try:
            self.app.db.save_bmi_record(
                user_id=self.app.current_user.user_id,
                weight_kg=weight_result.value,
                height_m=height_result.value,
                bmi=self._last_result.bmi,
                category=self._last_result.category,
            )
            messagebox.showinfo("Saved", "BMI record saved successfully!")
            self._save_btn.configure(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save record: {e}")

    # ── Display Helpers ───────────────────────────────────────────────

    def _display_result(self, result: BMIResult) -> None:
        """Display a BMI result in the result card.

        Args:
            result: The BMIResult to display.
        """
        p = self.app.theme.palette
        cat_color = self.app.theme.category_color(result.category)
        cat_bg = self.app.theme.category_bg_color(result.category)

        self._bmi_value_label.configure(text=f"{result.bmi}", fg=cat_color)
        self._category_label.configure(text=result.category, fg=cat_color)
        self._explanation_label.configure(text=result.explanation, fg=p.fg_primary)
        self._result_card.configure(bg=cat_bg)
        self._result_title.configure(bg=cat_bg, fg=p.fg_primary)
        self._bmi_value_label.configure(bg=cat_bg)
        self._category_label.configure(bg=cat_bg)
        self._explanation_label.configure(bg=cat_bg)
        self._scale_frame.configure(bg=cat_bg)

        # Scale labels need to match result card bg
        for dot, lbl in self._scale_labels:
            dot.configure(bg=cat_bg)
            lbl.configure(bg=cat_bg, fg=p.fg_primary)

    def _show_error(self, message: str) -> None:
        """Show an error message box.

        Args:
            message: The error message to display.
        """
        messagebox.showwarning("Validation Error", message)

    # ── Data Loading ──────────────────────────────────────────────────

    def _load_users(self) -> None:
        """Load users from the database into the combobox."""
        users = self.app.db.get_all_users()
        user_names = [f"{u.name} (ID: {u.user_id})" for u in users]
        self._user_combo["values"] = user_names
        self._users_list = users

    def _select_current_user(self) -> None:
        """Select the current user in the combobox."""
        if self.app.current_user and hasattr(self, "_users_list"):
            for i, u in enumerate(self._users_list):
                if u.user_id == self.app.current_user.user_id:
                    self._user_combo.current(i)
                    return

    # ── Public Methods ────────────────────────────────────────────────

    def refresh(self) -> None:
        """Refresh the page data (called on page switch)."""
        self._load_users()
        self._select_current_user()

        # Bind combobox selection
        self._user_combo.bind("<<ComboboxSelected>>", self._on_user_selected)

    def _on_user_selected(self, event=None) -> None:
        """Handle user selection from combobox."""
        idx = self._user_combo.current()
        if hasattr(self, "_users_list") and 0 <= idx < len(self._users_list):
            self.app.set_current_user(self._users_list[idx])

    def apply_theme(self) -> None:
        """Apply the current theme to all dashboard widgets."""
        p = self.app.theme.palette

        self.configure(bg=p.bg_primary)
        self._container.configure(bg=p.bg_primary)
        self._content_frame.configure(bg=p.bg_primary)
        self._header_label.configure(bg=p.bg_primary, fg=p.fg_primary)

        # Form card
        self._form_card.configure(bg=p.bg_primary)
        self._user_section_label.configure(bg=p.bg_primary, fg=p.fg_primary)
        self._user_frame.configure(bg=p.bg_primary)
        self._add_user_btn.configure(bg=p.bg_card, fg=p.fg_primary,
                                      activebackground=p.accent_hover, bd=0,
                                      highlightbackground=p.card_border,
                                      highlightthickness=1)

        self._weight_label.configure(bg=p.bg_primary, fg=p.fg_primary)
        self._weight_entry.configure(bg=p.bg_input, fg=p.fg_primary,
                                      insertbackground=p.fg_primary, relief=tk.FLAT,
                                      highlightbackground=p.input_border,
                                      highlightthickness=1,
                                      highlightcolor=p.input_focus)
        self._weight_hint.configure(bg=p.bg_primary, fg=p.fg_muted)

        self._height_label.configure(bg=p.bg_primary, fg=p.fg_primary)
        self._height_entry.configure(bg=p.bg_input, fg=p.fg_primary,
                                      insertbackground=p.fg_primary, relief=tk.FLAT,
                                      highlightbackground=p.input_border,
                                      highlightthickness=1,
                                      highlightcolor=p.input_focus)
        self._height_hint.configure(bg=p.bg_primary, fg=p.fg_muted)

        self._calc_btn.configure(bg=p.accent, fg="#FFFFFF",
                                  activebackground=p.accent_hover, bd=0)
        self._save_btn.configure(bg=p.bg_card, fg=p.fg_primary,
                                  activebackground=p.accent_hover, bd=0,
                                  highlightbackground=p.card_border,
                                  highlightthickness=1)

        # Result card
        if self._last_result:
            self._display_result(self._last_result)
        else:
            self._result_card.configure(bg=p.bg_card,
                                         highlightbackground=p.card_border,
                                         highlightthickness=1)
            self._result_title.configure(bg=p.bg_card, fg=p.fg_primary)
            self._bmi_value_label.configure(bg=p.bg_card, fg=p.fg_muted)
            self._category_label.configure(bg=p.bg_card, fg=p.fg_muted)
            self._explanation_label.configure(bg=p.bg_card, fg=p.fg_secondary)
            self._scale_frame.configure(bg=p.bg_card)

            # Scale labels
            for dot, lbl in self._scale_labels:
                dot.configure(bg=p.bg_card)
                lbl.configure(bg=p.bg_card, fg=p.fg_secondary)