from domain.gamelog.model.player_gamelog import PlayerGameLog
from infra.spi.nhlapi.nhl_gamelog_service import NHLGameLogService
from server.commons.helper.nhl_season_converter import NhlYearConverter


class GameLogService:

    def __init__(self):
        self.nhl_gamelog_service = NHLGameLogService()

    def get_player_gamelog(self, player_id):
        season = NhlYearConverter.get_current_season()
        print(f"getting gamelog for player {player_id} in season {season}")
        games = self.nhl_gamelog_service.get_game_log(player_id, season)
        return [self.__to_domain(g) for g in games]

    def __to_domain(self, g):
        return PlayerGameLog(
            date=g.gameDate,
            opponent=g.opponentAbbrev,
            goals=g.goals,
            assists=g.assists,
            points=g.points,
            pim=g.pim,
            plusMinus=g.plusMinus,
            powerPlayGoals=g.powerPlayGoals,
            powerPlayPoints=g.powerPlayPoints,
            timeOnIce=g.toi,
            shots=g.shots,
        )


if __name__ == '__main__':
    rows = GameLogService().get_player_gamelog(8478402)
    print(f"{len(rows)} rows")
    for r in rows[:3]:
        print(r)
