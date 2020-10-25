from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_team import Team


class NHLRosterService:

    def __init__(self):
        pass

    def get_team_roster_by_id(self, id):
        json = HttpHelper.get(self.__get_roster_url(id))
        return json

    @staticmethod
    def __get_roster_url(id):
        return f"https://statsapi.web.nhl.com/api/v1/teams/{id}/roster"

print(NHLRosterService().get_team_roster_by_id(1))