#!/usr/bin/env python3

import time


from copy import deepcopy
from enums import BrushSize, Tool, Window
from sense_hat import SenseHat
from signal import pause
from static_classes import Color, ColorGenerator, JoystickAction, Letter


class Main:
    def __init__(self):
        self.window = Window.CANVAS

        self.drops = {}

        self.random_color_text = "random"

        # See about getting a list of these like we're doing with the enums
        self.selectable_colors = [self.random_color_text, Color.RED, Color.GREEN, Color.BLUE]
        self.selectable_colors_index = 0

        self.selectable_tools = [tool for tool in Tool]
        self.selectable_tools_index = 0

        self.selectable_brush_sizes = [brush_size for brush_size in BrushSize]
        self.selectable_brush_sizes_index = 0

        self.origin = [0, 0]

        self.current_coordinates = deepcopy(self.origin)
        self.current_color = self.selectable_colors[2]
        self.current_tool = self.selectable_tools[0]
        self.current_brush_size = self.selectable_brush_sizes[0]

        self.sense = SenseHat()
        self.sense.stick.direction_any = self.handle_joystick

        self.number_of_pixels_in_row = 8

    def run(self):
        self.sense.clear()
        self.print_brush(self.current_coordinates, self.current_brush_size.value, self.current_color)

        pause()

    def print_brush(self, coordinates, width, color):
        for i in range(coordinates[1], coordinates[1] + width):
            for j in range(coordinates[0], coordinates[0] + width):
                self.sense.set_pixel(j, i, color)

    def adjust_brush_position(self, coordinates):
        for i in range(len(coordinates)):
            if coordinates[i] < 0:
                coordinates[i] = self.number_of_pixels_in_row - self.current_brush_size.value
            elif coordinates[i] + self.current_brush_size.value > self.number_of_pixels_in_row:
                coordinates[i] = 0

    def handle_joystick(self, event):
        if event.action == "pressed":
            if self.window == Window.CANVAS:
                self.handle_joystick_in_canvas(event)
            elif self.window == Window.COLOR_PALETTE:
                self.handle_joystick_in_color_palette(event)
            elif self.window == Window.TOOL:
                self.handle_joystick_in_tool(event)
            elif self.window == Window.BRUSH_SIZE:
                self.handle_joystick_in_brush_size(event)

            self.refresh_ui()

    def has_entered_menu(self):
        if self.current_coordinates == self.origin:
            self.window = Window.COLOR_PALETTE
        elif self.current_coordinates == [1, 0]:
            self.window = Window.TOOL
        elif self.current_coordinates == [2, 0]:
            self.window = Window.BRUSH_SIZE
        else:
            return False

        return True

    def handle_joystick_in_canvas(self, event):
        if event.direction == JoystickAction.UP:
            if not self.has_entered_menu():
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
        for i in range(self.current_coordinates[1], self.current_coordinates[1] + self.current_brush_size.value):
            for j in range(self.current_coordinates[0], self.current_coordinates[0] + self.current_brush_size.value):
                current_coordinates_tuple = j, i

                if self.current_tool == Tool.BRUSH:
                    self.drops[current_coordinates_tuple] = self.current_color
                elif self.current_tool == Tool.ERASER and current_coordinates_tuple in self.drops:
                    del self.drops[current_coordinates_tuple]

        self.animate_drops()

    def animate_drops(self):
        for i in range(self.current_coordinates[1], self.current_coordinates[1] + self.current_brush_size.value):
            for j in range(self.current_coordinates[0], self.current_coordinates[0] + self.current_brush_size.value):
                if self.current_tool == Tool.BRUSH:
                    self.sense.set_pixel(j, i, Color.BLUE)
                elif self.current_tool == Tool.ERASER:
                    self.sense.set_pixel(j, i, Color.RED)

        time.sleep(0.1)

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
        self.adjust_brush_position(self.current_coordinates)
        self.print_brush(self.current_coordinates, self.current_brush_size.value, self.current_color)

    def update_color_palette_window(self):
        color_palette_window = []
        border_color = Color.WHITE

        for _ in range(self.number_of_pixels_in_row):
            if _ in [0, self.number_of_pixels_in_row - 1]:
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

        if selectable_tool == Tool.BRUSH:
            tool_symbol = Letter.get_b(Color.BLUE)
        elif selectable_tool == Tool.ERASER:
            tool_symbol = Letter.get_e(Color.RED)
        else:
            tool_symbol = Letter.get_e(Color.GREEN)

        self.sense.set_pixels(tool_symbol)

    def update_brush_size_window(self):
        selectable_brush_size = self.selectable_brush_sizes[self.selectable_brush_sizes_index]
        self.print_brush(self.origin, selectable_brush_size.value, self.current_color)

    def add_drops_to_ui(self):
        for drop_coordinate, drop_color in self.drops.items():
            self.sense.set_pixel(drop_coordinate[0], drop_coordinate[1], drop_color)


if __name__ == "__main__":
    main = Main()
    main.run()
