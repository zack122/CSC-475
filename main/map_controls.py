from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 7700)

# =========================
# CHANGE THESE ONLY
# =========================
FIXTURE = 6
MODE = "speed"   # pan, tilt, brightness, red, green, blue, white, strobe, speed
VALUE = 127    # use 255 for brightness/colors/strobe, 127 is good for pan/tilt/speed
DELAY = 0.5

path = f"/mir/f{FIXTURE}/{MODE}"

print(f"Sending to {path} with value {VALUE}")

while True:
    client.send_message(path, VALUE)
    print(f"sending {path} -> {VALUE}")
    time.sleep(DELAY)