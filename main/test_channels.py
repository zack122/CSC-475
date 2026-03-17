import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lighting.qlc_sender import QLCController

qlc = QLCController(ip="127.0.0.1", port=7700, universe=0)

print("Dimmer full")
qlc.set_channel(1, 255)
time.sleep(1)

print("Warm full")
qlc.set_channel(2, 255)
time.sleep(1)

print("Cool full")
qlc.set_channel(3, 255)
time.sleep(1)

print("Strobe full")
qlc.set_channel(4, 255)
time.sleep(1)

print("Blackout")
qlc.blackout(4)