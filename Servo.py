from adafruit_pca9685 import PCA9685
from numpy import argmax, argmin, array, isnan
from scipy.interpolate import interp1d


class Servo:
    interp_fun: callable
    port: int
    pwmhat: PCA9685

    def __init__(self, pwmhat: PCA9685, port: int, pwm_vals: list, ang_vals: list):
        self.pwmhat = pwmhat
        self.port = port
        arr = array([ang_vals, pwm_vals]).T
        arr.sort(0)
        ang_vals, pwm_vals = arr.T
        self.interp_fun = interp1d(ang_vals, pwm_vals,
                                   bounds_error=False,
                                   fill_value=(pwm_vals[argmin(ang_vals)], pwm_vals[argmax(ang_vals)]))

    def setpos(self, position: float):
        if isnan(position) or self.port == -1:
            return
        duty_cycle = int(self.interp_fun(position))
        if self.pwmhat:
            self.pwmhat.channels[self.port].duty_cycle = duty_cycle
        else:
            print(f"Servo {self.port} set to {duty_cycle}")

    def stop(self):
        if self.pwmhat:
            self.pwmhat.channels[self.port].duty_cycle = 0
        else:
            print(f"Servo {self.port} stopped")
