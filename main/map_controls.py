from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 7700)

FIXTURE = 1  # change 1–4
MODE = "strobe"  # brightness, warm, cool, strobe

path = f"/mir/f{FIXTURE}/{MODE}"

print(f"Sending to {path}")

while True:
    client.send_message(path, 255)
    print(f"sending {path}")
    time.sleep(0.5)