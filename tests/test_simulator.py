import pytest

from mars_rover.commands import InvalidCommandError
from mars_rover.direction import Direction
from mars_rover.planet_map import PlanetMap, Position
from mars_rover.rover import Rover
from mars_rover.simulator import OutOfBoundsError, run_mission


def test_move_forward_north():
    planet_map = PlanetMap(width=10, height=10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "M")
    assert final_rover.position == Position(1, 2)
    assert final_rover.direction is Direction.NORTH


def test_classic_kata_sequence():
    planet_map = PlanetMap(width=10, height=10)
    rover = Rover(Position(1, 2), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "LMLMLMLMM")
    assert final_rover.position == Position(1, 3)
    assert final_rover.direction is Direction.NORTH


def test_empty_command_sequence_leaves_rover_unchanged():
    planet_map = PlanetMap(width=10, height=10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "")
    assert final_rover == rover


def test_moving_outside_the_map_raises_out_of_bounds_error():
    planet_map = PlanetMap(width=2, height=2)
    rover = Rover(Position(0, 1), Direction.NORTH)
    with pytest.raises(OutOfBoundsError) as excinfo:
        run_mission(planet_map, rover, "M")
    assert excinfo.value.rover == rover
    assert excinfo.value.attempted_position == Position(0, 2)


def test_out_of_bounds_keeps_the_effect_of_earlier_successful_moves():
    planet_map = PlanetMap(width=2, height=2)
    rover = Rover(Position(0, 0), Direction.EAST)
    with pytest.raises(OutOfBoundsError) as excinfo:
        run_mission(planet_map, rover, "MM")
    assert excinfo.value.rover.position == Position(1, 0)
    assert excinfo.value.rover.direction is Direction.EAST
    assert excinfo.value.attempted_position == Position(2, 0)


def test_invalid_command_raises():
    planet_map = PlanetMap(width=10, height=10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    with pytest.raises(InvalidCommandError):
        run_mission(planet_map, rover, "MX")
