#!/usr/bin/env python3

from random import randint


class Color:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)


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
