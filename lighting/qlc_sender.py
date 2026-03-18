from pythonosc.udp_client import SimpleUDPClient


class QLCController:
    def __init__(self, ip="127.0.0.1", port=7700):
        self.client = SimpleUDPClient(ip, port)

        # Map channel numbers from server.py to your QLC+ OSC widget paths
        self.path_map = {
            1: "/mir/brightness",
            2: "/mir/warm",
            3: "/mir/cool",
            4: "/mir/strobe",
        }

    def set_channel(self, channel, value):
        """
        channel: 1-4
            1 -> brightness
            2 -> warm
            3 -> cool
            4 -> strobe
        value: 0-255
        """
        if channel not in self.path_map:
            raise ValueError(f"Unknown channel: {channel}")

        value = max(0, min(255, int(value)))
        self.client.send_message(self.path_map[channel], value)

    def blackout(self, num_channels=4):
        for ch in range(1, num_channels + 1):
            if ch in self.path_map:
                self.set_channel(ch, 0)