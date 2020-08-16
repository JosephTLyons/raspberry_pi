#!/usr/bin/env python3

from sense_hat import SenseHat
import time

sense = SenseHat()

sense.clear()
sense.set_rotation(270)

o = [0, 0, 0]
r = [255, 0, 0]

red_minus = [
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
]

g = [0, 255, 0]

green_plus = [
    o, o, o, g, g, o, o, o,
    o, o, o, g, g, o, o, o,
    o, o, o, g, g, o, o, o,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    o, o, o, g, g, o, o, o,
    o, o, o, g, g, o, o, o,
    o, o, o, g, g, o, o, o,
]

b = [0, 0, 255]

blue_x = [
    b, b, o, o, o, o, b, b,
    b, b, b, o, o, b, b, b,
    o, b, b, b, b, b, b, o,
    o, o, b, b, b, b, o, o,
    o, o, b, b, b, b, o, o,
    o, b, b, b, b, b, b, o,
    b, b, b, o, o, b, b, b,
    b, b, o, o, o, o, b, b,
]

# sleep_in_seconds = 0.1
# images = [green_plus, red_minus, blue_x]

# for _ in range(4):
#     for image in images:
#         sense.set_pixels(image)
#         time.sleep(sleep_in_seconds)
#         sense.clear()
#         time.sleep(sleep_in_seconds)

# ==================================


# colors = [(0, 0, 255), (0, 0, 0), (0, 255, 0), (0, 0, 0)]

# while True:
#     for color in colors:
#         sense.set_pixel(2, 2, color)
#         time.sleep(0.2)

# ==================================

# def celsius_to_fahrenheit(c):
#     return (c * (9/5) + 32)


# while True:
#     temp = int(celsius_to_fahrenheit(sense.get_temperature()))
#     sense.show_message(str(temp))
#     print(temp)
#     time.sleep(1)


while True:
    acceleration = sense.get_accelerometer_raw()

    x = acceleration["x"]
    y = acceleration["y"]
    z = acceleration["z"]

    x = round(x, 1)
    y = round(y, 1)
    z = round(z, 1)

    print("{x}, {y}, {z}".format(x=x, y=y, z=z))
    time.sleep(0.25)
