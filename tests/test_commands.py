import pytest

from mars_rover.commands import Command, InvalidCommandError, parse_commands


def test_parse_commands_maps_letters_to_commands():
    assert parse_commands("MLR") == [
        Command.MOVE_FORWARD,
        Command.TURN_LEFT,
        Command.TURN_RIGHT,
    ]


def test_parse_commands_is_case_insensitive():
    assert parse_commands("mlr") == [
        Command.MOVE_FORWARD,
        Command.TURN_LEFT,
        Command.TURN_RIGHT,
    ]


def test_parse_commands_ignores_surrounding_whitespace():
    assert parse_commands("  MM  ") == [Command.MOVE_FORWARD, Command.MOVE_FORWARD]


def test_parse_commands_rejects_unknown_letter():
    with pytest.raises(InvalidCommandError):
        parse_commands("MX")
