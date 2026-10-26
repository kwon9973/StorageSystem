import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import serial
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

import logging
logging.basicConfig(level=logging.INFO)

URI = 'radio://0/80/2M'
MAX_SPEED = 0.6                       # m/s, keep it low at first
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)   # or /dev/ttyACM0
cflib.crtp.init_drivers()

def read_stick():
    last = None
    # if ser.in_waiting > 0:
    #     try:
    #         # Read whatever lines are backed up, keeping only the newest line
    #         while ser.in_waiting:
    #             x, y, b = ser.readline().decode().strip().split(',')
    #             last = (float(x), float(y), int(b))
    #     except (ValueError, IndexError):
    #         pass
    # return last

    while ser.in_waiting:             # keep only the newest line
        try:
            x, y, b = ser.readline().decode().strip().split(',')
            last = (float(x), float(y), int(b))
        except ValueError:
            pass
    return last

with SyncCrazyflie(URI) as scf:
    print("Connected Waiting for Flow Deck tracking stabilization...")
    with MotionCommander(scf, default_height=0.4) as mc:   # takes off by itself
        print("airborne Handshake stable, receiving serial inputs..")
        stamp = time.time()
        vx = vy = 0.0
        while True:
            s = read_stick()
            if s:
                x, y, btn = s
                stamp = time.time()
                if btn:
                    break                                  # press the stick = land
                vx, vy = y * MAX_SPEED, -x * MAX_SPEED    # flip signs if it feels backwards
            idle = time.time() - stamp
            if idle > 2:
                break                                      # no stick data for 2 s: land
            if idle > 0.3:
                vx = vy = 0.0                              # data stopped: hover
            mc.start_linear_motion(vx, vy, 0)
            time.sleep(0.05)