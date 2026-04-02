from pythonosc.udp_client import SimpleUDPClient


class QLCController:
    def __init__(self, ip="127.0.0.1", port=7700):
        self.client = SimpleUDPClient(ip, port)

    def set_fixture_channel(self, fixture, channel_name, value):
        """
        fixture: 1-4
        channel_name: brightness, red, green, blue, white, strobe
        value: 0-255
        """
        if fixture not in [1, 2, 3, 4]:
            raise ValueError(f"Invalid fixture: {fixture}")

        valid_channels = {"brightness", "red", "green", "blue", "white", "strobe"}
        if channel_name not in valid_channels:
            raise ValueError(f"Invalid channel name: {channel_name}")

        value = max(0, min(255, int(value)))
        path = f"/mir/f{fixture}/{channel_name}"
        self.client.send_message(path, value)

    def set_fixture(self, fixture, brightness=0, red=0, green=0, blue=0, white=0, strobe=0):
        self.set_fixture_channel(fixture, "brightness", brightness)
        self.set_fixture_channel(fixture, "red", red)
        self.set_fixture_channel(fixture, "green", green)
        self.set_fixture_channel(fixture, "blue", blue)
        self.set_fixture_channel(fixture, "white", white)
        self.set_fixture_channel(fixture, "strobe", strobe)

    def blackout(self, num_fixtures=4):
        for fixture in range(1, num_fixtures + 1):
            self.set_fixture(fixture, 0, 0, 0, 0, 0, 0)