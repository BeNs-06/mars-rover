import pytest

from mars_rover.direction import Direction, movement_delta, turn_left, turn_right


@pytest.mark.parametrize(
    "start, expected",
    [
        (Direction.NORTH, Direction.WEST),
        (Direction.WEST, Direction.SOUTH),
        (Direction.SOUTH, Direction.EAST),
        (Direction.EAST, Direction.NORTH),
    ],
)
def test_turn_left(start, expected):
    assert turn_left(start) is expected


@pytest.mark.parametrize(
    "start, expected",
    [
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST, Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST, Direction.NORTH),
    ],
)
def test_turn_right(start, expected):
    assert turn_right(start) is expected


@pytest.mark.parametrize(
    "direction, expected_delta",
    [
        (Direction.NORTH, (0, 1)),
        (Direction.EAST, (1, 0)),
        (Direction.SOUTH, (0, -1)),
        (Direction.WEST, (-1, 0)),
    ],
)
def test_movement_delta(direction, expected_delta):
    assert movement_delta(direction) == expected_delta


def test_four_left_turns_are_a_full_circle():
    direction = Direction.NORTH
    for _ in range(4):
        direction = turn_left(direction)
    assert direction is Direction.NORTH
