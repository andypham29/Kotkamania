from script.fantasy.fantasyhelper.excel_helper import ExcelHelper
from script.fantasy.fantasyhelper.fantasy_skater_grade_helper import FantasySkaterGradeHelper
from script.fantasy.model.fantasy_skater import FantasyPlayer
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService


class FantasyFacade:

    def __init__(self,
                 fantasy_skater_grade_helper=FantasySkaterGradeHelper(),
                 nhl_stats_leader_service=NHLStatsLeaderService(),
                 nhl_player_service_facade=NHLPlayerServiceFacade()):
        self.fantasy_player_grade_service = fantasy_skater_grade_helper
        self.nhl_stats_leader_service = nhl_stats_leader_service
        self.nhl_player_service_facade = nhl_player_service_facade

    def get_skaters(self):
        players = self.nhl_stats_leader_service.getForwards(start=0, end=100)
        # players += self.nhl_stats_leader_service.getForward(start=101, end=200)
        # players += self.nhl_stats_leader_service.getForward(start=201, end=300)
        # players += self.nhl_stats_leader_service.getForward(start=301, end=400)
        # players += self.nhl_stats_leader_service.getForward(start=401, end=500)
        return [FantasyPlayer(player.playerId,
                              player.skaterFullName,
                              player.gamesPlayed,
                              player.goals,
                              player.assists,
                              player.points,
                              self.fantasy_player_grade_service.shotPctIndex(player.shootingPct * 100),
                              self.fantasy_player_grade_service.getSkaterGrade(
                                  self.nhl_player_service_facade.get_player_stats_by_playerId_and_seasons(
                                      player.playerId)))
                for player in players]

    def get_defensemen(self):
        players = self.nhl_stats_leader_service.getDefensemen(start=0, end=100)
        # players += self.nhl_stats_leader_service.getDefensemen(start=101, end=200)
        return [FantasyPlayer(player.playerId,
                              player.skaterFullName,
                              player.gamesPlayed,
                              player.goals,
                              player.assists,
                              player.points,
                              self.fantasy_player_grade_service.shotPctIndex(player.shootingPct * 100),
                              self.fantasy_player_grade_service.getSkaterGrade(
                                  self.nhl_player_service_facade.get_player_stats_by_playerId_and_seasons(
                                      player.playerId)))
                for player in players]


if __name__ == '__main__':
    excel_helper = ExcelHelper()

    fantasy_skaters = FantasyFacade().get_skaters()
    fantasy_skaters.sort(key=lambda x: x.score, reverse=True)
    excel_helper.write_players_to_excel(sheet='forward', players=fantasy_skaters)

    # fantasy_defensemen = FantasyFacade().get_defensemen()
    # fantasy_defensemen.sort(key=lambda x: x.score, reverse=True)
    # excel_helper.write_players_to_excel(sheet='defense', players=fantasy_defensemen)

    excel_helper.close()
