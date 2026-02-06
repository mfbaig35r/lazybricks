"""Home screen — health snapshot dashboard.

The first screen users see. Shows:
- Workspace identity
- Spark connectivity status
- Cluster/Job/Warehouse health summaries
- Most recent failure
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static
from textual import work

from lazybricks.models.health import HealthSnapshot
from lazybricks.tui.screens.base import BaseScreen
from lazybricks.tui.widgets.status_bar import HOME_BINDINGS


class HomeScreen(BaseScreen):
    """Home screen with health dashboard."""

    SCREEN_BINDINGS = HOME_BINDINGS

    BINDINGS = [
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._snapshot: HealthSnapshot | None = None
        self._loading = True

    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Static("Loading...", id="health-content"),
                id="home-container",
            ),
            id="screen-content",
        )

    def on_mount(self) -> None:
        """Load data on mount."""
        super().on_mount()
        self._refresh_data()
        # Auto-refresh every 60 seconds
        self.set_interval(60.0, self._refresh_data)

    def _refresh_data(self) -> None:
        """Trigger background data refresh."""
        self._load_health()

    @work(thread=True, exclusive=True)
    def _load_health(self) -> None:
        """Load health snapshot in background thread."""
        try:
            snapshot = self.lazybricks_app.health_builder.build()
            self.app.call_from_thread(self._update_display, snapshot)
        except Exception as e:
            self.app.call_from_thread(self._show_error, str(e))

    def _update_display(self, snapshot: HealthSnapshot) -> None:
        """Update UI with health data (called on main thread)."""
        self._snapshot = snapshot
        self._loading = False

        content = self.query_one("#health-content", Static)

        # Build the display
        lines = [
            "",
            "  [bold #e94560]LazyBricks — Health Snapshot[/]",
            "  " + "─" * 50,
            "",
            f"  [dim]Workspace:[/]  {snapshot.workspace_host}",
            f"  [dim]User:[/]       {snapshot.workspace_user}",
            f"  [dim]Profile:[/]    {snapshot.active_profile or 'default'}",
            "",
            f"  [dim]Spark:[/]      {self._format_spark_status(snapshot)}",
            "",
            "  " + "─" * 50,
            "",
            f"  [dim]Clusters:[/]   {snapshot.cluster_health_display}",
            f"  [dim]Jobs:[/]       {snapshot.job_health_display}",
            f"  [dim]Warehouses:[/] {snapshot.running_warehouses}/{snapshot.total_warehouses} running",
            "",
            "  " + "─" * 50,
            "",
            f"  [dim]Last fail:[/]  {snapshot.last_failure_display}",
            "",
            "  " + "─" * 50,
            "",
            "  [dim]Navigation:[/]  [bold #e94560]c[/] clusters  [bold #e94560]j[/] jobs  [bold #e94560]w[/] warehouses  [bold #e94560]p[/] profiles  [bold #e94560]?[/] help  [bold #e94560]q[/] quit",
            "  [dim]Actions:[/]     [bold #e94560]r[/] refresh  [bold #e94560]A[/] arm (for destructive actions)",
            "",
        ]

        content.update("\n".join(lines))

    def _format_spark_status(self, snapshot: HealthSnapshot) -> str:
        """Format spark status with color."""
        from lazybricks.models.health import SparkStatus

        if snapshot.spark_status == SparkStatus.CONNECTED:
            return f"[green]{snapshot.spark_display}[/]"
        elif snapshot.spark_status == SparkStatus.STALE:
            return f"[yellow]{snapshot.spark_display}[/]"
        elif snapshot.spark_status == SparkStatus.DISCONNECTED:
            return f"[red]{snapshot.spark_display}[/]"
        else:
            return f"[dim]{snapshot.spark_display}[/]"

    def _show_error(self, error: str) -> None:
        """Show error message."""
        content = self.query_one("#health-content", Static)
        content.update(f"\n  [red]Error loading health data:[/]\n  {error}\n\n  Press [bold]r[/] to retry.")
        self._loading = False

    def action_refresh(self) -> None:
        """Manual refresh action."""
        content = self.query_one("#health-content", Static)
        content.update("\n  Refreshing...")
        self._refresh_data()
        self.notify_success("Refreshing health data...")
