from server.commons.helper.nhl_team_converter import NhlTeamConverter
from server.internaldata.model.fantasy_nhl_player import FantasyNhlPlayer
from server.nhlapi.service.facade.nhl_roster_service_facade import NHLRosterServiceFacade
from server.nhlapi.service.nhl_team_service import NhlTeamService


class FantasyTeamHelper:

    def get_all_players_in_teams(self):
        nhl_roster_service_facade = NHLRosterServiceFacade()
        roster_players = []
        teams = NhlTeamService().getAllTeams()
        for team in teams:
            # # TODO remove when UTA
            teamName = "Utah Hockey Club" if team.id == 56 else team.name
            roster_players += [
                FantasyNhlPlayer(id=player.playerId, skaterFullName=player.fullName, positionCode=player.position,
                                 teamId=team.id, teamName=teamName)
                for player in nhl_roster_service_facade.get_nhl_roster_by_team_id(team.id)]

        return roster_players


if __name__ == '__main__':
    a = NhlTeamService().getAllTeams()
    print(FantasyTeamHelper().get_all_players_in_teams())
