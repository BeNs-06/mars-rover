import pytest

from mars_rover.commands import InvalidCommandError
from mars_rover.direction import Direction
from mars_rover.planet_map import PlanetMap, Position
from mars_rover.rover import Rover
from mars_rover.simulator import InvalidStartPositionError, run_mission


def _free_map(width: int, height: int) -> PlanetMap:
    return PlanetMap.from_rows(["🟩" * width] * height)


def test_move_forward_north():
    planet_map = _free_map(10, 10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "M")
    assert final_rover.position == Position(1, 2)
    assert final_rover.direction is Direction.NORTH


def test_turning_changes_direction_without_moving():
    planet_map = _free_map(10, 10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "R")
    assert final_rover.position == Position(1, 1)
    assert final_rover.direction is Direction.EAST


def test_classic_kata_sequence():
    planet_map = _free_map(10, 10)
    rover = Rover(Position(1, 2), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "LMLMLMLMM")
    assert final_rover.position == Position(1, 3)
    assert final_rover.direction is Direction.NORTH


def test_empty_command_sequence_leaves_rover_unchanged():
    planet_map = _free_map(10, 10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "")
    assert final_rover == rover


def test_move_blocked_by_obstacle_leaves_rover_in_place():
    planet_map = PlanetMap.from_rows(["🌳", "🟩"])
    rover = Rover(Position(0, 0), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "M")
    assert final_rover == rover


def test_move_blocked_by_map_edge_leaves_rover_in_place():
    planet_map = _free_map(2, 2)
    rover = Rover(Position(0, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "M")
    assert final_rover == rover


def test_execution_continues_after_a_move_blocked_by_an_obstacle():
    planet_map = PlanetMap.from_rows(["🌳🟩", "🟩🟩"])
    rover = Rover(Position(0, 0), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "MRM")
    # Le M initial est bloqué par l'obstacle (rover immobile pour cette
    # commande), puis R et le second M s'exécutent normalement.
    assert final_rover.position == Position(1, 0)
    assert final_rover.direction is Direction.EAST


def test_execution_continues_after_a_move_blocked_by_the_map_edge():
    planet_map = _free_map(2, 2)
    rover = Rover(Position(0, 1), Direction.NORTH)
    final_rover = run_mission(planet_map, rover, "MRM")
    assert final_rover.position == Position(1, 1)
    assert final_rover.direction is Direction.EAST


def test_start_position_out_of_bounds_raises_before_any_execution():
    planet_map = _free_map(2, 2)
    rover = Rover(Position(5, 5), Direction.NORTH)
    with pytest.raises(InvalidStartPositionError) as excinfo:
        run_mission(planet_map, rover, "M")
    assert excinfo.value.position == Position(5, 5)


def test_start_position_on_obstacle_raises_before_any_execution():
    planet_map = PlanetMap.from_rows(["🌳"])
    rover = Rover(Position(0, 0), Direction.NORTH)
    with pytest.raises(InvalidStartPositionError) as excinfo:
        run_mission(planet_map, rover, "M")
    assert excinfo.value.position == Position(0, 0)


def test_invalid_command_raises_before_any_execution():
    planet_map = _free_map(10, 10)
    rover = Rover(Position(1, 1), Direction.NORTH)
    with pytest.raises(InvalidCommandError):
        run_mission(planet_map, rover, "MX")
