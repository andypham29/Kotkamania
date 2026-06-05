from dataclasses import fields

from helper.http_helper import HttpHelper
from infra.spi.nhlapi.nhlgoalie.model.nhl_goalie_summary import GoalieSummary
from server.commons.helper.nhl_season_converter import NhlYearConverter

_GOALIESUMMARY_FIELDS = {f.name for f in fields(GoalieSummary)}

_SORT = (
    "%5B%7B%22property%22:%22wins%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22savePct%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D"
)


class NHLGoalieSummaryService:

    def __init__(self):
        pass

    def getAllGoalies(self, start="0", end="98", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_paging(start, end, seasonId))["data"]
        return [self.__to_model(goalie) for goalie in response]

    def getGoalie(self, playerId, seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_player(playerId, seasonId))["data"]
        if not response:
            return None
        return self.__to_model(response[0])

    def getGoaliesPerTeam(self, franchiseId, start="0", end="98", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_team_paging(franchiseId, start, end, seasonId))["data"]
        return [self.__to_model(goalie) for goalie in response]

    def __get_url_paging(self, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/goalie/summary"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __get_url_player(self, playerId, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/goalie/summary"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start=0&limit=1"
            f"&cayenneExp=playerId%3D{playerId}%20and%20gameTypeId=2%20"
            f"and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __get_url_team_paging(self, franchiseId, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/goalie/summary"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=franchiseId%3D{franchiseId}%20and%20gameTypeId=2%20"
            f"and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __to_model(self, row: dict) -> GoalieSummary:
        return GoalieSummary(**{k: v for k, v in row.items() if k in _GOALIESUMMARY_FIELDS})


if __name__ == '__main__':
    import json
    goalies = NHLGoalieSummaryService().getAllGoalies(seasonId=20252026)
    print(json.dumps(goalies[0].__dict__, indent=2))
