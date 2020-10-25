from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_player import Player, PlayerStat


class NHLPlayerStatService:

    def __init__(self):
        pass

    def get_player_stat_by_id(self, id):
        stats_json = HttpHelper.get(self.__get_player_stats_url(id))
        stats = stats_json["people"]
        return None
    @staticmethod
    def __get_player_stats_url(id, year="20192020"):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}/stat?stats=statsSingleSeason&season={year}"


print([p.__dict__ for p in NHLPlayerStatService().get_player_stat_by_id(1)])
