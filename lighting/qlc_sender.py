from pythonosc.udp_client import SimpleUDPClient


class QLCController:
    def __init__(self, ip="127.0.0.1", port=7700, universe=0):
        self.client = SimpleUDPClient(ip, port)
        self.universe = universe

    def set_channel(self, channel, value):
        """
        channel: DMX channel number starting at 1
        value: DMX value from 0 to 255
        """
        value = max(0, min(255, int(value)))
        osc_path = f"/{self.universe}/dmx/{channel - 1}"
        osc_value = value / 255.0
        self.client.send_message(osc_path, osc_value)

    def blackout(self, num_channels=4):
        for ch in range(1, num_channels + 1):
            self.set_channel(ch, 0)