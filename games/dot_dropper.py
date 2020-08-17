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
random_text = "random"
selectable_colors = [red, green, blue, random_text]


def make_random_color():
    return [randint(0, 255) for _ in range(3)]


def update_color_palette_window():
    color_palette_window =[]
    border_color = white

    for i in range(8):
        if i in [0, 7]:
            color_palette_window += [border_color] * 8
        else:
            color_palette_window += [border_color]

            color_option = selectable_colors[selectable_color_index]

            if color_option == random_text:
                color_palette_window += [make_random_color() for _ in range(6)]
            else:
                color_palette_window += [color_option] * 6

            color_palette_window += [border_color]

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
        drops[current_coordinates_tuple] = current_color

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
    global window

    if event.direction in ["up", "down"]:
        if event.direction == "up":
            selectable_color_index += 1

            last_index = len(selectable_colors) - 1

            if selectable_color_index > last_index:
                selectable_color_index = last_index
        elif event.direction == "down":
            if selectable_color_index == 0:
                window = Window.CANVAS
                return

            selectable_color_index -= 1
    elif event.direction == "middle":
        global current_color

        current_color = selectable_colors[selectable_color_index]

        if current_color == random_text:
            current_color = make_random_color()

        selectable_color_index = 0
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
    # temp_current_color = current_color
    # time.sleep(0.25)
    # current_color = off
    # refresh_ui()
    # time.sleep(0.25)
    # current_color = temp_current_color
    # refresh_ui()
    time.sleep(1)


# Shake to erase whole thing? (make sure to keep main dot where it is at)
# Double tap to exit or press and hold?
# Should I be using the while true?
