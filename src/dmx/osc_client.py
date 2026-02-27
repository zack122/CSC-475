"""OSC client for sending DMX values to QLC+.

Owner: Leo DeRosa
"""

from src.models import DMXFrame


class OSCClient:
    """Sends DMXFrame values to QLC+ over OSC (UDP)."""

    def __init__(self, host: str = "127.0.0.1", port: int = 7700, address_map: dict | None = None):
        self._host = host
        self._port = port
        self._address_map = address_map or {}
        self._client = None  # python_osc.SimpleUDPClient, initialized in connect()

    def connect(self) -> None:
        """Initialize the OSC UDP client."""
        # TODO: from pythonosc.udp_client import SimpleUDPClient
        raise NotImplementedError

    def send(self, dmx: DMXFrame) -> None:
        """Send all DMX channel values as OSC messages to QLC+."""
        # TODO: iterate address_map, send each field
        raise NotImplementedError

    def close(self) -> None:
        """Clean up the OSC client."""
        # TODO: teardown
        raise NotImplementedError
