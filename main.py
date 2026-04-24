from machine import I2C, Pin
import time
import sys
from pca9685 import PCA9685   # save driver as pca9685.py

# ---------- I2C SETUP ----------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

pca = PCA9685(i2c)
pca.frequency = 50  # Servo frequency

# ---------- SERVO SETTINGS ----------
SERVO_MIN = 1500   # pulse length for 0°
SERVO_MAX = 6000   # pulse length for 180°

servo_channels = [0, 1, 2, 3, 4]  # Thumb → Pinky

def set_servo_angle(channel, angle):
    angle = max(0, min(180, angle))
    pulse = int(SERVO_MIN + (angle / 180) * (SERVO_MAX - SERVO_MIN))
    pca.channels[channel].duty_cycle = pulse

print("✅ PCA9685 5-Servo Hand Ready")

# ---------- SERIAL CONTROL ----------
# Send: 90,45,120,30,0
while True:
    try:
        line = sys.stdin.readline().strip()
        if not line:
            continue

        angles = line.split(',')
        if len(angles) != 5:
            print("❌ Send 5 angles only")
            continue

        angles = [int(a) for a in angles]

        for i in range(5):
            set_servo_angle(servo_channels[i], angles[i])

        print("✔ Angles set:", angles)

    except Exception as e:
        print("Error:", e)
