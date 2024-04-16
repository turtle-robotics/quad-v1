import json

import board
from adafruit_pca9685 import PCA9685
from adafruit_bno08x import BNO_REPORT_ROTATION_VECTOR
from adafruit_bno08x.i2c import BNO08X_I2C
from busio import I2C
from numpy import (arccos, arctan2, array, isclose, ndarray, sqrt, tile,
                   transpose)
from numpy.linalg import norm
from scipy.interpolate import interp1d
from scipy.spatial.transform import Rotation as R

from Servo import Servo

pwmhat = None
imu = None
try:
    i2c = I2C(board.SCL, board.SDA)
    pwmhat = PCA9685(i2c)
    pwmhat.frequency = 50
    imu = BNO08X_I2C(i2c)
    imu.enable_feature(BNO_REPORT_ROTATION_VECTOR)
    orientation = R.from_quat(imu.quaternion)
except:
    pass


l_shoulder = 29.5e-3
l_upper = 70.123e-3
l_lower = 61.97e-3
r_foot = 4.9e-3
h_rest = 0.8*sqrt(l_upper**2+l_lower**2)  # arbitrary

T = 1.0  # Step period
rest_pos = array([0.0, l_shoulder, h_rest])
h_step = h_rest*0.5

legs = {}

with open("servos.json") as f:
    servo_dict = json.load(f)
    for name, options in servo_dict.items():
        if name[:2] not in legs:
            legs[name[:2]] = {}
        legs[name[:2]][name[2:3]] = Servo(
            pwmhat, options["port"], options["pwm_vals"], options["ang_vals"])


# Position relative to the shoulder pivot
def pos_to_angles(pos: ndarray):
    x, y, z = transpose(pos)
    z -= r_foot
    alpha = arctan2(z, y)-arccos(l_shoulder/sqrt(z**2+y**2))
    z = sqrt(z**2+y**2-l_shoulder**2)
    beta = arctan2(z, x)-arccos((l_upper**2+x**2+z**2-l_lower**2) /
                                (2*l_upper*sqrt(x**2+z**2)))
    gamma = arccos((l_upper**2+l_lower**2-x**2-z**2) /
                   (2*l_upper*l_lower))
    return array([alpha, beta, gamma]).T


# Returns positions of the feet along the walking trajectory
def walk_positions(v: ndarray, t: ndarray, orientation=Rotation()):
    d = norm(v)*T  # Travel distance
    if isclose(d, 0.0):
        if type(t) == ndarray:
            return tile(rest_pos, (t.size, 4, 1))
        return tile(rest_pos, (4, 1))
    dx, dy = v*T  # Travel distance in x and y
    h = sqrt(h_step**2+d**2)  # Hypotinuse of step
    dist = h+d  # Second half of step distance
    t1 = (h/dist+1)*T/2  # time at end of hypotinuse

    # points on step trajectory
    p1 = rest_pos
    p2 = array([0.0, 0.0, -h_step])+rest_pos
    p3 = array([dx, dy, 0.0])+rest_pos

    # interpolation function
    p = interp1d([0.0, T/2, t1, T], [p1, p2, p3, p1], axis=0)

    time = array([t, (t+T/2), (t+T/2), t]) % T

    # LF, RF, LB, RB
    return p(time)


def set_servos(angles):
    legmap = ['LF', 'RF', 'LB', 'RB']
    servomap = "SUL"
    for leg_name, servo_angles in zip(legmap, angles):
        for servo_name, angle in zip(servomap, servo_angles):
            try:
                legs[leg_name][servo_name].setpos(angle)
            except:
                pass
