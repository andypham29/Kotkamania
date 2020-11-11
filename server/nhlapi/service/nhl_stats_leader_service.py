from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_leader_player import LeaderPlayer


class NhlStatsLeaderService:

    def __init__(self):
        pass

    def getAllPlayers(self, start="0", end="100", seasonId="20192020"):
        response = HttpHelper.get(self.__get_url_player_paging(start, end, seasonId))["data"]
        return [self.__getStatsForAllLeaderPlayers(player) for player in response]

    def __get_url_player_paging(self, start, end, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start={start}&limit={end}&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __getStatsForAllLeaderPlayers(self, player_json):
        return LeaderPlayer(player_json["assists"],
                            player_json["evGoals"],
                            player_json["evPoints"],
                            player_json["faceoffWinPct"],
                            player_json["gameWinningGoals"],
                            player_json["gamesPlayed"],
                            player_json["goals"],
                            player_json["lastName"],
                            player_json["otGoals"],
                            player_json["penaltyMinutes"],
                            player_json["playerId"],
                            player_json["plusMinus"],
                            player_json["points"],
                            player_json["pointsPerGame"],
                            player_json["positionCode"],
                            player_json["ppGoals"],
                            player_json["ppPoints"],
                            player_json["seasonId"],
                            player_json["shGoals"],
                            player_json["shPoints"],
                            player_json["shootingPct"],
                            player_json["shootsCatches"],
                            player_json["shots"],
                            player_json["skaterFullName"],
                            player_json["teamAbbrevs"],
                            player_json["timeOnIcePerGame"])
