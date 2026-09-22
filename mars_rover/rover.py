from __future__ import annotations

from dataclasses import dataclass

from .direction import Direction, movement_delta, turn_left, turn_right
from .planet_map import Position


@dataclass(frozen=True)
class Rover:
    position: Position
    direction: Direction

    def turned_left(self) -> "Rover":
        return Rover(self.position, turn_left(self.direction))

    def turned_right(self) -> "Rover":
        return Rover(self.position, turn_right(self.direction))

    def next_position(self) -> Position:
        dx, dy = movement_delta(self.direction)
        return self.position.translated(dx, dy)

    def moved_to(self, position: Position) -> "Rover":
        return Rover(position, self.direction)

    def __str__(self) -> str:
        return f"{self.position}:{self.direction.value}"
