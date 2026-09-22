import pytest

from mars_rover.planet_map import InvalidMapError, PlanetMap, Position, parse_map


def test_position_str():
    assert str(Position(2, 3)) == "2:3"


def test_from_rows_builds_map_with_correct_dimensions():
    planet_map = PlanetMap.from_rows(["🟩🟩", "🟩🟩", "🟩🟩"])
    assert planet_map.width == 2
    assert planet_map.height == 3


@pytest.mark.parametrize(
    "position",
    [Position(0, 0), Position(1, 0), Position(0, 2), Position(1, 2)],
)
def test_position_within_bounds(position):
    planet_map = PlanetMap.from_rows(["🟩🟩", "🟩🟩", "🟩🟩"])
    assert planet_map.is_within_bounds(position)


@pytest.mark.parametrize(
    "position",
    [Position(-1, 0), Position(0, -1), Position(2, 0), Position(0, 3)],
)
def test_position_out_of_bounds(position):
    planet_map = PlanetMap.from_rows(["🟩🟩", "🟩🟩", "🟩🟩"])
    assert not planet_map.is_within_bounds(position)


def test_first_row_is_the_top_of_the_map():
    # La première ligne saisie correspond au y le plus élevé (nord = haut).
    planet_map = PlanetMap.from_rows(["🌳", "🟩"])
    assert planet_map.is_free(Position(0, 0))
    assert not planet_map.is_free(Position(0, 1))


@pytest.mark.parametrize("symbol", ["🟩", "🟫"])
def test_free_symbols(symbol):
    planet_map = PlanetMap.from_rows([symbol])
    assert planet_map.is_free(Position(0, 0))


@pytest.mark.parametrize("symbol", ["🌳", "🪨"])
def test_obstacle_symbols(symbol):
    planet_map = PlanetMap.from_rows([symbol])
    assert not planet_map.is_free(Position(0, 0))


def test_mixed_symbol_sets_behave_like_a_single_set():
    mixed = PlanetMap.from_rows(["🟩🟫🌳🪨"])
    equivalent = PlanetMap.from_rows(["🟩🟩🌳🌳"])
    for x in range(4):
        position = Position(x, 0)
        assert mixed.is_free(position) == equivalent.is_free(position)


def test_is_free_is_false_outside_bounds():
    planet_map = PlanetMap.from_rows(["🟩"])
    assert not planet_map.is_free(Position(5, 5))


def test_unknown_symbol_raises():
    with pytest.raises(InvalidMapError):
        PlanetMap.from_rows(["🟩❓"])


def test_empty_rows_raise():
    with pytest.raises(InvalidMapError):
        PlanetMap.from_rows([])


def test_empty_row_raises():
    with pytest.raises(InvalidMapError):
        PlanetMap.from_rows([""])


def test_irregular_row_widths_raise():
    with pytest.raises(InvalidMapError):
        PlanetMap.from_rows(["🟩🟩", "🟩"])


def test_parse_map_from_raw_multiline_string():
    planet_map = parse_map("🟩🟩\n🌳🟩\n")
    assert planet_map.width == 2
    assert planet_map.height == 2
    assert not planet_map.is_free(Position(0, 0))
