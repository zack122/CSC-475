from pythonosc.udp_client import SimpleUDPClient


class QLCController:
    def __init__(self, ip="127.0.0.1", port=7700):
        self.client = SimpleUDPClient(ip, port)

    def _clamp(self, value):
        return max(0, min(255, int(value)))

    def _send(self, path, value):
        self.client.send_message(path, self._clamp(value))

    def set_fixture_channel(self, fixture, channel_name, value):
        """
        Generic OSC sender for a mapped QLC+ control.

        fixture:
            wash lights: 1-4
            moving heads: 5-6

        channel_name examples:
            brightness, red, green, blue, white, strobe, pan, tilt, speed
        """
        valid_channels = {
            "brightness",
            "red",
            "green",
            "blue",
            "white",
            "strobe",
            "pan",
            "tilt",
            "speed",
        }

        if fixture not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"Invalid fixture: {fixture}")

        if channel_name not in valid_channels:
            raise ValueError(f"Invalid channel name: {channel_name}")

        path = f"/mir/f{fixture}/{channel_name}"
        try:
            self.client.send_message(path, value)
        except BlockingIOError:
            # macOS errno 35 (EAGAIN): non-blocking UDP socket send buffer is
            # momentarily full. Drop this frame's packet — missing a single
            # ~23ms lighting frame is imperceptible.
            pass

    def set_fixture(
        self,
        fixture,
        brightness=0,
        red=0,
        green=0,
        blue=0,
        white=0,
        strobe=0,
    ):
        """
        Set RGBW wash-style controls for any mapped fixture.
        For moving heads (fixtures 5 and 6), this controls:
          brightness, RGBW, and strobe
        """
        self.set_fixture_channel(fixture, "brightness", brightness)
        self.set_fixture_channel(fixture, "red", red)
        self.set_fixture_channel(fixture, "green", green)
        self.set_fixture_channel(fixture, "blue", blue)
        self.set_fixture_channel(fixture, "white", white)
        self.set_fixture_channel(fixture, "strobe", strobe)

    def set_moving_head(self, fixture, pan=127, tilt=127, speed=100):
        """
        Moving heads are fixtures 5 and 6.

        fixture 5 channels:
            33 pan
            34 tilt
            35 brightness
            36 red
            37 green
            38 blue
            39 white
            40 strobe
            41 speed

        fixture 6 channels:
            42 pan
            43 tilt
            44 brightness
            45 red
            46 green
            47 blue
            48 white
            49 strobe
            50 speed
        """
        if fixture not in [5, 6]:
            raise ValueError("Moving heads must be fixture 5 or 6")

        self.set_fixture_channel(fixture, "pan", pan)
        self.set_fixture_channel(fixture, "tilt", tilt)
        self.set_fixture_channel(fixture, "speed", speed)

    def blackout(self, num_fixtures=6):
        """
        Black out all mapped fixtures.
        """
        for fixture in range(1, num_fixtures + 1):
            try:
                self.set_fixture(
                    fixture,
                    brightness=0,
                    red=0,
                    green=0,
                    blue=0,
                    white=0,
                    strobe=0,
                )
            except Exception:
                pass

        # Park moving heads roughly centered and slowed
        for fixture in [5, 6]:
            try:
                self.set_moving_head(fixture, pan=127, tilt=127, speed=255)
            except Exception:
                pass
