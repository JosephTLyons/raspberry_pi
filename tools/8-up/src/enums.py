#!/usr/bin/env python3

from enum import Enum, auto, unique


@unique
class BrushSize(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()


@unique
class Tool(Enum):
    BRUSH = auto()
    ERASER = auto()


@unique
class Window(Enum):
    COLOR_PALETTE = auto()
    CANVAS = auto()
    TOOL = auto()
    BRUSH_SIZE = auto()
