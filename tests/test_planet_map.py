import pytest

from mars_rover.planet_map import PlanetMap, Position


def test_position_within_bounds():
    planet_map = PlanetMap(width=5, height=5)
    assert planet_map.is_within_bounds(Position(0, 0))
    assert planet_map.is_within_bounds(Position(4, 4))


@pytest.mark.parametrize(
    "position",
    [Position(-1, 0), Position(0, -1), Position(5, 0), Position(0, 5)],
)
def test_position_out_of_bounds(position):
    planet_map = PlanetMap(width=5, height=5)
    assert not planet_map.is_within_bounds(position)


@pytest.mark.parametrize("width, height", [(0, 5), (5, 0), (-1, 5)])
def test_invalid_map_dimensions_raise(width, height):
    with pytest.raises(ValueError):
        PlanetMap(width=width, height=height)


def test_position_str():
    assert str(Position(2, 3)) == "2:3"
