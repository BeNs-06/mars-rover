from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Sequence


class CellState(Enum):
    FREE = auto()
    OBSTACLE = auto()


class InvalidMapError(ValueError):
    pass


_SYMBOL_TO_STATE = {
    "🟩": CellState.FREE,
    "🟫": CellState.FREE,
    "🌳": CellState.OBSTACLE,
    "🪨": CellState.OBSTACLE,
}


def _symbol_to_state(symbol: str) -> CellState:
    try:
        return _SYMBOL_TO_STATE[symbol]
    except KeyError as exc:
        raise InvalidMapError(f"Symbole de carte inconnu : {symbol!r}") from exc


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
    _cells: tuple[tuple[CellState, ...], ...]

    def __post_init__(self) -> None:
        if not self._cells or not self._cells[0]:
            raise InvalidMapError("La carte doit contenir au moins une ligne et une colonne")
        width = len(self._cells[0])
        if any(len(row) != width for row in self._cells):
            raise InvalidMapError("Toutes les lignes de la carte doivent avoir la même largeur")

    @classmethod
    def from_rows(cls, rows: Sequence[str]) -> "PlanetMap":
        if not rows:
            raise InvalidMapError("La carte doit contenir au moins une ligne")
        # La première ligne saisie représente le haut de la carte (nord),
        # donc le y le plus élevé : on inverse l'ordre pour que l'axe y
        # croisse vers le haut, comme movement_delta(NORTH) == (0, 1).
        cells = tuple(
            tuple(_symbol_to_state(symbol) for symbol in row) for row in reversed(rows)
        )
        return cls(cells)

    @property
    def width(self) -> int:
        return len(self._cells[0])

    @property
    def height(self) -> int:
        return len(self._cells)

    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def is_free(self, position: Position) -> bool:
        if not self.is_within_bounds(position):
            return False
        return self._cells[position.y][position.x] is CellState.FREE


def parse_map(raw: str) -> PlanetMap:
    rows = raw.strip().splitlines()
    return PlanetMap.from_rows(rows)
