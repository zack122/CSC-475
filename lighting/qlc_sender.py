from pythonosc.udp_client import SimpleUDPClient


class QLCController:
    def __init__(self, ip="127.0.0.1", port=7700):
        self.client = SimpleUDPClient(ip, port)
        self.last_sent = {}

        self.path_map = {
            (1, "brightness"): "/mir/f1/brightness",
            (1, "warm"): "/mir/f1/warm",
            (1, "cool"): "/mir/f1/cool",
            (1, "strobe"): "/mir/f1/strobe",

            (2, "brightness"): "/mir/f2/brightness",
            (2, "warm"): "/mir/f2/warm",
            (2, "cool"): "/mir/f2/cool",
            (2, "strobe"): "/mir/f2/strobe",

            (3, "brightness"): "/mir/f3/brightness",
            (3, "warm"): "/mir/f3/warm",
            (3, "cool"): "/mir/f3/cool",
            (3, "strobe"): "/mir/f3/strobe",

            (4, "brightness"): "/mir/f4/brightness",
            (4, "warm"): "/mir/f4/warm",
            (4, "cool"): "/mir/f4/cool",
            (4, "strobe"): "/mir/f4/strobe",
        }

    def set_fixture_value(self, fixture, control, value):
        key = (int(fixture), str(control))
        if key not in self.path_map:
            raise ValueError(f"Unknown fixture/control mapping: {key}")

        value = max(0, min(255, int(value)))

        if self.last_sent.get(key) == value:
            return

        self.last_sent[key] = value
        self.client.send_message(self.path_map[key], value)

    def set_fixture(self, fixture, brightness=0, warm=0, cool=0, strobe=0):
        self.set_fixture_value(fixture, "brightness", brightness)
        self.set_fixture_value(fixture, "warm", warm)
        self.set_fixture_value(fixture, "cool", cool)
        self.set_fixture_value(fixture, "strobe", strobe)

    def blackout(self, num_fixtures=4):
        for fixture in range(1, num_fixtures + 1):
            self.set_fixture(fixture, 0, 0, 0, 0)