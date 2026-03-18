from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 7700)

while True:
    print("brightness")
    client.send_message("/mir/brightness", 255)
    time.sleep(1)

    print("warm")
    client.send_message("/mir/warm", 255)
    time.sleep(1)

    print("cool")
    client.send_message("/mir/cool", 255)
    time.sleep(1)

    print("strobe")
    client.send_message("/mir/strobe", 255)
    time.sleep(1)

    print("all off")
    client.send_message("/mir/brightness", 0)
    client.send_message("/mir/warm", 0)
    client.send_message("/mir/cool", 0)
    client.send_message("/mir/strobe", 0)
    time.sleep(1)