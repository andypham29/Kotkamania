from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_player import PlayerStat, SeasonStat, GoalieStat


class NHLPlayerStatService:

    def __init__(self):
        pass

    def get_player_playoff_stat_by_playerId_and_seasons(self, playerId, seasons=[""]):
        stats = []
        for season in seasons:
            stats_json = HttpHelper.get(self.__get_player_playoff_stats_url(playerId, season))
            stat_splits = stats_json["stats"][0]["splits"]
            stats += [SeasonStat(split["season"], self.__get_player_stat(split)) for split in stat_splits]

        return stats

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

    def get_player_gamelogs_by_playerId_and_season(self, playerId, season):
        stats = []
        stats_json = HttpHelper.get(self.__get_player_gamelogs_url(playerId, season))
        stat_splits = stats_json["stats"][0]["splits"]
        stats += [SeasonStat(split["season"], self.__get_player_stat(split)) for split in stat_splits]

        return stats

    @staticmethod
    def __get_player_playoff_stats_url(id, year):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=statsSingleSeasonPlayoffs&season={year}"

    @staticmethod
    def __get_player_stats_url(id, year):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=statsSingleSeason&season={year}"

    @staticmethod
    def __get_player_gamelogs_url(id, year):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=gameLog&season={year}"

    @staticmethod
    def __get_player_stat(split):
        return PlayerStat(
            timeOnIce=split["stat"].get("timeOnIce", None),
            assists=split["stat"].get("assists", None),
            goals=split["stat"].get("goals", None),
            pim=split["stat"].get("pim", None),
            shots=split["stat"].get("shots", None),
            games=split["stat"].get("games", None),
            hits=split["stat"].get("hits", None),
            powerPlayGoals=split["stat"].get("powerPlayGoals", None),
            powerPlayPoints=split["stat"].get("powerPlayPoints", None),
            powerPlayTimeOnIce=split["stat"].get("powerPlayTimeOnIce", None),
            evenTimeOnIce=split["stat"].get("evenTimeOnIce", None),
            penaltyMinutes=split["stat"].get("penaltyMinutes", None),
            faceOffPct=split["stat"].get("faceOffPct", None),
            shotPct=split["stat"].get("shotPct", None),
            gameWinningGoals=split["stat"].get("gameWinningGoals", None),
            overTimeGoals=split["stat"].get("overTimeGoals", None),
            shortHandedGoals=split["stat"].get("shortHandedGoals", None),
            shortHandedPoints=split["stat"].get("shortHandedPoints", None),
            shortHandedTimeOnIce=split["stat"].get("shortHandedTimeOnIce", None),
            blocked=split["stat"].get("blocked", None),
            plusMinus=split["stat"].get("plusMinus", None),
            points=split["stat"].get("points", None),
            shifts=split["stat"].get("shifts", None),
            timeOnIcePerGame=split["stat"].get("timeOnIcePerGame", None),
            evenTimeOnIcePerGame=split["stat"].get("evenTimeOnIcePerGame", None),
            shortHandedTimeOnIcePerGame=split["stat"].get("shortHandedTimeOnIcePerGame", None),
            powerPlayTimeOnIcePerGame=split["stat"].get("powerPlayTimeOnIcePerGame", None)
        )

    @staticmethod
    def __get_goalie_stat(split):
        return GoalieStat(
            timeOnIce=split["stat"].get("timeOnIce", None),
            ot=split["stat"].get("ot", None),
            shutouts=split["stat"].get("shutouts", None),
            ties=split["stat"].get("ties", None),
            wins=split["stat"].get("wins", None),
            losses=split["stat"].get("losses", None),
            saves=split["stat"].get("saves", None),
            powerPlaySaves=split["stat"].get("powerPlaySaves", None),
            shortHandedSaves=split["stat"].get("shortHandedSaves", None),
            evenSaves=split["stat"].get("evenSaves", None),
            shortHandedShots=split["stat"].get("shortHandedShots", None),
            evenShots=split["stat"].get("evenShots", None),
            powerPlayShots=split["stat"].get("powerPlayShots", None),
            savePercentage=split["stat"].get("savePercentage", None),
            goalAgainstAverage=split["stat"].get("goalAgainstAverage", None),
            games=split["stat"].get("games", None),
            gamesStarted=split["stat"].get("gamesStarted", None),
            shotsAgainst=split["stat"].get("shotsAgainst", None),
            goalsAgainst=split["stat"].get("goalsAgainst", None),
            timeOnIcePerGame=split["stat"].get("timeOnIcePerGame", None),
            powerPlaySavePercentage=split["stat"].get("powerPlaySavePercentage", None),
            shortHandedSavePercentage=split["stat"].get("shortHandedSavePercentage", None),
            evenStrengthSavePercentage=split["stat"].get("evenStrengthSavePercentage", None)
        )
