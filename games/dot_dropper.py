#!/usr/bin/env python3

import time


from enum import Enum, auto, unique
from random import randint
from sense_hat import SenseHat


sense = SenseHat()
sense.clear()


@unique
class Window(Enum):
    COLOR_PALETTE = auto()
    CANVAS = auto()


window = Window.CANVAS


green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
off = (0,) * 3
white = (255,) * 3


current_coordinates = [0, 0]
current_color = green


drops = {}


selectable_color_index = 0
selectable_colors = [green, blue, red]
shown = selectable_colors[0]


def update_color_palette_window():
    color_palette_window = [
        white, white, white, white, white, white, white, white,
        white, shown, shown, shown, shown, shown, shown, white,
        white, shown, shown, shown, shown, shown, shown, white,
        white, shown, shown, shown, shown, shown, shown, white,
        white, shown, shown, shown, shown, shown, shown, white,
        white, shown, shown, shown, shown, shown, shown, white,
        white, shown, shown, shown, shown, shown, shown, white,
        white, white, white, white, white, white, white, white,
    ]

    sense.set_pixels(color_palette_window)


def add_pixel(coordinates, color):
    for i in range(len(current_coordinates)):
        current_coordinates[i] %= 8

    sense.set_pixel(coordinates[0], coordinates[1], color)


def add_drops_to_ui():
    for drop_coordinate, drop_color in drops.items():
        add_pixel(drop_coordinate, drop_color)


def animate_drop():
    add_pixel(current_coordinates, red)
    time.sleep(0.1)
    add_pixel(current_coordinates, current_color)


def update_drop_dict():
    current_coordinates_tuple = tuple(current_coordinates)

    if current_coordinates_tuple in drops:
        del drops[current_coordinates_tuple]
    else:
        if current_color:
            color = current_color
        else:
            color = [randint(0, 255) for _ in range(3)]

        drops[current_coordinates_tuple] = color

    animate_drop()


def refresh_ui():
    sense.clear()

    if window == Window.CANVAS:
        add_drops_to_ui()
        add_pixel(current_coordinates, current_color)
    elif window == Window.COLOR_PALETTE:
        update_color_palette_window()


def handle_joystick_in_cavas(event):
    if event.direction == "up":
        if current_coordinates == [0, 0]:
            global window
            window = Window.COLOR_PALETTE
        else:
            current_coordinates[1] -= 1
    elif event.direction == "down":
        current_coordinates[1] += 1
    elif event.direction == "left":
        current_coordinates[0] -= 1
    elif event.direction == "right":
        current_coordinates[0] += 1
    elif event.direction == "middle":
        update_drop_dict()


def handle_joystick_in_color_palette(event):
    global selectable_color_index

    if event.direction in ["up", "down"]:
        if event.direction == "up":
            selectable_color_index += 1
        elif event.direction == "down":
            selectable_color_index -= 1

        last_index = len(selectable_colors) - 1

        if selectable_color_index < 0:
            selectable_color_index = 0
        elif selectable_color_index > last_index:
            selectable_color_index = last_index

        global shown
        shown = selectable_colors[selectable_color_index]
        print(selectable_color_index)
    elif event.direction == "middle":
        global current_color

        current_color = selectable_colors[selectable_color_index]
        selectable_color_index = 0

        global window
        window = Window.CANVAS


def handle_joystick(event):
    if event.action == "pressed":
        if window == Window.CANVAS:
            handle_joystick_in_cavas(event)
        elif window == Window.COLOR_PALETTE:
            handle_joystick_in_color_palette(event)

        refresh_ui()


sense.stick.direction_any = handle_joystick
add_pixel(current_coordinates, current_color)


while True:
    time.sleep(1)


# Shake to erase whole thing? (make sure to keep main dot where it is at)
# Double tap to exit or press and hold?
# Should I be using the while true?
