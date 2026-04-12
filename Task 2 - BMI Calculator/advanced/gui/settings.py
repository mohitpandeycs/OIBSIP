"""Settings page for the BMI Calculator GUI.

Provides theme switching (dark/light), user management (add, select,
delete), and application information.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ..database.models import UserRecord
from .styles import (
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_BUTTON, FONT_INPUT, PADDING_XS, PADDING_SM,
    PADDING_MD, PADDING_LG, PADDING_XL,
)


class SettingsPage(tk.Frame):
    """Page for application settings and user management.

    Attributes:
        app: Reference to the root BMIApp instance for shared state.
    """

    def __init__(self, parent: tk.Widget, app: "BMIApp") -> None:
        super().__init__(parent)
        self.app = app
        self._build_ui()
        self.apply_theme()

    def _build_ui(self) -> None:
        """Build all settings page UI components."""
        self._container = tk.Frame(self)
        self._container.pack(fill=tk.BOTH, expand=True, padx=PADDING_XL, pady=PADDING_XL)

        # ── Header ────────────────────────────────────────────────────
        self._header_label = tk.Label(
            self._container, text="⚙ Settings", font=FONT_TITLE, anchor="w",
        )
        self._header_label.pack(fill=tk.X, pady=(0, PADDING_LG))

        # ── Theme Section ─────────────────────────────────────────────
        self._theme_card = tk.Frame(self._container, padx=PADDING_LG, pady=PADDING_LG)
        self._theme_card.pack(fill=tk.X, pady=(0, PADDING_MD))

        self._theme_title = tk.Label(
            self._theme_card, text="🎨 Appearance", font=FONT_HEADING, anchor="w",
        )
        self._theme_title.pack(fill=tk.X, pady=(0, PADDING_SM))

        self._theme_desc = tk.Label(
            self._theme_card,
            text="Switch between dark and light themes to suit your preference.",
            font=FONT_BODY, anchor="w", wraplength=500, justify=tk.LEFT,
        )
        self._theme_desc.pack(fill=tk.X, pady=(0, PADDING_MD))

        self._theme_btn = tk.Button(
            self._theme_card,
            text="🌙 Switch to Light Theme",
            font=FONT_BUTTON,
            cursor="hand2",
            command=self._toggle_theme,
        )
        self._theme_btn.pack(fill=tk.X, ipady=8)

        # ── User Management Section ───────────────────────────────────
        self._user_card = tk.Frame(self._container, padx=PADDING_LG, pady=PADDING_LG)
        self._user_card.pack(fill=tk.X, pady=(0, PADDING_MD))

        self._user_title = tk.Label(
            self._user_card, text="👤 User Management", font=FONT_HEADING, anchor="w",
        )
        self._user_title.pack(fill=tk.X, pady=(0, PADDING_MD))

        # Current user display
        self._current_user_label = tk.Label(
            self._user_card, text="Current User: None", font=FONT_BODY_BOLD, anchor="w",
        )
        self._current_user_label.pack(fill=tk.X, pady=(0, PADDING_MD))

        # User list
        self._user_list_label = tk.Label(
            self._user_card, text="All Users:", font=FONT_SUBHEADING, anchor="w",
        )
        self._user_list_label.pack(fill=tk.X, pady=(0, PADDING_SM))

        self._user_listbox = tk.Listbox(
            self._user_card, font=FONT_INPUT, height=6, selectmode=tk.SINGLE,
        )
        self._user_listbox.pack(fill=tk.X, pady=(0, PADDING_MD))

        # User action buttons
        user_btn_frame = tk.Frame(self._user_card)
        user_btn_frame.pack(fill=tk.X)

        self._select_user_btn = tk.Button(
            user_btn_frame, text="✓ Select", font=FONT_SMALL, cursor="hand2",
            command=self._select_user,
        )
        self._select_user_btn.pack(side=tk.LEFT, padx=(0, PADDING_SM))

        self._delete_user_btn = tk.Button(
            user_btn_frame, text="🗑 Delete User", font=FONT_SMALL, cursor="hand2",
            command=self._delete_user,
        )
        self._delete_user_btn.pack(side=tk.LEFT)

        # ── About Section ─────────────────────────────────────────────
        self._about_card = tk.Frame(self._container, padx=PADDING_LG, pady=PADDING_LG)
        self._about_card.pack(fill=tk.X, pady=(0, PADDING_MD))

        self._about_title = tk.Label(
            self._about_card, text="ℹ About", font=FONT_HEADING, anchor="w",
        )
        self._about_title.pack(fill=tk.X, pady=(0, PADDING_SM))

        self._about_text = tk.Label(
            self._about_card,
            text=(
                "BMI Calculator v1.0\n\n"
                "Calculate your Body Mass Index and track your health over time.\n"
                "BMI = weight(kg) / height(m)²\n\n"
                "Categories based on WHO standards:\n"
                "  • Underweight: BMI < 18.5\n"
                "  • Normal: 18.5 ≤ BMI < 25\n"
                "  • Overweight: 25 ≤ BMI < 30\n"
                "  • Obese: BMI ≥ 30"
            ),
            font=FONT_BODY, anchor="w", justify=tk.LEFT,
        )
        self._about_text.pack(fill=tk.X)

    # ── Event Handlers ────────────────────────────────────────────────

    def _toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        new_mode = self.app.theme.toggle()
        self.app.apply_theme()

        if new_mode == "light":
            self._theme_btn.configure(text="🌙 Switch to Dark Theme")
        else:
            self._theme_btn.configure(text="☀ Switch to Light Theme")

    def _select_user(self) -> None:
        """Select the user highlighted in the listbox."""
        selection = self._user_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a user from the list.")
            return

        users = self.app.db.get_all_users()
        idx = selection[0]
        if idx < len(users):
            self.app.set_current_user(users[idx])
            self._update_current_user_display()

    def _delete_user(self) -> None:
        """Delete the user highlighted in the listbox."""
        selection = self._user_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a user from the list.")
            return

        users = self.app.db.get_all_users()
        idx = selection[0]
        if idx >= len(users):
            return

        user = users[idx]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete user '{user.name}' and all their BMI records?",
        )
        if confirm:
            self.app.db.delete_user(user.user_id)
            # If deleted user was current, clear it
            if self.app.current_user and self.app.current_user.user_id == user.user_id:
                self.app.set_current_user(None)
            self._load_users()
            self._update_current_user_display()

    # ── Data Loading ──────────────────────────────────────────────────

    def _load_users(self) -> None:
        """Load users from the database into the listbox."""
        self._user_listbox.delete(0, tk.END)
        users = self.app.db.get_all_users()
        for u in users:
            self._user_listbox.insert(tk.END, f"  {u.name}  (ID: {u.user_id})")

    def _update_current_user_display(self) -> None:
        """Update the current user label."""
        if self.app.current_user:
            self._current_user_label.configure(
                text=f"Current User: {self.app.current_user.name}"
            )
        else:
            self._current_user_label.configure(text="Current User: None")

    # ── Public Methods ────────────────────────────────────────────────

    def refresh(self) -> None:
        """Refresh the page data (called on page switch)."""
        self._load_users()
        self._update_current_user_display()

        # Update theme button text
        if self.app.theme.mode == "light":
            self._theme_btn.configure(text="🌙 Switch to Dark Theme")
        else:
            self._theme_btn.configure(text="☀ Switch to Light Theme")

    def apply_theme(self) -> None:
        """Apply the current theme to all settings page widgets."""
        p = self.app.theme.palette

        self.configure(bg=p.bg_primary)
        self._container.configure(bg=p.bg_primary)
        self._header_label.configure(bg=p.bg_primary, fg=p.fg_primary)

        # Theme card
        self._theme_card.configure(bg=p.bg_card, highlightbackground=p.card_border,
                                    highlightthickness=1)
        self._theme_title.configure(bg=p.bg_card, fg=p.fg_primary)
        self._theme_desc.configure(bg=p.bg_card, fg=p.fg_secondary)
        self._theme_btn.configure(bg=p.accent, fg="#FFFFFF",
                                   activebackground=p.accent_hover, bd=0)

        # User card
        self._user_card.configure(bg=p.bg_card, highlightbackground=p.card_border,
                                   highlightthickness=1)
        self._user_title.configure(bg=p.bg_card, fg=p.fg_primary)
        self._current_user_label.configure(bg=p.bg_card, fg=p.fg_primary)
        self._user_list_label.configure(bg=p.bg_card, fg=p.fg_primary)
        self._user_listbox.configure(bg=p.bg_input, fg=p.fg_primary,
                                      selectbackground=p.accent,
                                      selectforeground="#FFFFFF",
                                      relief=tk.FLAT,
                                      highlightbackground=p.input_border,
                                      highlightthickness=1,
                                      highlightcolor=p.input_focus)
        self._select_user_btn.configure(bg=p.accent, fg="#FFFFFF",
                                         activebackground=p.accent_hover, bd=0)
        self._delete_user_btn.configure(bg=p.bg_secondary, fg=p.error,
                                          activebackground=p.accent_hover, bd=0)

        # About card
        self._about_card.configure(bg=p.bg_card, highlightbackground=p.card_border,
                                    highlightthickness=1)
        self._about_title.configure(bg=p.bg_card, fg=p.fg_primary)
        self._about_text.configure(bg=p.bg_card, fg=p.fg_secondary)