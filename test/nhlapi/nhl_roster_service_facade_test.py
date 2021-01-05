from server.nhlapi.service.facade.nhl_roster_service_facade import NHLRosterServiceFacade


def test_when_getting_roster_then_return_roster():
    roster = NHLRosterServiceFacade().get_nhl_roster_by_team_id(1)
    for rosterPlayer in roster:
        assert rosterPlayer.playerId is not None
        assert rosterPlayer.position is not None
        assert rosterPlayer.fullName is not None
        # assert rosterPlayer.jerseyNumber is not None (optional)
