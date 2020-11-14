from script.fantasy.fantasyhelper.fantasy_forward_grade_helper import FantasyForwardGradeHelper
from script.fantasy.model.fantasy_skater import FantasyPlayer
from server.internaldata.repository.player_repository import InternalPlayerRepository
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService


class FantasyPlayerHelper:

    def __init__(self,
                 fantasy_skater_grade_helper=FantasyForwardGradeHelper(),
                 nhl_stats_leader_service=NHLStatsLeaderService(),
                 nhl_player_service_facade=NHLPlayerServiceFacade()):
        self.fantasy_player_grade_service = fantasy_skater_grade_helper
        self.nhl_stats_leader_service = nhl_stats_leader_service
        self.nhl_player_service_facade = nhl_player_service_facade

    def get_forward(self, amount=100):
        # counter = 0
        # players = []
        # while counter < amount:
        #     end_counter = amount if (100 - amount) > 0 else counter + 99
        #     players += self.nhl_stats_leader_service.getForwards(start=counter, end=end_counter)
        #     counter = end_counter + 1

        # players = self.nhl_stats_leader_service.getForwards(start=0, end=0)
        # players += self.nhl_stats_leader_service.getDefensemen(start=0, end=100)
        players = InternalPlayerRepository().get_all_forwards()
        # players = InternalPlayerRepository().save_internal_players(players)
        # players += self.nhl_stats_leader_service.getForwards(start=201, end=300)
        # players += self.nhl_stats_leader_service.getForwards(start=301, end=400)
        # players += self.nhl_stats_leader_service.getForwards(start=401, end=500)
        return [FantasyPlayer(player.playerId,
                              player.skaterFullName,
                              player.gamesPlayed,
                              player.goals,
                              player.assists,
                              player.points,
                              self.fantasy_player_grade_service.shotPctIndex(player.shootingPct * 100),
                              self.fantasy_player_grade_service.getForwardGrade(
                                  self.nhl_player_service_facade.get_player_stats_by_playerId_and_seasons(
                                      player.playerId)))
                for player in players]

    def get_defensemen(self, amount=100):
        counter = 0
        players = []
        # while counter < amount:
        #     end_counter = amount - counter if (100 - amount) < 0 else counter + 99
        #     players += self.nhl_stats_leader_service.getDefensemen(start=counter, end=end_counter)
        #     counter = end_counter + 1
        # players = self.nhl_stats_leader_service.getDefensemen(start=0, end=0)
        # players += self.nhl_stats_leader_service.getDefensemen(start=101, end=200)
        # InternalPlayerRepository().save_internal_players(players)
        players = InternalPlayerRepository().get_all_defensemen()
        return [FantasyPlayer(player.playerId,
                              player.skaterFullName,
                              player.gamesPlayed,
                              player.goals,
                              player.assists,
                              player.points,
                              self.fantasy_player_grade_service.shotPctIndex(player.shootingPct * 100),
                              self.fantasy_player_grade_service.getForwardGrade(
                                  self.nhl_player_service_facade.get_player_stats_by_playerId_and_seasons(
                                      player.playerId)))
                for player in players]
