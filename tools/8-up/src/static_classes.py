#!/usr/bin/env python3

from random import randint


class Color:
    BLACK = (0, 0, 0)
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


class Letter:
    @staticmethod
    def get_b(color):
        o = Color.BLACK
        c = color

        letter = [
            c, c, c, c, c, c, c, o,
            c, c, c, c, c, c, c, c,
            c, c, o, o, o, o, c, c,
            c, c, c, c, c, c, c, o,
            c, c, c, c, c, c, c, o,
            c, c, o, o, o, o, c, c,
            c, c, c, c, c, c, c, c,
            c, c, c, c, c, c, c, o,
        ]

        return letter

    @staticmethod
    def get_e(color):
        o = Color.BLACK
        c = color

        letter = [
            c, c, c, c, c, c, c, c,
            c, c, c, c, c, c, c, c,
            c, c, o, o, o, o, o, o,
            c, c, c, c, c, c, c, c,
            c, c, c, c, c, c, c, c,
            c, c, o, o, o, o, o, o,
            c, c, c, c, c, c, c, c,
            c, c, c, c, c, c, c, c,
        ]

        return letter


class JoystickAction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
