from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 7700)

# Universe 1, channel 1 -> /0/dmx/0
client.send_message("/0/dmx/0", 1.0)
print("Channel 1 full")
time.sleep(2)

client.send_message("/0/dmx/0", 0.0)
print("Channel 1 off")