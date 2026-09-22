from __future__ import annotations

from .commands import Command, parse_commands
from .planet_map import PlanetMap, Position
from .rover import Rover


class InvalidStartPositionError(ValueError):
    def __init__(self, position: Position):
        self.position = position
        super().__init__(
            f"Position de départ invalide en {position} "
            "(hors de la carte ou sur une case obstacle)"
        )


def run_mission(planet_map: PlanetMap, rover: Rover, raw_commands: str) -> Rover:
    if not planet_map.is_free(rover.position):
        raise InvalidStartPositionError(rover.position)
    commands = parse_commands(raw_commands)

    for command in commands:
        if command is Command.TURN_LEFT:
            rover = rover.turned_left()
        elif command is Command.TURN_RIGHT:
            rover = rover.turned_right()
        elif command is Command.MOVE_FORWARD:
            next_position = rover.next_position()
            if planet_map.is_free(next_position):
                rover = rover.moved_to(next_position)
    return rover
