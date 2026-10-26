import time
import logging
logging.basicConfig(level=logging.INFO)
import cflib.crtp
from cflib.crazyflie import Crazyflie

cflib.crtp.init_drivers()
cf = Crazyflie()
cf.console.receivedChar.add_callback(lambda text: print(text, end='', flush=True))
cf.link_established.add_callback(lambda uri: print("LINK ESTABLISHED", uri))
cf.connected.add_callback(lambda uri: print("CONNECTED", uri))
cf.fully_connected.add_callback(lambda uri: print("FULLY CONNECTED", uri))
cf.connection_failed.add_callback(lambda uri, msg: print("FAILED", msg))
cf.connection_lost.add_callback(lambda uri, msg: print("LOST", msg))
cf.open_link("radio://0/80/2M")

time.sleep(20)
cf.close_link()
print("done")