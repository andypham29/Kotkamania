from dataclasses import fields

from helper.http_helper import HttpHelper
from infra.spi.nhlapi.model.nhl_skater_timeonice import SkaterTimeOnIce
from server.commons.helper.nhl_season_converter import NhlYearConverter

_TIMEONICE_FIELDS = {f.name for f in fields(SkaterTimeOnIce)}


class NHLSkaterTimeOnIceService:

    def __init__(self):
        pass

    def getAllPlayers(self, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_player_paging(start, end, seasonId))["data"]
        return [self.__to_timeonice(player) for player in response]

    def getForwards(self, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_forward_paging(start, end, seasonId))["data"]
        return [self.__to_timeonice(player) for player in response]

    def getDefensemen(self, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_defense_paging(start, end, seasonId))["data"]
        return [self.__to_timeonice(player) for player in response]

    def getPlayersPerTeam(self, franchiseId, start="0", end="100", seasonId=NhlYearConverter.get_current_season()):
        response = HttpHelper.get(self.__get_url_team_paging(franchiseId, start, end, seasonId))["data"]
        return [self.__to_timeonice(player) for player in response]

    def __get_url_team_paging(self, franchiseId, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={limit}&cayenneExp=franchiseId%3D{franchiseId}%20and%20gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_url_player_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={limit}&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_url_forward_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={limit}&cayenneExp=(positionCode%3D%22L%22%20or%20positionCode%3D%22R%22%20or%20positionCode%3D%22C%22)%20and%20gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_url_defense_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={limit}&cayenneExp=gameTypeId=2%20and%20positionCode%3D%22D%22%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __to_timeonice(self, player_json):
        return SkaterTimeOnIce(**{k: v for k, v in player_json.items() if k in _TIMEONICE_FIELDS})


if __name__ == '__main__':
    import json
    players = NHLSkaterTimeOnIceService().getPlayersPerTeam(6)
    print(json.dumps(players[0].__dict__, indent=2))
