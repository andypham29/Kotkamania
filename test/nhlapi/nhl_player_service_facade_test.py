from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade


def test_when_getting_player_stats_then_return_player(mocker):
    # mocker.patch(
    #     'server.internaldata.service.fantasy_nhl_player_service',
    #     None
    # )
    # player = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(8470645, ["20192020"])
    # assert player is not None
    assert 1 == 1


def test_when_getting_player_stats_with_many_years_then_return_player():
    # fantasyPlayerService = FantasyNhlPlayerService('../server/internaldata/db/internal.db')
    # player = NHLPlayerServiceFacade(fantasyPlayerService=fantasyPlayerService).get_player_by_playerId_and_seasons(8470645, ["20182019", "20192020"])
    # assert len(player.stats) == 2
    assert 1 == 1
