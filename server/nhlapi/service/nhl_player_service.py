from datetime import date

from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_player import Player, SeasonStat, PlayerStat, PlayerDraftDetails


class NHLPlayerService:

    def __init__(self):
        pass

    def get_player_by_id(self, id):
        player = HttpHelper.get(self.__get_player_info_url(id))

        return Player(player.get("playerId", None),
                      f"{player.get('firstName', None).get('default')} {player.get('lastName', None).get('default')}",
                      player.get("position", None),
                      player.get("currentTeamId", None),
                      player.get("currentTeamAbbrev", None),
                      player.get("sweaterNumber", None),
                      player.get("birthDate", None),
                      self.__current_age(player.get("birthDate", None)),
                      player.get("birthCity", None).get("default", None),
                      player.get("birthCountry", None),
                      player.get("heightInCentimeters", None),
                      player.get("weightInKilograms", None),
                      player.get("shootsCatches", None),
                      # stats=self.get_stats(player.get("seasonTotals", None)),
                      playerDraftDetails=self.get_playerDraftDetails(player.get("draftDetails", None)),
                      )

    def get_playerDraftDetails(self, draftDetail):
        if draftDetail is None:
            return None
        return PlayerDraftDetails(
            year=draftDetail.get("year", None),
            teamAbbrev=draftDetail.get("teamAbbrev", None),
            draftRound=draftDetail.get("round", None),
            pickInRound=draftDetail.get("pickInRound", None),
            overallPick=draftDetail.get("overallPick", None),
        )

    def get_stats(self, playerStats):
        return [SeasonStat(
            season=playerStat.get("season"),
            stat=self.get_season_stat(playerStat)) for playerStat in playerStats]

    def get_season_stat(self, playerStat):
        return PlayerStat(
            timeOnIce=playerStat.get("timeOnIce", None),
            assists=playerStat.get("assists", None),
            goals=playerStat.get("goals", None),
            pim=playerStat.get("pim", None),
            shots=playerStat.get("shots", None),
            games=playerStat.get("gamesPlayed", None),
            hits=playerStat.get("hits", None),
            powerPlayGoals=playerStat.get("powerPlayGoals", None),
            powerPlayPoints=playerStat.get("powerPlayPoints", None),
            powerPlayTimeOnIce=playerStat.get("powerPlayTimeOnIce", None),
            evenTimeOnIce=playerStat.get("evenTimeOnIce", None),
            penaltyMinutes=playerStat.get("penaltyMinutes", None),
            faceOffPct=playerStat.get("faceOffPct", None),
            shotPct=playerStat.get("shotPct", None),
            gameWinningGoals=playerStat.get("gameWinningGoals", None),
            overTimeGoals=playerStat.get("overTimeGoals", None),
            shortHandedGoals=playerStat.get("shortHandedGoals", None),
            shortHandedPoints=playerStat.get("shortHandedPoints", None),
            shortHandedTimeOnIce=playerStat.get("shortHandedTimeOnIce", None),
            blocked=playerStat.get("blocked", None),
            plusMinus=playerStat.get("plusMinus", None),
            points=playerStat.get("points", None),
            shifts=playerStat.get("shifts", None),
            timeOnIcePerGame=playerStat.get("timeOnIcePerGame", None),
            evenTimeOnIcePerGame=playerStat.get("evenTimeOnIcePerGame", None),
            shortHandedTimeOnIcePerGame=playerStat.get("shortHandedTimeOnIcePerGame", None),
            powerPlayTimeOnIcePerGame=playerStat.get("powerPlayTimeOnIcePerGame", None),
        )

    def __current_age(self, birthday):
        today = date.today()
        b = birthday.split("-")
        year, month, day = int(b[0]), int(b[1]), int(b[2])
        return today.year - year - ((today.month, day) < (month, day))

    @staticmethod
    def __get_player_info_url(id):
        return f"https://api-web.nhle.com/v1/player/{id}/landing"


if __name__ == '__main__':
    player = NHLPlayerService().get_player_by_id(8478402)
    print([i.__dict__ for i in player.stats])
