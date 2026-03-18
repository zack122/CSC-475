from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 7700)

# Change this variable to map different controls
MODE = "brightness"
# options: "brightness", "warm", "cool", "strobe"

print(f"Mapping mode: {MODE}")

while True:
    if MODE == "brightness":
        client.send_message("/mir/brightness", 255)
        print("sending brightness")

    elif MODE == "warm":
        client.send_message("/mir/warm", 255)
        print("sending warm")

    elif MODE == "cool":
        client.send_message("/mir/cool", 255)
        print("sending cool")

    elif MODE == "strobe":
        client.send_message("/mir/strobe", 255)
        print("sending strobe")

    time.sleep(0.3)