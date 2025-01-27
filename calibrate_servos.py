from matplotlib import pyplot
import json
import time
import board
from busio import I2C
from adafruit_pca9685 import PCA9685
from adafruit_ads7830.ads7830 import ADS7830
from adafruit_ads7830.analog_in import AnalogIn
from pandas import DataFrame
from scipy.stats import linregress


i2c = I2C(board.SCL, board.SDA)

# Initialize PCA9685 PWM generator
pwmhat = PCA9685(i2c)
pwmhat.frequency = 50

# Initialize ADS7830 Analog-Digital Converter
adc = ADS7830(i2c)
chan = [AnalogIn(adc, channel) for channel in range(0, 7)]

config = []


def save():
    with open("servos.json", "w") as file:
        json.dump(config, file)


i = 0  # servo and adc port
data = []

pwmhat.channels[i].duty_cycle = 1500
time.sleep(2)
print("Testing")
for duty_cycle in range(1500, 8500, 20):
    print(duty_cycle, chan[i].value)
    pwmhat.channels[i].duty_cycle = duty_cycle
    data += [(duty_cycle, chan[i].value)]
    time.sleep(0.005)
pwmhat.channels[i].duty_cycle = 5000
df = DataFrame(data, columns=["duty_cycle", "adc"])
df.to_csv("servo_calibration.csv", index=False)

regression = linregress(df["adc"], df["duty_cycle"])
intercept = regression.intercept
slope = regression.slope
r2 = regression.rvalue**2

if (r2 < 0.9997):
    print("Trend is not liear enough (R^2 < 0.9997)")
    exit(1)

# with open("replayScript.json", "r+") as jsonFile:
#     data = json.load(jsonFile)

#     data[""]
#     data[""] = "NewPath"

#     jsonFile.seek(0)  # rewind
#     json.dump(data, jsonFile)
#     jsonFile.truncate()


print(slope, intercept, r2)

pyplot.plot(df["adc"], df["duty_cycle"])
pyplot.savefig("servo_map.jpg")
