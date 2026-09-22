from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def translated(self, dx: int, dy: int) -> "Position":
        return Position(self.x + dx, self.y + dy)

    def __str__(self) -> str:
        return f"{self.x}:{self.y}"


@dataclass(frozen=True)
class PlanetMap:
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("La carte doit avoir une largeur et une hauteur positives")

    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height
