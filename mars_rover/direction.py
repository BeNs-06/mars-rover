from __future__ import annotations

from enum import Enum


class Direction(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


_CLOCKWISE_ORDER = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

_MOVEMENT_DELTA = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0),
}


def turn_left(direction: Direction) -> Direction:
    index = _CLOCKWISE_ORDER.index(direction)
    return _CLOCKWISE_ORDER[(index - 1) % len(_CLOCKWISE_ORDER)]


def turn_right(direction: Direction) -> Direction:
    index = _CLOCKWISE_ORDER.index(direction)
    return _CLOCKWISE_ORDER[(index + 1) % len(_CLOCKWISE_ORDER)]


def movement_delta(direction: Direction) -> tuple[int, int]:
    return _MOVEMENT_DELTA[direction]
