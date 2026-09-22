from mars_rover.direction import Direction
from mars_rover.planet_map import Position
from mars_rover.rover import Rover


def test_turned_left_changes_direction_only():
    rover = Rover(Position(1, 1), Direction.NORTH)
    turned = rover.turned_left()
    assert turned.position == rover.position
    assert turned.direction is Direction.WEST


def test_turned_right_changes_direction_only():
    rover = Rover(Position(1, 1), Direction.NORTH)
    turned = rover.turned_right()
    assert turned.position == rover.position
    assert turned.direction is Direction.EAST


def test_next_position_faces_north():
    rover = Rover(Position(1, 1), Direction.NORTH)
    assert rover.next_position() == Position(1, 2)


def test_moved_to_changes_position_only():
    rover = Rover(Position(1, 1), Direction.NORTH)
    moved = rover.moved_to(Position(1, 2))
    assert moved.position == Position(1, 2)
    assert moved.direction is rover.direction


def test_str_representation():
    rover = Rover(Position(3, 4), Direction.EAST)
    assert str(rover) == "3:4:E"
