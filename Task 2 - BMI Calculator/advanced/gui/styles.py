"""Theme and style definitions for the BMI Calculator GUI.

Provides the Theme class with dark/light color palettes, typography,
spacing constants, and color-coded BMI category colors used across
all GUI components.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    """Immutable color palette for a theme.

    All values are Tkinter-compatible color strings (hex or named).
    """
    bg_primary: str
    bg_secondary: str
    bg_card: str
    bg_input: str
    fg_primary: str
    fg_secondary: str
    fg_muted: str
    accent: str
    accent_hover: str
    border: str
    card_border: str
    input_border: str
    input_focus: str
    error: str
    success: str
    warning: str


# ── BMI Category Colors (shared across themes) ─────────────────────────────

CATEGORY_COLORS: dict[str, str] = {
    "Underweight": "#5DADE2",   # Soft blue
    "Normal":     "#58D68D",    # Fresh green
    "Overweight": "#F4D03F",    # Warm amber
    "Obese":      "#EC7063",    # Coral red
}

CATEGORY_BG_COLORS: dict[str, str] = {
    "Underweight": "#1A3A5C",
    "Normal":      "#1A3C2A",
    "Overweight":  "#3C3510",
    "Obese":       "#3C1A1A",
}


# ── Dark Theme ──────────────────────────────────────────────────────────────

DARK_PALETTE = ColorPalette(
    bg_primary="#1E1E2E",
    bg_secondary="#252540",
    bg_card="#2A2A45",
    bg_input="#22223A",
    fg_primary="#F0F0F5",
    fg_secondary="#C0C0D0",
    fg_muted="#8888A0",
    accent="#7C5CFC",
    accent_hover="#9B7FFF",
    border="#3A3A55",
    card_border="#3A3A55",
    input_border="#4A4A65",
    input_focus="#7C5CFC",
    error="#FF6B6B",
    success="#51CF66",
    warning="#FFD43B",
)


# ── Light Theme ──────────────────────────────────────────────────────────────

LIGHT_PALETTE = ColorPalette(
    bg_primary="#F5F5FA",
    bg_secondary="#EAEAF0",
    bg_card="#FFFFFF",
    bg_input="#FFFFFF",
    fg_primary="#1A1A2E",
    fg_secondary="#4A4A60",
    fg_muted="#808098",
    accent="#5B3FD4",
    accent_hover="#7C5CFC",
    border="#D0D0DD",
    card_border="#D0D0DD",
    input_border="#C0C0D0",
    input_focus="#5B3FD4",
    error="#D63031",
    success="#2F9E44",
    warning="#E67E22",
)


# ── Typography ──────────────────────────────────────────────────────────────

FONT_FAMILY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"

FONT_TITLE = (FONT_FAMILY, 24, "bold")
FONT_HEADING = (FONT_FAMILY, 17, "bold")
FONT_SUBHEADING = (FONT_FAMILY, 14, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_BODY_BOLD = (FONT_FAMILY, 12, "bold")
FONT_SMALL = (FONT_FAMILY, 10)
FONT_BUTTON = (FONT_FAMILY, 12, "bold")
FONT_INPUT = (FONT_FAMILY, 12)
FONT_DISPLAY = (FONT_FAMILY, 48, "bold")
FONT_DISPLAY_CATEGORY = (FONT_FAMILY, 20, "bold")
FONT_NAV = (FONT_FAMILY, 12)


# ── Spacing ─────────────────────────────────────────────────────────────────

PADDING_XS = 4
PADDING_SM = 8
PADDING_MD = 16
PADDING_LG = 24
PADDING_XL = 32

BORDER_RADIUS = 8
INPUT_HEIGHT = 40
BUTTON_HEIGHT = 44
CARD_PADDING = 20


# ── Theme Manager ───────────────────────────────────────────────────────────

class Theme:
    """Manages the current theme and provides access to palette colors.

    Switches between dark and light themes and exposes the active
    ColorPalette for use by all GUI components.
    """

    DARK = "dark"
    LIGHT = "light"

    _PALETTES = {
        "dark": DARK_PALETTE,
        "light": LIGHT_PALETTE,
    }

    def __init__(self, mode: str = "dark") -> None:
        """Initialize the Theme with a mode ('dark' or 'light').

        Args:
            mode: The initial theme mode.

        Raises:
            ValueError: If mode is not 'dark' or 'light'.
        """
        if mode not in self._PALETTES:
            raise ValueError(f"Invalid theme mode: '{mode}'. Use 'dark' or 'light'.")
        self._mode = mode

    @property
    def mode(self) -> str:
        """Current theme mode string."""
        return self._mode

    @property
    def palette(self) -> ColorPalette:
        """The active ColorPalette for the current mode."""
        return self._PALETTES[self._mode]

    def toggle(self) -> str:
        """Switch between dark and light themes.

        Returns:
            The new theme mode string.
        """
        self._mode = "light" if self._mode == "dark" else "dark"
        return self._mode

    def set_mode(self, mode: str) -> None:
        """Set the theme mode explicitly.

        Args:
            mode: 'dark' or 'light'.

        Raises:
            ValueError: If mode is not valid.
        """
        if mode not in self._PALETTES:
            raise ValueError(f"Invalid theme mode: '{mode}'. Use 'dark' or 'light'.")
        self._mode = mode

    def category_color(self, category: str) -> str:
        """Get the foreground color for a BMI category.

        Args:
            category: WHO category string.

        Returns:
            Hex color string for the category.
        """
        return CATEGORY_COLORS.get(category, self.palette.fg_primary)

    def category_bg_color(self, category: str) -> str:
        """Get the background color for a BMI category.

        Args:
            category: WHO category string.

        Returns:
            Hex color string for the category background.
        """
        return CATEGORY_BG_COLORS.get(category, self.palette.bg_card)