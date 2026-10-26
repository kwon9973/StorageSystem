import time
import logging
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s"
)

URI = "radio://0/80/2M"

first_packet = Event()
finished = Event()

cf = Crazyflie(rw_cache="./cache")


def on_link_established(uri):
    print(f"FIRST RESPONSE RECEIVED: {uri}", flush=True)
    first_packet.set()


def on_connected(uri):
    print(f"CONNECTED SUCCESSFULLY: {uri}", flush=True)
    finished.set()


def on_connection_failed(uri, message):
    print(f"CONNECTION FAILED: {uri}", flush=True)
    print(f"Reason: {message}", flush=True)
    finished.set()


cf.link_established.add_callback(on_link_established)
cf.connected.add_callback(on_connected)
cf.connection_failed.add_callback(on_connection_failed)

cflib.crtp.init_drivers()

print(f"Attempting connection to {URI}...", flush=True)
cf.open_link(URI)

deadline = time.monotonic() + 600

while time.monotonic() < deadline and not finished.is_set():
    time.sleep(0.1)

if not finished.is_set():
    print("TIMEOUT: no completed connection after 30 seconds.")
    print("Did the drone send a response?", first_packet.is_set())

cf.close_link()
print("Test finished.")