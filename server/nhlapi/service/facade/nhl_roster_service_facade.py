from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.nhlapi.service.nhl_roster_service import NHLRosterService


class NHLRosterServiceFacade:

    def __init__(self, nhlRosterService=NHLRosterService()):
        self.nhlRosterService = nhlRosterService

    def get_nhl_roster_by_team_id(self, id):
        roster_players = self.nhlRosterService.get_team_roster_by_id(id)
        player_ids = [i.playerId for i in roster_players]
        players = FantasyNhlPlayerService().getFantasySkaterByIds(player_ids)
        return sorted(players, key=lambda x: x.fantasyGrade, reverse=True)
        # return players


if __name__ == '__main__':
    roster = NHLRosterServiceFacade().get_nhl_roster_by_team_id(8)
    for i in roster:
        print(i.__dict__)