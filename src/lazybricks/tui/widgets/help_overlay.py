"""Help overlay — modal showing all keybindings.

Shows complete keyboard reference organized by section.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Static
from textual.binding import Binding


class HelpOverlay(ModalScreen):
    """Modal overlay showing all keybindings."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("question_mark", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
    ]

    DEFAULT_CSS = """
    HelpOverlay {
        align: center middle;
    }

    #help-container {
        width: 70;
        max-height: 85%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    #help-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #help-scroll {
        height: auto;
        max-height: 100%;
    }

    .section-title {
        color: $primary;
        text-style: bold;
        margin-top: 1;
    }

    .help-row {
        margin-left: 2;
    }

    .key {
        color: $warning;
    }

    #help-footer {
        margin-top: 1;
        text-align: center;
        color: $text-muted;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(
            Static("LazyBricks Keyboard Reference", id="help-title"),
            ScrollableContainer(
                # Global Navigation
                Static("Global Navigation", classes="section-title"),
                Static("  [h]       Home", classes="help-row"),
                Static("  [c]       Clusters", classes="help-row"),
                Static("  [j]       Jobs", classes="help-row"),
                Static("  [w]       Warehouses", classes="help-row"),
                Static("  [p]       Profiles", classes="help-row"),
                Static("  [?]       Help", classes="help-row"),
                Static("  [q]       Quit", classes="help-row"),

                # Armed Mode
                Static("Armed Mode", classes="section-title"),
                Static("  [A]       Arm (30s countdown)", classes="help-row"),
                Static("  [Esc]     Disarm (when armed)", classes="help-row"),
                Static("  Destructive actions only work when armed.", classes="help-row"),
                Static("  Footer shows ARMED + countdown when active.", classes="help-row"),

                # Clusters
                Static("Clusters", classes="section-title"),
                Static("  [r]       Refresh list", classes="help-row"),
                Static("  [Enter]   Open in browser", classes="help-row"),
                Static("  [s]       Start (when armed, if stopped)", classes="help-row"),
                Static("  [t]       Terminate (when armed, if running)", classes="help-row"),
                Static("  [R]       Restart (when armed, if running)", classes="help-row"),

                # Jobs
                Static("Jobs", classes="section-title"),
                Static("  [Tab]     Switch pane (Jobs/Runs/Detail)", classes="help-row"),
                Static("  [Enter]   Drill down into selection", classes="help-row"),
                Static("  [Esc]     Back up one pane", classes="help-row"),
                Static("  [r]       Refresh", classes="help-row"),
                Static("  [l]       View logs for selected run", classes="help-row"),
                Static("  [n]       Run job now (when armed)", classes="help-row"),
                Static("  [c]       Cancel run (when armed, if active)", classes="help-row"),
                Static("  [R]       Rerun (when armed, if completed)", classes="help-row"),

                # Logs
                Static("Logs", classes="section-title"),
                Static("  [/]       Search", classes="help-row"),
                Static("  [n]       Next match", classes="help-row"),
                Static("  [N]       Previous match", classes="help-row"),
                Static("  [f]       Cycle filter (ALL/ERROR/WARN+/INFO+)", classes="help-row"),
                Static("  [g]       Go to top", classes="help-row"),
                Static("  [G]       Go to bottom", classes="help-row"),
                Static("  [o]       Open in browser", classes="help-row"),
                Static("  [Esc]     Close log viewer", classes="help-row"),

                # Warehouses
                Static("Warehouses", classes="section-title"),
                Static("  [r]       Refresh list", classes="help-row"),
                Static("  [Enter]   Open in browser", classes="help-row"),
                Static("  [s]       Start (when armed, if stopped)", classes="help-row"),
                Static("  [S]       Stop (when armed, if running)", classes="help-row"),

                # Profiles
                Static("Profiles", classes="section-title"),
                Static("  [Enter]   Switch to selected profile", classes="help-row"),
                Static("  [t]       Test connection", classes="help-row"),

                id="help-scroll",
            ),
            Static("Press Esc to close", id="help-footer"),
            id="help-container",
        )

    def action_dismiss(self) -> None:
        """Close the help overlay."""
        self.app.pop_screen()
