from server.nhlapi.service.nhl_player_service import NHLPlayerService
from server.nhlapi.service.nhl_roster_service import NHLRosterService


class NHLRosterServiceFacade:

    def __init__(self, nhlRosterService=NHLRosterService(), nhlPlayerService=NHLPlayerService()):
        self.nhlRosterService = nhlRosterService
        self.nhlPlayerService = nhlPlayerService

    def get_nhl_roster_by_team_id(self, id):
        player_ids = self.nhlRosterService.get_team_roster_by_id(id)
        return player_ids


print(NHLRosterServiceFacade().get_nhl_roster_by_team_id(1))
