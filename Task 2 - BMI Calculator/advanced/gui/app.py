"""Main application shell for the BMI Calculator GUI.

Contains the BMIApp class which is the root Tkinter window. Manages
the navigation sidebar, content area, page switching, theme application,
and shared state (database manager, theme, current user).
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

from ..core.bmi_engine import BMIEngine
from ..core.validators import InputValidator
from ..database.db_manager import DatabaseManager
from ..database.models import UserRecord
from .styles import (
    Theme, FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_BUTTON, FONT_NAV,
    FONT_SMALL, PADDING_SM, PADDING_MD, PADDING_LG,
)


class BMIApp(tk.Tk):
    """Root application window for the BMI Calculator.

    Manages the navigation sidebar, content pages, shared state
    (database, theme, current user), and theme application across
    all widgets.
    """

    def __init__(self, db_path: str = "bmi_data.db") -> None:
        """Initialize the application window and all components.

        Args:
            db_path: Path to the SQLite database file.
        """
        super().__init__()

        # ── Shared State ──────────────────────────────────────────────
        self.theme = Theme(mode="dark")
        self.db = DatabaseManager(db_path)
        self.db.initialize_database()
        self.current_user: Optional[UserRecord] = None

        # ── Page Registry ─────────────────────────────────────────────
        self._pages: dict[str, tk.Frame] = {}
        self._current_page: Optional[str] = None

        # ── Window Setup ─────────────────────────────────────────────
        self.title("BMI Calculator")
        self.geometry("1020x680")
        self.minsize(860, 560)
        self.configure(bg=self.theme.palette.bg_primary)

        # ── Build UI ─────────────────────────────────────────────────
        self._build_sidebar()
        self._build_content_area()

        # ── Load Pages ───────────────────────────────────────────────
        self._create_pages()

        # ── Show Default Page ────────────────────────────────────────
        self.show_page("dashboard")

        # ── Protocol Handlers ────────────────────────────────────────
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Sidebar ────────────────────────────────────────────────────────

    def _build_sidebar(self) -> None:
        """Build the left navigation sidebar."""
        self._sidebar = tk.Frame(self, width=220)
        self._sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self._sidebar.pack_propagate(False)

        # App title area
        self._sidebar_header = tk.Frame(self._sidebar)
        self._sidebar_header.pack(fill=tk.X, padx=PADDING_MD, pady=(PADDING_LG, PADDING_MD))

        self._sidebar_icon = tk.Label(
            self._sidebar_header,
            text="⚖",
            font=("Segoe UI", 20),
            anchor="center",
        )
        self._sidebar_icon.pack(side=tk.LEFT, padx=(0, PADDING_SM))

        self._sidebar_title = tk.Label(
            self._sidebar_header,
            text="BMI Calc",
            font=FONT_TITLE,
            anchor="w",
        )
        self._sidebar_title.pack(side=tk.LEFT)

        # Separator
        self._sidebar_sep = tk.Frame(self._sidebar, height=1)
        self._sidebar_sep.pack(fill=tk.X, padx=PADDING_MD, pady=(0, PADDING_MD))

        # Navigation label
        self._nav_label = tk.Label(
            self._sidebar,
            text="MENU",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        )
        self._nav_label.pack(fill=tk.X, padx=PADDING_LG, pady=(0, PADDING_SM))

        # Navigation buttons
        self._nav_buttons: dict[str, tk.Button] = {}
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("history", "📋  History"),
            ("trends", "📈  Trends"),
            ("settings", "⚙  Settings"),
        ]

        for page_key, label_text in nav_items:
            btn = tk.Button(
                self._sidebar,
                text=label_text,
                font=FONT_NAV,
                anchor="w",
                padx=PADDING_MD,
                pady=PADDING_SM,
                bd=0,
                cursor="hand2",
                command=lambda key=page_key: self.show_page(key),
            )
            btn.pack(fill=tk.X, padx=PADDING_SM, pady=1)
            self._nav_buttons[page_key] = btn

        # Spacer
        tk.Frame(self._sidebar).pack(fill=tk.BOTH, expand=True)

        # Separator before user
        self._sidebar_sep2 = tk.Frame(self._sidebar, height=1)
        self._sidebar_sep2.pack(fill=tk.X, padx=PADDING_MD, pady=PADDING_SM)

        # User indicator at bottom
        self._user_label = tk.Label(
            self._sidebar,
            text="👤 No user selected",
            font=FONT_SMALL,
            anchor="w",
            padx=PADDING_MD,
            pady=PADDING_MD,
        )
        self._user_label.pack(fill=tk.X)

        self._apply_sidebar_theme()

    def _apply_sidebar_theme(self) -> None:
        """Apply current theme colors to sidebar widgets."""
        p = self.theme.palette
        self._sidebar.configure(bg=p.bg_secondary)
        self._sidebar_header.configure(bg=p.bg_secondary)
        self._sidebar_icon.configure(bg=p.bg_secondary, fg=p.accent)
        self._sidebar_title.configure(bg=p.bg_secondary, fg=p.fg_primary)
        self._sidebar_sep.configure(bg=p.border)
        self._sidebar_sep2.configure(bg=p.border)
        self._nav_label.configure(bg=p.bg_secondary, fg=p.fg_muted)
        self._user_label.configure(bg=p.bg_secondary, fg=p.fg_secondary)

        for key, btn in self._nav_buttons.items():
            is_active = self._current_page == key
            if is_active:
                btn.configure(
                    bg=p.accent,
                    fg="#FFFFFF",
                    activebackground=p.accent_hover,
                    activeforeground="#FFFFFF",
                )
            else:
                btn.configure(
                    bg=p.bg_secondary,
                    fg=p.fg_secondary,
                    activebackground=p.bg_card,
                    activeforeground=p.fg_primary,
                )

    # ── Content Area ──────────────────────────────────────────────────

    def _build_content_area(self) -> None:
        """Build the main content area where pages are displayed."""
        self._content = tk.Frame(self)
        self._content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._content.configure(bg=self.theme.palette.bg_primary)

    # ── Page Management ───────────────────────────────────────────────

    def _create_pages(self) -> None:
        """Instantiate all page frames and register them."""
        from .dashboard import DashboardPage
        from .history import HistoryPage
        from .trends import TrendsPage
        from .settings import SettingsPage

        page_classes = {
            "dashboard": DashboardPage,
            "history": HistoryPage,
            "trends": TrendsPage,
            "settings": SettingsPage,
        }

        for key, cls in page_classes.items():
            page = cls(parent=self._content, app=self)
            self._pages[key] = page

    def show_page(self, page_key: str) -> None:
        """Switch the visible page in the content area.

        Args:
            page_key: Key identifying the page to show.
        """
        # Hide current page
        if self._current_page and self._current_page in self._pages:
            self._pages[self._current_page].pack_forget()

        # Show new page
        if page_key in self._pages:
            self._pages[page_key].pack(fill=tk.BOTH, expand=True)
            self._current_page = page_key

            # Refresh page data if it has a refresh method
            if hasattr(self._pages[page_key], "refresh"):
                self._pages[page_key].refresh()

        # Update sidebar active state
        self._apply_sidebar_theme()

    # ── Theme Application ─────────────────────────────────────────────

    def apply_theme(self) -> None:
        """Apply the current theme to the entire application."""
        p = self.theme.palette
        self.configure(bg=p.bg_primary)
        self._content.configure(bg=p.bg_primary)
        self._apply_sidebar_theme()

        # Re-apply theme to all pages
        for page in self._pages.values():
            if hasattr(page, "apply_theme"):
                page.apply_theme()

    # ── User Management ───────────────────────────────────────────────

    def set_current_user(self, user: Optional[UserRecord]) -> None:
        """Set the currently active user and update the UI.

        Args:
            user: The UserRecord to set as active, or None.
        """
        self.current_user = user
        if user:
            self._user_label.configure(text=f"👤 {user.name}")
        else:
            self._user_label.configure(text="👤 No user selected")

        # Refresh current page to reflect user change
        if self._current_page and self._current_page in self._pages:
            page = self._pages[self._current_page]
            if hasattr(page, "refresh"):
                page.refresh()

    # ── Cleanup ───────────────────────────────────────────────────────

    def _on_close(self) -> None:
        """Handle window close: close database and destroy window."""
        self.db.close()
        self.destroy()