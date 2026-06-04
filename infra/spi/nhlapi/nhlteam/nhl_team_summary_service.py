from dataclasses import fields

from helper.http_helper import HttpHelper
from infra.spi.nhlapi.nhlteam.model.nhl_team_summary import TeamSummary
from server.commons.helper.nhl_season_converter import NhlYearConverter

_TEAMSUMMARY_FIELDS = {f.name for f in fields(TeamSummary)}

_SORT = (
    "%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22wins%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22teamId%22,%22direction%22:%22ASC%22%7D%5D"
)


class NhlTeamSummaryService:

    def __init__(self):
        pass

    def getAllTeams(self, start="0", end="50", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_paging(start, end, seasonId))["data"]
        return [self.__to_model(team) for team in response]

    def getTeam(self, teamId, seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_team(teamId, seasonId))["data"]
        if not response:
            return None
        return self.__to_model(response[0])

    def __get_url_paging(self, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/team/summary"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __get_url_team(self, teamId, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/team/summary"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start=0&limit=1"
            f"&cayenneExp=teamId%3D{teamId}%20and%20gameTypeId=2%20"
            f"and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __to_model(self, row: dict) -> TeamSummary:
        return TeamSummary(**{k: v for k, v in row.items() if k in _TEAMSUMMARY_FIELDS})


if __name__ == '__main__':
    import json
    teams = NhlTeamSummaryService().getAllTeams(seasonId=20252026)
    print(json.dumps(teams[0].__dict__, indent=2))
