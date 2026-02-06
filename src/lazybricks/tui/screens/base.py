"""Base screen with common patterns for all LazyBricks screens.

All screens inherit from this to get:
- Access to app-level state (client, guard, ops)
- Common refresh patterns
- Error handling
- Footer bar context action updates
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.screen import Screen

from lazybricks.tui.widgets.footer_bar import HintItem

if TYPE_CHECKING:
    from lazybricks.tui.app import LazyBricksApp


class BaseScreen(Screen):
    """Base class for all LazyBricks screens.

    Provides:
    - Type-safe access to app instance
    - Common refresh pattern with error handling
    - Footer bar context action management
    """

    @property
    def lazybricks_app(self) -> "LazyBricksApp":
        """Type-safe access to the LazyBricks app."""
        from lazybricks.tui.app import LazyBricksApp
        assert isinstance(self.app, LazyBricksApp)
        return self.app

    @property
    def client(self):
        """Shortcut to DatabricksClient."""
        return self.lazybricks_app.client

    @property
    def guard(self):
        """Shortcut to ArmedGuard."""
        return self.lazybricks_app.guard

    def on_mount(self) -> None:
        """Called when screen is mounted. Updates footer."""
        self._update_footer()

    def on_screen_resume(self) -> None:
        """Called when screen is resumed. Updates footer."""
        self._update_footer()

    def get_context_actions(self) -> list[HintItem]:
        """Return context actions for footer bar.

        Override in subclasses to provide screen-specific actions.
        Actions with destructive=True only show when armed.
        """
        return []

    def _update_footer(self) -> None:
        """Update footer bar with this screen's context actions."""
        actions = self.get_context_actions()
        self.lazybricks_app.update_footer(actions)

    def notify_error(self, message: str) -> None:
        """Show an error notification."""
        self.app.notify(message, severity="error", timeout=5)

    def notify_success(self, message: str) -> None:
        """Show a success notification."""
        self.app.notify(message, severity="information", timeout=3)

    def notify_warning(self, message: str) -> None:
        """Show a warning notification."""
        self.app.notify(message, severity="warning", timeout=4)

    def require_armed(self, action_name: str) -> bool:
        """Check if armed mode is active.

        If not armed, shows a warning notification.

        Returns:
            True if armed and action can proceed, False otherwise.
        """
        if self.guard.is_armed:
            return True

        self.notify_warning(f"Press A to arm before {action_name}")
        return False
