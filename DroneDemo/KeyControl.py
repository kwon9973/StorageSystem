import curses
import time

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M'
SPEED = 0.3     # m/s
YAW_RATE = 60   # deg/s
HOLD = 0.3      # seconds a keypress keeps the motion going

KEYS = {  # key: (vx, vy, vz, yaw_rate)
    ord('w'): (SPEED, 0, 0, 0),      # forward
    ord('s'): (-SPEED, 0, 0, 0),     # back
    ord('a'): (0, SPEED, 0, 0),      # left
    ord('d'): (0, -SPEED, 0, 0),     # right
    ord('r'): (0, 0, SPEED, 0),      # up
    ord('f'): (0, 0, -SPEED, 0),     # down
    ord('q'): (0, 0, 0, YAW_RATE),   # turn left
    ord('e'): (0, 0, 0, -YAW_RATE),  # turn right
}

def fly(stdscr):
    stdscr.nodelay(True)  # getch() returns -1 instead of waiting
    stdscr.addstr(0, 0, "w/s a/d r/f q/e = move    x = land and quit")
    cmd, last = (0, 0, 0, 0), 0.0
    with SyncCrazyflie(URI) as scf:
        with MotionCommander(scf, default_height=0.4) as mc:  # takes off
            while True:
                key = -1
                while (k := stdscr.getch()) != -1:  # drain buffered keys, keep the latest
                    key = k
                if key == ord('x'):
                    break
                if key in KEYS:
                    cmd, last = KEYS[key], time.time()
                elif time.time() - last > HOLD:
                    cmd = (0, 0, 0, 0)  # no recent key: hover in place
                mc.start_linear_motion(*cmd)
                time.sleep(0.05)
        # leaving the block lands it

cflib.crtp.init_drivers()
curses.wrapper(fly)