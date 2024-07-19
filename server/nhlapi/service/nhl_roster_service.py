from helper.http_helper import HttpHelper
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.nhl_team_converter import NhlTeamConverter
from server.nhlapi.model.nhl_roster_player_info import RosterPlayerInfo


class NHLRosterService:

    def __init__(self):
        pass

    def get_team_roster_by_id(self, id):
        json = HttpHelper.get(self.__get_roster_url(id))
        roster_players = self.__get_roster_players(json)
        return [self.__get_roster_player_info(player) for player in roster_players]

    @staticmethod
    def __get_roster_url(id):
        abr = NhlTeamConverter.get_abbreviation_by_teamId(id)
        year = NhlYearConverter.get_current_season()
        return f"https://api-web.nhle.com/v1/roster/{abr}/{year}"

    @staticmethod
    def __get_roster_players(json):
        forwards = json.get("forwards", [])
        defensemen = json.get("defensemen", [])
        goalies = json.get("goalies", [])

        return forwards + defensemen + goalies

    @staticmethod
    def __get_roster_player_info(player):
        return RosterPlayerInfo(
            player.get("id", None),
            f"{player.get('firstName', None).get('default', None)} {player.get('lastName', None).get('default', None)}",
            player.get("positionCode", None),
            player.get("sweaterNumber", None),
        )
if __name__ == '__main__':
    print([i.__dict__ for i in NHLRosterService().get_team_roster_by_id(None)])
