from helper.http_helper import HttpHelper
from server.commons.helper.time_converter import TimeConverter
# from server.internaldata.model.models import InternalPlayerStat
from server.internaldata.model.internal_nhl_player_stat import InternalPlayerStat


class NHLStatMiscService:

    def __init__(self):
        pass

    def get_player_by_id(self, id, seasonId):
        players = self.get_all_players(seasonId)
        return [player for player in players if player.playerId == id]

    def get_all_players(self, seasonId):
        stats = sorted(HttpHelper.get(self.__get_stat_url(seasonId))["data"], key=lambda d: d['playerId'])
        miscs = sorted(HttpHelper.get(self.__get_misc_url(seasonId))["data"], key=lambda d: d['playerId'])
        tois = sorted(HttpHelper.get(self.__get_toi_url(seasonId))["data"], key=lambda d: d['playerId'])

        internalPlayerStats = list()

        for i in range(len(stats)):
            stat = stats[i]
            misc = miscs[i]
            toi = tois[i]
            internalPlayerStats.append(self.__build_model(stat, misc, toi))

        return internalPlayerStats


    def __get_stat_url(self, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start=0&limit=50&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_misc_url(self, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/realtime?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22hits%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_toi_url(self, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22timeOnIce%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start=0&limit=50&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

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
    print(NHLStatMiscService().get_all_players("20232024")[0].__dict__)
    print(NHLStatMiscService().get_player_by_id(8471675, "20232024")[0].__dict__)
