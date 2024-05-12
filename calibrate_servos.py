import json
from math import pi
import board
from busio import I2C
import adafruit_pca9685
import re

i2c = I2C(board.SCL, board.SDA)
pwmhat = adafruit_pca9685.PCA9685(i2c)
pwmhat.frequency = 50

config = {}
try:
    with open("servos.json", "r") as file:
        config = json.load(file)
except:
    print("Could not open servos.json")
    pass


def save():
    with open("servos.json", "w") as file:
        json.dump(config, file)


# atexit.register(onexit)

servo_name = ""
servo_port = 0
angle = 0
pwm_val = 0

while True:
    inp = input(f"[{servo_name} P{servo_port} A:{angle}π pwm:{pwm_val}]: ")
    if inp == "s":
        save()
    elif inp == "a":
        config[servo_name]["pwm_vals"] += [pwm_val]
        config[servo_name]["ang_vals"] += [angle]
    elif inp == "d":
        print(config[servo_name])
    elif inp == "c":
        config[servo_name] = {"port": 0, "pwm_vals": [], "ang_vals": []}
    # elif re.match("(L|R)(F|B)(S|U|L)", inp):
    #     print(f"matched name: {inp}")
    #     servo_name = inp
    #     if not servo_name in config:
    #         config[servo_name] = {"port": 0, "pwm_vals": [], "ang_vals": []}
    elif re.match("P[0-9]+", inp):
        servo_port = int(inp[1:])
        print(f"matched port: {servo_port}")
        # config[servo_name]["port"] = servo_port
    # elif re.match("A[-+]?\d*[.,]\d+|\d+", inp):
    #     angle = float(inp[1:])*pi
    elif re.match("\d+", inp):
        pwm_val = int(inp)
        pwmhat.channels[servo_port].duty_cycle = pwm_val
