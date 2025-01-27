#! /usr/bin/env python3
import board
from busio import I2C
from adafruit_pca9685 import PCA9685
import code


i2c = I2C(board.SCL, board.SDA)

# Initialize PCA9685 PWM generator
pwmhat = PCA9685(i2c)
pwmhat.frequency = 50

print("pwmhat.channels[<channel>].duty_cycle = <duty cycle>")
code.interact(local=locals())
