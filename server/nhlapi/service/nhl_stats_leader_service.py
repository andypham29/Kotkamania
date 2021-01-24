from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_leader_player import LeaderPlayer


class NHLStatsLeaderService:

    def __init__(self):
        pass

    def getAllPlayers(self, start="0", end="100", seasonId="20202021"):
        response = HttpHelper.get(self.__get_url_player_paging(start, end, seasonId))["data"]
        return [self.__getStatsForAllLeaderPlayers(player) for player in response]

    def getForwards(self, start="0", end="100", seasonId="20202021"):
        response = HttpHelper.get(self.__get_url_forward_paging(start, end, seasonId))["data"]
        return [self.__getStatsForAllLeaderPlayers(player) for player in response]

    def getDefensemen(self, start="0", end="100", seasonId="20202021"):
        response = HttpHelper.get(self.__get_url_defense_paging(start, end, seasonId))["data"]
        return [self.__getStatsForAllLeaderPlayers(player) for player in response]

    def getGoalies(self, start="0", end="100", seasonId="20202021"):
        response = HttpHelper.get(self.__get_url_goalie_paging(start, end, seasonId))["data"]
        return [self.__getStatsForAllLeaderPlayers(player) for player in response]

    def __get_url_player_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start={start}&limit={limit}&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_url_forward_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start={start}&limit={limit}&factCayenneExp=gamesPlayed%3E=1&cayenneExp=(positionCode%3D%22L%22%20or%20positionCode%3D%22R%22%20or%20positionCode%3D%22C%22)%20and%20gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_url_defense_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start={start}&limit={limit}&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20positionCode%3D%22D%22%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

    def __get_url_goalie_paging(self, start, limit, seasonId):
        return f"https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22goalsAgainstAverage%22,%22direction%22:%22ASC%22%7D%5D&start={start}&limit={limit}&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={seasonId}%20and%20seasonId%3E={seasonId}"

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
