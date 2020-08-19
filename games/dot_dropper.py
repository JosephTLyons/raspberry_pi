#!/usr/bin/env python3

import time


from enum import Enum, auto, unique
from random import randint
from sense_hat import SenseHat


@unique
class Window(Enum):
    COLOR_PALETTE = auto()
    CANVAS = auto()
    TOOL = auto()
    BRUSH_SIZE = auto()


@unique
class Tool(Enum):
    BRUSH = auto()
    ERASER = auto()


@unique
class BrushSize(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


# Can this be made into an enum?
class Color:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)


# Can this be made into an enum?
class JoystickAction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class ColorGenerator:
    @staticmethod
    def make_random_color():
        return [randint(0, 255) for _ in range(3)]

    @classmethod
    def make_random_color_list(cls, number_of_colors):
        return [cls.make_random_color() for _ in range(number_of_colors)]


class Main:
    def __init__(self):
        self.window = Window.CANVAS

        self.drops = {}

        self.random_color_text = "random"

        self.selectable_colors = [self.random_color_text, Color.RED, Color.GREEN, Color.BLUE]
        self.selectable_colors_index = 0

        self.selectable_tools = [Tool.BRUSH, Tool.ERASER]
        self.selectable_tools_index = 0

        self.selectable_brush_sizes = [BrushSize.SMALL, BrushSize.MEDIUM, BrushSize.LARGE]
        self.selectable_brush_sizes_index = 0

        self.current_coordinates = [0, 0]

        self.current_color = Color.GREEN
        self.current_tool = Tool.BRUSH
        self.current_brush_size = BrushSize.SMALL

        self.current_brush_size = self.selectable_brush_sizes[0]

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
        self.sense.set_pixel(coordinates[0], coordinates[1], color)


    def add_pixel_safe(self, coordinates, color):
        for i in range(len(coordinates)):
            self.current_coordinates[i] %= 8

        self.add_pixel(coordinates, color)

    def handle_joystick(self, event):
        if event.action == "pressed":
            if self.window == Window.CANVAS:
                self.handle_joystick_in_cavas(event)
            elif self.window == Window.COLOR_PALETTE:
                self.handle_joystick_in_color_palette(event)
            elif self.window == Window.TOOL:
                self.handle_joystick_in_tool(event)
            elif self.window == Window.BRUSH_SIZE:
                self.handle_joystick_in_brush_size(event)

            self.refresh_ui()

    def handle_joystick_in_cavas(self, event):
        if event.direction == JoystickAction.UP:
            if self.current_coordinates == [0, 0]:
                self.window = Window.COLOR_PALETTE
            elif self.current_coordinates == [1, 0]:
                self.window = Window.TOOL
            elif self.current_coordinates == [2, 0]:
                self.window = Window.BRUSH_SIZE
            else:
                self.current_coordinates[1] -= 1
        elif event.direction == JoystickAction.DOWN:
            self.current_coordinates[1] += 1
        elif event.direction == JoystickAction.LEFT:
            self.current_coordinates[0] -= 1
        elif event.direction == JoystickAction.RIGHT:
            self.current_coordinates[0] += 1
        elif event.direction == JoystickAction.MIDDLE:
            self.update_drop_dict()

    def handle_joystick_in_color_palette(self, event):
        self.handle_joystick_in_menu_base(event, "current_color", "selectable_colors", "selectable_colors_index")

        if event.direction == JoystickAction.MIDDLE:
            if self.current_color == self.random_color_text:
                self.current_color = ColorGenerator.make_random_color()

    def handle_joystick_in_tool(self, event):
        self.handle_joystick_in_menu_base(event, "current_tool", "selectable_tools", "selectable_tools_index")

    def handle_joystick_in_brush_size(self, event):
        self.handle_joystick_in_menu_base(event, "current_brush_size", "selectable_brush_sizes", "selectable_brush_sizes_index")

    def handle_joystick_in_menu_base(self, event, current_item, selectable_items, selectable_item_index):
        index = getattr(self, selectable_item_index)
        items = getattr(self, selectable_items)

        if event.direction == JoystickAction.UP:
            index += 1

            last_index = len(items) - 1

            if index > last_index:
                index = last_index
        elif event.direction == JoystickAction.DOWN:
            if index == 0:
                self.window = Window.CANVAS
                return

            index -= 1
        elif event.direction == JoystickAction.MIDDLE:
            setattr(self, current_item, items[index])
            index = 0

            self.window = Window.CANVAS

        setattr(self, selectable_item_index, index)


    def update_drop_dict(self):
        current_coordinates_tuple = tuple(self.current_coordinates)

        if self.current_tool == Tool.ERASER and current_coordinates_tuple in self.drops:
            del self.drops[current_coordinates_tuple]
        elif self.current_tool == Tool.BRUSH:
            self.drops[current_coordinates_tuple] = self.current_color

        self.animate_drop()

    def animate_drop(self):
        if self.current_tool == Tool.BRUSH:
            self.add_pixel(self.current_coordinates, Color.BLUE)
        elif self.current_tool == Tool.ERASER:
            self.add_pixel(self.current_coordinates, Color.RED)

        time.sleep(0.1)
        self.add_pixel(self.current_coordinates, self.current_color)

    def refresh_ui(self):
        self.sense.clear()

        if self.window == Window.CANVAS:
            self.update_canvas_window()
        elif self.window == Window.COLOR_PALETTE:
            self.update_color_palette_window()
        elif self.window == Window.TOOL:
            self.update_tool_window()
        elif self.window == Window.BRUSH_SIZE:
            self.update_brush_size_window()

    def update_canvas_window(self):
        self.add_drops_to_ui()
        self.add_pixel_safe(self.current_coordinates, self.current_color)

    def update_color_palette_window(self):
        color_palette_window = []
        border_color = Color.WHITE

        for i in range(self.number_of_pixels_in_row):
            if i in [0, self.number_of_pixels_in_row - 1]:
                color_palette_window += [border_color] * self.number_of_pixels_in_row
            else:
                color_palette_window += [border_color]

                selectable_color = self.selectable_colors[self.selectable_colors_index]

                if selectable_color == self.random_color_text:
                    color_palette_window += ColorGenerator.make_random_color_list(6)
                else:
                    color_palette_window += [selectable_color] * 6

                color_palette_window += [border_color]

        self.sense.set_pixels(color_palette_window)

    def update_tool_window(self):
        selectable_tool = self.selectable_tools[self.selectable_tools_index]

        o = Color.BLACK

        tool_symbol = []

        if selectable_tool == Tool.BRUSH:
            b = Color.BLUE

            tool_symbol = [
                b, b, b, b, b, b, b, o,
                b, b, b, b, b, b, b, b,
                b, b, o, o, o, o, b, b,
                b, b, b, b, b, b, b, o,
                b, b, b, b, b, b, b, o,
                b, b, o, o, o, o, b, b,
                b, b, b, b, b, b, b, b,
                b, b, b, b, b, b, b, o,
            ]
        elif selectable_tool == Tool.ERASER:
            r = Color.RED

            tool_symbol = [
                r, r, r, r, r, r, r, r,
                r, r, r, r, r, r, r, r,
                r, r, o, o, o, o, o, o,
                r, r, r, r, r, r, r, r,
                r, r, r, r, r, r, r, r,
                r, r, o, o, o, o, o, o,
                r, r, r, r, r, r, r, r,
                r, r, r, r, r, r, r, r,
            ]

        self.sense.set_pixels(tool_symbol)

    def update_brush_size_window(self):
        if self.current_brush_size == BrushSize.SMALL:
            self.sense.set_pixel(0, 0, self.current_color)
        elif self.current_brush_size == BrushSize.MEDIUM:

            self.sense.set_pixels(0, 0, self.current_color)
        elif self.current_brush_size == BrushSize.LARGE:
            pass

    def add_drops_to_ui(self):
        for drop_coordinate, drop_color in self.drops.items():
            self.add_pixel(drop_coordinate, drop_color)


if __name__ == "__main__":
    main = Main()
    main.run()


# Shake to erase whole thing? (make sure to keep main dot where it is at)
# Double tap to exit or press and hold?
# Should I be using the while true?
# Move other classes / enums to their own files?
# Move project to its own repo and rename it to something else?
# Maybe extend it to be able to do animations as well (sprites)
# Color the erase and brush animations dynamically so that the animations are never the same as the current color
# Should the current color change based on what the current color is on top of?  Or it could flicker
# Brush size menu, this will require the canvas actions to be reworked, brush size should affect the erase and the brush
# Brush shape menu
# Animations and having it run them
# Should the multiple menus be rolled into one menu and that menu have submenus for brushes, colors, and brush size?
