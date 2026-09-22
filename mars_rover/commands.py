from __future__ import annotations

from enum import Enum


class Command(Enum):
    MOVE_FORWARD = "M"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"


class InvalidCommandError(ValueError):
    pass


_COMMANDS_BY_LETTER = {command.value: command for command in Command}


def parse_commands(raw_commands: str) -> list[Command]:
    commands = []
    for letter in raw_commands.strip().upper():
        try:
            commands.append(_COMMANDS_BY_LETTER[letter])
        except KeyError as exc:
            raise InvalidCommandError(f"Commande inconnue : {letter!r}") from exc
    return commands
