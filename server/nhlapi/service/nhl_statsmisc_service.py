from helper.http_helper import HttpHelper
from server.commons.helper.time_converter import TimeConverter
# from server.internaldata.model.internal_nhl_player_stat import InternalPlayerStat
from server.internaldata.model.models import InternalPlayerStat


class NHLStatMiscService:
    __summary = "summary"
    __realtime = "realtime"
    __timeonice = "timeonice"

    def __init__(self):

        pass

    def get_player_by_id(self, id, seasonId):
        players = self.get_all_player_stats(seasonId)
        return [player for player in players if player.playerId == id]

    def get_all_player_stats(self, seasonId):
        stats = self.__loop(self.__summary, seasonId)
        miscs = self.__loop(self.__realtime, seasonId)
        tois = self.__loop(self.__timeonice, seasonId)

        internalPlayerStats = list()

        for i in range(len(stats)):
            stat = stats[i]
            misc = miscs[i]
            toi = tois[i]
            internalPlayerStats.append(self.__build_model(stat, misc, toi))

        return internalPlayerStats

    def __loop(self, url_type, seasonId):
        data_set = []
        for i in range(10):
            if url_type == self.__summary:
                url = self.__get_stat_url(seasonId, i+1)
            elif url_type == self.__realtime:
                url = self.__get_misc_url(seasonId, i+1)
            elif url_type == self.__timeonice:
                url = self.__get_toi_url(seasonId, i+1)

            data = HttpHelper.get(url)["data"]

            data_set += data
            print(f"Preparing data of type {url_type}: {i+1} of {10}")

        return sorted(data_set, key=lambda d: d.get('playerId'), reverse=True)

    def __get_stat_url(self, seasonId, page):
        start = 100 * page - 100
        end = 100 * page
        return f"https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={end}&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_misc_url(self, seasonId, page):
        start = 100 * page - 100
        end = 100 * page
        return f"https://api.nhle.com/stats/rest/en/skater/realtime?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22hits%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={end}&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId={seasonId}"
    def __get_toi_url(self, seasonId, page):
        start = 100 * page - 100
        end = 100 * page
        return f"https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={end}&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __build_model(self, stat, misc, toi):
        return InternalPlayerStat(
            playerId=stat.get("playerId", None),
            seasonId=stat.get("seasonId", None),
            timeOnIce=TimeConverter.convert_total_seconds_to_string(stat.get("timeOnIcePerGame", 0)),
            assists=stat.get("assists", None),
            goals=stat.get("goals", None),
            pim=stat.get("penaltyMinutes", None),
            shots=stat.get("shots", None),
            games=stat.get("gamesPlayed", None),
            hits=misc.get("hits", None),
            powerPlayGoals=stat.get("ppGoals", None),
            powerPlayPoints=stat.get("ppPoints", None),
            powerPlayTimeOnIce=TimeConverter.convert_total_seconds_to_string(toi.get("ppTimeOnIce", 0)),
            evenTimeOnIce=TimeConverter.convert_total_seconds_to_string(toi.get("evTimeOnIce", 0)),
            penaltyMinutes=stat.get("penaltyMinutes", None),
            faceOffPct=stat.get("faceoffWinPct", None),
            shotPct=stat.get("shootingPct", None),
            gameWinningGoals=stat.get("gameWinningGoals", None),
            overTimeGoals=stat.get("otGoals", None),
            shortHandedGoals=stat.get("shGoals", None),
            shortHandedPoints=stat.get("shPoints", None),
            shortHandedTimeOnIce=TimeConverter.convert_total_seconds_to_string(toi.get("shTimeOnIce", 0)),
            blocked=misc.get("blockedShots", None),
            plusMinus=stat.get("plusMinus", None),
            points=stat.get("points", None),
            shifts=TimeConverter.convert_total_seconds_to_string(toi.get("shifts", 0)),
            timeOnIcePerGame=TimeConverter.convert_total_seconds_to_string(toi.get("timeOnIcePerGame", 0)),
            evenTimeOnIcePerGame=TimeConverter.convert_total_seconds_to_string(toi.get("evTimeOnIcePerGame", 0)),
            shortHandedTimeOnIcePerGame=TimeConverter.convert_total_seconds_to_string(toi.get("timeOnIcePerGame", 0)),
            powerPlayTimeOnIcePerGame=TimeConverter.convert_total_seconds_to_string(toi.get("ppTimeOnIcePerGame", 0)),
        )


if __name__ == '__main__':
    # print([i.__dict__ for i in NHLStatMiscService().get_all_player_stats("20232024")])
    print(NHLStatMiscService().get_player_by_id(8471675, "20232024")[0].__dict__)
