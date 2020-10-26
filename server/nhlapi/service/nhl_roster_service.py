from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_roster_player_info import RosterPlayerInfo


class NHLRosterService:

    def __init__(self):
        pass

    def get_team_roster_by_id(self, id):
        json = HttpHelper.get(self.__get_roster_url(id))
        roster_players = json["roster"]
        return [self.__get_roster_player_info(player) for player in roster_players]

    @staticmethod
    def __get_roster_url(id):
        return f"https://statsapi.web.nhl.com/api/v1/teams/{id}/roster"

    @staticmethod
    def __get_roster_player_info(player):
        return RosterPlayerInfo(
            player["person"]["id"],
            player["person"]["fullName"],
            player["position"]["code"],
            player["jerseyNumber"]
        )


