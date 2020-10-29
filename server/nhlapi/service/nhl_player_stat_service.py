from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_player import PlayerStat, SeasonStat, GoalieStat


class NHLPlayerStatService:

    def __init__(self):
        pass

    def get_player_stat_by_playerId_and_seasons(self, playerId, seasons=[""]):
        stats = []
        for season in seasons:
            stats_json = HttpHelper.get(self.__get_player_stats_url(playerId, season))
            stat_splits = stats_json["stats"][0]["splits"]
            stats += [SeasonStat(split["season"], self.__get_player_stat(split)) for split in stat_splits]

        return stats

    def get_goalie_stat_by_playerId_and_season(self, playerId, seasons=[""]):
        stats = []
        for season in seasons:
            stats_json = HttpHelper.get(self.__get_player_stats_url(playerId, season))
            stat_splits = stats_json["stats"][0]["splits"]
            stats += [SeasonStat(split["season"], self.__get_goalie_stat(split)) for split in stat_splits]

        return stats

    @staticmethod
    def __get_player_stats_url(id, year):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=statsSingleSeason&season={year}"

    @staticmethod
    def __get_player_stat(split):
        return PlayerStat(
            timeOnIce=split["stat"]["timeOnIce"],
            assists=split["stat"]["assists"],
            goals=split["stat"]["goals"],
            pim=split["stat"]["pim"],
            shots=split["stat"]["shots"],
            games=split["stat"]["games"],
            hits=split["stat"]["hits"],
            powerPlayGoals=split["stat"]["powerPlayGoals"],
            powerPlayPoints=split["stat"]["powerPlayPoints"],
            powerPlayTimeOnIce=split["stat"]["powerPlayTimeOnIce"],
            evenTimeOnIce=split["stat"]["evenTimeOnIce"],
            penaltyMinutes=split["stat"]["penaltyMinutes"],
            faceOffPct=split["stat"]["faceOffPct"],
            shotPct=split["stat"]["shotPct"],
            gameWinningGoals=split["stat"]["gameWinningGoals"],
            overTimeGoals=split["stat"]["overTimeGoals"],
            shortHandedGoals=split["stat"]["shortHandedGoals"],
            shortHandedPoints=split["stat"]["shortHandedPoints"],
            shortHandedTimeOnIce=split["stat"]["shortHandedTimeOnIce"],
            blocked=split["stat"]["blocked"],
            plusMinus=split["stat"]["plusMinus"],
            points=split["stat"]["points"],
            shifts=split["stat"]["shifts"],
            timeOnIcePerGame=split["stat"]["timeOnIcePerGame"],
            evenTimeOnIcePerGame=split["stat"]["evenTimeOnIcePerGame"],
            shortHandedTimeOnIcePerGame=split["stat"]["shortHandedTimeOnIcePerGame"],
            powerPlayTimeOnIcePerGame=split["stat"]["powerPlayTimeOnIcePerGame"],
        )

    @staticmethod
    def __get_goalie_stat(split):
        return GoalieStat(
            timeOnIce=split["stat"]["timeOnIce"],
            ot=split["stat"]["ot"],
            shutouts=split["stat"]["shutouts"],
            ties=split["stat"]["ties"],
            wins=split["stat"]["wins"],
            losses=split["stat"]["losses"],
            saves=split["stat"]["saves"],
            powerPlaySaves=split["stat"]["powerPlaySaves"],
            shortHandedSaves=split["stat"]["shortHandedSaves"],
            evenSaves=split["stat"]["evenSaves"],
            shortHandedShots=split["stat"]["shortHandedShots"],
            evenShots=split["stat"]["evenShots"],
            powerPlayShots=split["stat"]["powerPlayShots"],
            savePercentage=split["stat"]["savePercentage"],
            goalAgainstAverage=split["stat"]["goalAgainstAverage"],
            games=split["stat"]["games"],
            gamesStarted=split["stat"]["gamesStarted"],
            shotsAgainst=split["stat"]["shotsAgainst"],
            goalsAgainst=split["stat"]["goalsAgainst"],
            timeOnIcePerGame=split["stat"]["timeOnIcePerGame"],
            powerPlaySavePercentage=split["stat"]["powerPlaySavePercentage"],
            shortHandedSavePercentage=split["stat"]["shortHandedSavePercentage"],
            evenStrengthSavePercentage=split["stat"]["evenStrengthSavePercentage"]
        )
