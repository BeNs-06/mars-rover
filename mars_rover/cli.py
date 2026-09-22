from __future__ import annotations

import argparse
import sys

from .commands import InvalidCommandError
from .direction import Direction
from .planet_map import PlanetMap, Position
from .rover import Rover
from .simulator import OutOfBoundsError, run_mission


def _parse_direction(value: str) -> Direction:
    try:
        return Direction(value.upper())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Direction invalide : {value!r} (attendu N, E, S ou W)"
        ) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mars-rover",
        description="Simule le déplacement d'un rover sur Mars et affiche sa position finale.",
    )
    parser.add_argument("--width", type=int, required=True, help="Largeur de la carte")
    parser.add_argument("--height", type=int, required=True, help="Hauteur de la carte")
    parser.add_argument("--start-x", type=int, required=True, help="Position de départ (X)")
    parser.add_argument("--start-y", type=int, required=True, help="Position de départ (Y)")
    parser.add_argument(
        "--start-direction",
        type=_parse_direction,
        required=True,
        help="Direction de départ (N, E, S ou W)",
    )
    parser.add_argument("commands", help="Liste de commandes, ex: 'MMRMLM'")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        planet_map = PlanetMap(args.width, args.height)
    except ValueError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1

    start_position = Position(args.start_x, args.start_y)
    if not planet_map.is_within_bounds(start_position):
        print(
            f"Erreur : la position de départ {start_position} est hors de la carte.",
            file=sys.stderr,
        )
        return 1

    rover = Rover(start_position, args.start_direction)

    try:
        final_rover = run_mission(planet_map, rover, args.commands)
    except (InvalidCommandError, OutOfBoundsError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1

    print(final_rover)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
