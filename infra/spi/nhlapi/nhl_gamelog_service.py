from helper.http_helper import HttpHelper
from infra.spi.nhlapi.model.nhl_gamelog import GameLog, CommonName


class NHLGameLogService:

    def __init__(self):
        pass

    def get_game_log(self, player_id, season):
        data = HttpHelper.get(self.__get_game_log_url(player_id, season))
        if data is None:
            return []
        return [self.__map_game(g) for g in data.get("gameLog", [])]

    def __map_game(self, g):
        return GameLog(
            gameId=g.get("gameId", None),
            teamAbbrev=g.get("teamAbbrev", None),
            homeRoadFlag=g.get("homeRoadFlag", None),
            gameDate=g.get("gameDate", None),
            goals=g.get("goals", None),
            assists=g.get("assists", None),
            commonName=self.__map_common_name(g.get("commonName", None)),
            opponentCommonName=self.__map_common_name(g.get("opponentCommonName", None)),
            points=g.get("points", None),
            plusMinus=g.get("plusMinus", None),
            powerPlayGoals=g.get("powerPlayGoals", None),
            powerPlayPoints=g.get("powerPlayPoints", None),
            gameWinningGoals=g.get("gameWinningGoals", None),
            otGoals=g.get("otGoals", None),
            shots=g.get("shots", None),
            shifts=g.get("shifts", None),
            shorthandedGoals=g.get("shorthandedGoals", None),
            shorthandedPoints=g.get("shorthandedPoints", None),
            opponentAbbrev=g.get("opponentAbbrev", None),
            pim=g.get("pim", None),
            toi=g.get("toi", None),
        )

    def __map_common_name(self, name):
        if name is None:
            return None
        return CommonName(default=name.get("default", None))

    @staticmethod
    def __get_game_log_url(player_id, season):
        return f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season}/2"


if __name__ == '__main__':
    games = NHLGameLogService().get_game_log(8478402, 20252026)
    print(f"{len(games)} games")
    for g in games[:3]:
        print(g)
