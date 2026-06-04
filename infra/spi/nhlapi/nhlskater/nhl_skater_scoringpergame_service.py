from dataclasses import fields

from helper.http_helper import HttpHelper
from infra.spi.nhlapi.nhlskater.model.nhl_skater_scoringpergame import SkaterScoringPerGame
from server.commons.helper.nhl_season_converter import NhlYearConverter

_SCORINGPERGAME_FIELDS = {f.name for f in fields(SkaterScoringPerGame)}

_SORT = (
    "%5B%7B%22property%22:%22pointsPerGame%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22goalsPerGame%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D"
)


class NHLSkaterScoringPerGameService:

    def __init__(self):
        pass

    def getAllPlayers(self, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_player_paging(start, end, seasonId))["data"]
        return [self.__to_model(player) for player in response]

    def getForwards(self, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_forward_paging(start, end, seasonId))["data"]
        return [self.__to_model(player) for player in response]

    def getDefensemen(self, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_defense_paging(start, end, seasonId))["data"]
        return [self.__to_model(player) for player in response]

    def getPlayersPerTeam(self, franchiseId, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_team_paging(franchiseId, start, end, seasonId))["data"]
        return [self.__to_model(player) for player in response]

    def __get_url_team_paging(self, franchiseId, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/skater/scoringpergame"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=franchiseId%3D{franchiseId}%20and%20gameTypeId=2%20"
            f"and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __get_url_player_paging(self, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/skater/scoringpergame"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __get_url_forward_paging(self, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/skater/scoringpergame"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=(positionCode%3D%22L%22%20or%20positionCode%3D%22R%22%20or%20positionCode%3D%22C%22)%20"
            f"and%20gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __get_url_defense_paging(self, start, limit, seasonId):
        return (
            f"https://api.nhle.com/stats/rest/en/skater/scoringpergame"
            f"?isAggregate=false&isGame=false&sort={_SORT}"
            f"&start={start}&limit={limit}"
            f"&cayenneExp=gameTypeId=2%20and%20positionCode%3D%22D%22%20"
            f"and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"
        )

    def __to_model(self, row: dict) -> SkaterScoringPerGame:
        return SkaterScoringPerGame(**{k: v for k, v in row.items() if k in _SCORINGPERGAME_FIELDS})


if __name__ == '__main__':
    import json
    players = NHLSkaterScoringPerGameService().getAllPlayers(end="5", seasonId=20252026)
    print(json.dumps(players[0].__dict__, indent=2))
