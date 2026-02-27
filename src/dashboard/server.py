"""FastAPI + WebSocket dashboard for real-time monitoring."""

from src.models import FeatureFrame, DMXFrame


class DashboardServer:
    """Runs a FastAPI server in a background thread, pushing feature/DMX data via WebSocket."""

    def __init__(self, port: int = 8080, push_rate_hz: int = 30):
        self._port = port
        self._push_rate_hz = push_rate_hz
        self._app = None  # FastAPI instance

    def start(self) -> None:
        """Launch the server in a background thread."""
        # TODO: create FastAPI app, mount static files, start uvicorn in thread
        raise NotImplementedError

    def push(self, features: FeatureFrame, dmx: DMXFrame, latency_ms: float) -> None:
        """Push current state to all connected WebSocket clients."""
        # TODO: serialize and broadcast via WebSocket
        raise NotImplementedError

    def stop(self) -> None:
        """Shut down the dashboard server."""
        # TODO: graceful shutdown
        raise NotImplementedError
