#!/usr/bin/env python3

import time


from enum import Enum, auto, unique
from random import randint
from sense_hat import SenseHat


@unique
class Window(Enum):
    COLOR_PALETTE = auto()
    CANVAS = auto()
    TOOL_SELECTOR = auto()


@unique
class Tool(Enum):
    ERASER = auto()
    BRUSH = auto()


class Color:
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)


class ColorGenerator:
    @staticmethod
    def make_random_color():
        return [randint(0, 255) for _ in range(3)]

    @classmethod
    def make_random_color_list(cls, number_of_colors):
        return [cls.make_random_color() for _ in range(number_of_colors)]


# def update_tool():
#     color_option = selectable_colors[selectable_color_index]

#     if color_option == Color.BLACK:
#         current_tool = Tool.ERASER


# class Menu:
#     def __init__(self, menu_items):
#         self.menu_items = menu_items


class Main:
    def __init__(self):
        self.window = Window.CANVAS

        self.drops = {}

        self.random_color_text = "random"

        self.selectable_colors = [self.random_color_text, Color.RED, Color.GREEN, Color.BLUE]
        self.selectable_color_index = 0

        self.selectable_tools = [Tool.BRUSH, Tool.ERASER]
        self.selectable_tool_index = 0

        self.current_coordinates = [0, 0]
        self.current_color = Color.GREEN
        self.current_tool = Tool.BRUSH

        self.sense = SenseHat()
        self.sense.stick.direction_any = self.handle_joystick

        self.number_of_pixels_in_row = 8

    def run(self):
        self.sense.clear()
        self.add_pixel(self.current_coordinates, self.current_color)

        while True:
            # temp_current_color = current_color
            # time.sleep(0.25)
            # current_color = black
            # refresh_ui()
            # time.sleep(0.25)
            # current_color = temp_current_color
            # refresh_ui()
            time.sleep(1)

    def add_pixel(self, coordinates, color):
        for i in range(len(coordinates)):
            self.current_coordinates[i] %= 8

        self.sense.set_pixel(coordinates[0], coordinates[1], color)

    def handle_joystick(self, event):
        if event.action == "pressed":
            if self.window == Window.CANVAS:
                self.handle_joystick_in_cavas(event)
            elif self.window == Window.COLOR_PALETTE:
                self.handle_joystick_in_color_palette(event)
            elif self.window == Window.TOOL_SELECTOR:
                self.handle_joystick_in_tool_selector(event)

            self.refresh_ui()

    def handle_joystick_in_cavas(self, event):
        if event.direction == "up":
            if self.current_coordinates == [0, 0]:
                self.window = Window.COLOR_PALETTE
            elif self.current_coordinates == [1, 0]:
                self.window = Window.TOOL_SELECTOR
            else:
                self.current_coordinates[1] -= 1
        elif event.direction == "down":
            self.current_coordinates[1] += 1
        elif event.direction == "left":
            self.current_coordinates[0] -= 1
        elif event.direction == "right":
            self.current_coordinates[0] += 1
        elif event.direction == "middle":
            self.update_drop_dict()

    def handle_joystick_in_color_palette(self, event):
        if event.direction == "up":
            self.selectable_color_index += 1

            last_index = len(self.selectable_colors) - 1

            if self.selectable_color_index > last_index:
                self.selectable_color_index = last_index
        elif event.direction == "down":
            if self.selectable_color_index == 0:
                self.window = Window.CANVAS
                return

            self.selectable_color_index -= 1
        elif event.direction == "middle":
            self.current_color = self.selectable_colors[self.selectable_color_index]

            if self.current_color == self.random_color_text:
                self.current_color = ColorGenerator.make_random_color()

            self.selectable_color_index = 0
            self.window = Window.CANVAS

    def handle_joystick_in_tool_selector(self, event):
        # Refactor handle_joystick_in_color_palette to work with both color and tool menu
        pass

    def update_drop_dict(self):
        current_coordinates_tuple = tuple(self.current_coordinates)

        if self.current_tool == Tool.ERASER and current_coordinates_tuple in self.drops:
            del self.drops[current_coordinates_tuple]
        elif self.current_tool == Tool.BRUSH:
            self.drops[current_coordinates_tuple] = self.current_color

        self.animate_drop()

    def animate_drop(self):
        self.add_pixel(self.current_coordinates, Color.RED)
        time.sleep(0.1)
        self.add_pixel(self.current_coordinates, self.current_color)

    def refresh_ui(self):
        self.sense.clear()

        if self.window == Window.CANVAS:
            self.update_canvas()
        elif self.window == Window.COLOR_PALETTE:
            self.update_color_palette()
        elif self.window == Window.TOOL_SELECTOR:
            self.update_tool()

    def update_canvas(self):
        self.add_drops_to_ui()
        self.add_pixel(self.current_coordinates, self.current_color)

    def update_color_palette(self):
        color_palette_window =[]
        border_color = Color.WHITE

        for i in range(self.number_of_pixels_in_row):
            if i in [0, self.number_of_pixels_in_row - 1]:
                color_palette_window += [border_color] * self.number_of_pixels_in_row
            else:
                color_palette_window += [border_color]

                color_option = self.selectable_colors[self.selectable_color_index]

                if color_option == self.random_color_text:
                    color_palette_window += ColorGenerator.make_random_color_list(6)
                else:
                    color_palette_window += [color_option] * 6

                color_palette_window += [border_color]

        self.sense.set_pixels(color_palette_window)

    def add_drops_to_ui(self):
        for drop_coordinate, drop_color in self.drops.items():
            self.add_pixel(drop_coordinate, drop_color)


if __name__ == "__main__":
    main = Main()
    main.run()


# Shake to erase whole thing? (make sure to keep main dot where it is at)
# Double tap to exit or press and hold?
# Should I be using the while true?
