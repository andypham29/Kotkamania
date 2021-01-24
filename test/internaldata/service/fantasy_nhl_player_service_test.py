from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService


def test_when_getting_fantasy_skater_with_empty_query():
    query = ""
    result = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(query)
    assert result == []


def test_when_getting_fantasy_skater_with_empty_query():
    query = " "
    result = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(query)
    assert result == []


def test_when_getting_fantasy_skater_with_1_char_query_then_return_empty_array():
    query = "a"
    result = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(query)
    assert result == []


def test_when_getting_fantasy_skater_with_2_char_query_then_return_empty_array():
    query = "aa"
    result = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(query)
    assert result == []


def test_when_getting_fantasy_skater_with_2_char_1_space_query_then_return_empty_array():
    query = "a a"
    result = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(query)
    assert result == []


def test_when_getting_fantasy_skater_with_symbols_query_then_return_empty_array():
    query = ".'[;"
    result = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(query)
    assert result == []
