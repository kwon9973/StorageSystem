import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import time
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M'
cflib.crtp.init_drivers()


with SyncCrazyflie(URI) as scf:
    scf.cf.supervisor.send_arming_request(True)

    mc = MotionCommander(scf, default_height=0.4)
    mc.take_off()
    time.sleep(3)    # hover for 3 seconds
    mc.land()
