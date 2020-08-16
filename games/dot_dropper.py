#!/usr/bin/env python3

import time

from random import randint
from sense_hat import SenseHat


sense = SenseHat()
sense.clear()


green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
off = (0, 0, 0)
current_coordinates = [0, 0]
drops = {}


def add_pixel(coordinates, color):
    for i in range(len(current_coordinates)):
        current_coordinates[i] %= 8

    sense.set_pixel(coordinates[0], coordinates[1], color)


def add_drops():
    for drop_coordinate, drop_color in drops.items():
        if current_coordinates == drop_coordinate:
            color = green
        else:
            color = drop_color

        add_pixel(drop_coordinate, color)


def animate_drop():
    add_pixel(current_coordinates, red)
    time.sleep(0.1)
    add_pixel(current_coordinates, green)


def handle_drops():
    current_coordinates_tuple = tuple(current_coordinates)

    if current_coordinates_tuple in drops:
        del drops[current_coordinates_tuple]
    else:
        drops[current_coordinates_tuple] = [randint(0, 255) for _ in range(3)]

    animate_drop()


def build():
    add_drops()
    add_pixel(current_coordinates, green)


def handle_joystick(event):
    if event.action == "pressed":
        sense.clear()

        if event.direction == "up":
            current_coordinates[1] -= 1
        elif event.direction == "down":
            current_coordinates[1] += 1
        elif event.direction == "left":
            current_coordinates[0] -= 1
        elif event.direction == "right":
            current_coordinates[0] += 1
        elif event.direction == "middle":
            handle_drops()

        build()


sense.stick.direction_any = handle_joystick

add_pixel(current_coordinates, green)

while True:
    time.sleep(1)


# Shake to erase whole thing? (make sure to keep main dot where it is at)
# Double tap to exit or press and hold?
