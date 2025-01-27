import json

import board
from adafruit_bno08x import BNO_REPORT_ROTATION_VECTOR
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_pca9685 import PCA9685
from busio import I2C
from numpy import (arccos, arctan2, array, isclose, ndarray, pi, sqrt, tile,
                   transpose)
from numpy.linalg import norm
from scipy.interpolate import interp1d
from scipy.spatial.transform import Rotation as R
from importlib import import_module

from Servo import Servo


class Quad:
    pwmhat = None
    imu = None
    config = {}

    l_chassis = 0
    w_chassis = 0
    l_shoulder = 0
    l_upper = 0
    l_lower = 0
    r_foot = 0
    legs = {}
    h_rest = 0
    rest_pos = 0
    h_step = 0
    T = 1  # Step period

    orientation = R.identity()

    def __init__(self, configfile: str):
        try:
            i2c = I2C(board.SCL, board.SDA)
            self.pwmhat = PCA9685(i2c)
            self.pwmhat.frequency = 50
            self.imu = BNO08X_I2C(i2c)
            self.imu.enable_feature(BNO_REPORT_ROTATION_VECTOR)
        except:
            pass

        self.config = import_module(configfile).config
        config = self.config

        self.l_chassis = config["l_chassis"]
        self.w_chassis = config["w_chassis"]
        self.l_shoulder = config["l_shoulder"]
        self.l_upper = config["l_upper"]
        self.l_lower = config["l_lower"]
        self.r_foot = config["r_foot"]
        for name, options in config["servos"].items():
            if name[:2] not in self.legs:
                self.legs[name[:2]] = {}
            self.legs[name[:2]][name[2:3]] = Servo(
                self.pwmhat, options["port"], options["pwm_vals"], options["ang_vals"])
        self.h_rest = sqrt(self.l_upper**2+self.l_lower**2)
        self.rest_pos = array([0, self.l_shoulder, self.h_rest])
        self.h_step = self.h_rest*0.5

    def pos_to_angles(self, pos: ndarray):
        x, y, z = transpose(pos)
        z -= self.r_foot
        alpha = arctan2(z, y)-arccos(self.l_shoulder/sqrt(z**2+y**2))
        z = sqrt(z**2+y**2-self.l_shoulder**2)
        beta = arctan2(z, x)-arccos((self.l_upper**2+x**2+z**2-self.l_lower**2) /
                                    (2*self.l_upper*sqrt(x**2+z**2)))
        gamma = arccos((self.l_upper**2+self.l_lower**2-x**2-z**2) /
                       (2*self.l_upper*self.l_lower))
        return array([alpha, beta, gamma]).T

    # Returns positions of the feet along the walking trajectory

    def walk_positions(self, v: ndarray, t: ndarray):
        d = norm(v)  # Travel distance
        if isclose(d, 0.0):
            if type(t) == ndarray:
                return tile(self.rest_pos, (t.size, 4, 1))
            return tile(self.rest_pos, (4, 1))
        dx, dy = v*self.T  # Travel distance in x and y

        # points on step trajectory
        p1 = self.rest_pos
        p2 = array([0.0, 0.0, -self.h_step])+self.rest_pos
        p3 = array([-dx, dy, 0.0])+self.rest_pos

        # interpolation function
        p = interp1d([0.0, self.T/4, self.T/2, self.T],
                     [p1, p2, p3, p1], axis=0)

        time = array([t, (t+self.T/2), (t+self.T/2), t]) % self.T

        # LF, RF, LB, RB
        return p(time)

    def set_servos(self, angles):
        legmap = ['LF', 'RF', 'LB', 'RB']
        servomap = "SUL"
        for leg_name, servo_angles in zip(legmap, angles):
            for servo_name, angle in zip(servomap, servo_angles):
                try:
                    self.legs[leg_name][servo_name].setpos(angle)
                except:
                    pass

    def stop(self):
        legmap = ['LF', 'RF', 'LB', 'RB']
        servomap = "SUL"
        for leg_name in legmap:
            for servo_name in servomap:
                try:
                    self.legs[leg_name][servo_name].stop()
                except:
                    pass

    def rest_state_angles(self):
        return array([[0]*4, [pi/4]*4, [pi/2]*4]).T

    def t_pose_angles(self):
        return array([[0]*4, [0]*4, [pi/2]*4]).T
