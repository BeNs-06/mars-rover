from __future__ import annotations

from .commands import Command, parse_commands
from .planet_map import PlanetMap, Position
from .rover import Rover


class OutOfBoundsError(Exception):
    def __init__(self, rover: Rover, attempted_position: Position):
        self.rover = rover
        self.attempted_position = attempted_position
        super().__init__(
            f"Le rover ne peut pas sortir de la carte en {attempted_position} "
            f"(dernière position valide : {rover})"
        )


def run_mission(planet_map: PlanetMap, rover: Rover, raw_commands: str) -> Rover:
    for command in parse_commands(raw_commands):
        if command is Command.TURN_LEFT:
            rover = rover.turned_left()
        elif command is Command.TURN_RIGHT:
            rover = rover.turned_right()
        elif command is Command.MOVE_FORWARD:
            next_position = rover.next_position()
            if not planet_map.is_within_bounds(next_position):
                raise OutOfBoundsError(rover, next_position)
            rover = rover.moved_to(next_position)
    return rover
