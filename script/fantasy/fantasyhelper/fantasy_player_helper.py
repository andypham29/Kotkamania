from script.fantasy.fantasyhelper.fantasy_defense_grade_helper import FantasyDefenseGradeHelper
from script.fantasy.fantasyhelper.fantasy_forward_grade_helper import FantasyForwardGradeHelper
from script.fantasy.model.fantasy_player import FantasyPlayer
from server.internaldata.repository.player_repository import InternalPlayerRepository
from server.internaldata.repository.player_stat_repository import InternalPlayerStatRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService


class FantasyPlayerHelper:

    def __init__(self,
                 fantasy_skater_grade_helper=FantasyForwardGradeHelper(),
                 fantasy_defense_grade_helper=FantasyDefenseGradeHelper(),
                 nhl_stats_leader_service=NHLStatsLeaderService(),
                 nhl_player_service_facade=NHLPlayerServiceFacade(),
                 fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../server/internaldata/db/fantasy.db')):

        self.fantasy_forward_grade_service = fantasy_skater_grade_helper
        self.fantasy_defensemen_grade_service = fantasy_defense_grade_helper
        self.nhl_stats_leader_service = nhl_stats_leader_service
        self.nhl_player_service_facade = nhl_player_service_facade
        self.fantasy_nhl_player_service = fantasy_nhl_player_service

    def save_player_stats(self):
        internal_players = InternalPlayerRepository().get_forwards(amount=250)
        internal_players += InternalPlayerRepository().get_defensemen(amount=150)
        nhl_players = []
        for player in internal_players:
            print(player.__dict__)
            p = self.nhl_player_service_facade \
                .get_player_by_playerId_and_seasons(playerId=player.playerId,
                                                    seasons=["20102011", "20112012", "20122013",
                                                             "20132014", "20142015"])
            # nhl_players.append(self.nhl_player_service_facade \
            #                    .get_player_by_playerId_and_seasons(playerId=player.playerId,
            #                                                        seasons=["20152016", "20162017", "20172018",
            #                                                                 "20182019", "20192020"]))

            InternalPlayerStatRepository().save_internal_player_stats(p)
        # InternalPlayerStatRepository().bulk_save_internal_players_stats(nhl_players[])

    def get_fantasy_forward(self, amount=100):
        # counter = 0
        # players = []
        # while counter < amount:
        #     end_counter = amount if (100 - amount) > 0 else counter + 99
        #     players += self.nhl_stats_leader_service.getForwards(start=counter, end=end_counter)
        #     counter = end_counter + 1

        # players = self.nhl_stats_leader_service.getForwards(start=0, end=0)
        # players += self.nhl_stats_leader_service.getDefensemen(start=0, end=100)
        players = InternalPlayerRepository().get_forwards(amount)
        # players = InternalPlayerRepository().save_internal_players(players)
        # players += self.nhl_stats_leader_service.getForwards(start=201, end=300)
        # players += self.nhl_stats_leader_service.getForwards(start=301, end=400)
        # players += self.nhl_stats_leader_service.getForwards(start=401, end=500)

        return [self.__convert_to_fantasy_player(player) for player in players]

    def get_fantasy_defensemen(self, amount=100):
        counter = 0
        players = []
        # while counter < amount:
        #     end_counter = amount - counter if (100 - amount) < 0 else counter + 99
        #     players += self.nhl_stats_leader_service.getDefensemen(start=counter, end=end_counter)
        #     counter = end_counter + 1
        # players = self.nhl_stats_leader_service.getDefensemen(start=0, end=0)
        # players += self.nhl_stats_leader_service.getDefensemen(start=101, end=200)
        # InternalPlayerRepository().save_internal_players(players)
        players = InternalPlayerRepository().get_defensemen(amount)

        return [self.__convert_to_fantasy_player(player) for player in players]

    def get_all_fantasy_player_from_internal_db(self):
        players = self.fantasy_nhl_player_service.getAllFantasySkaters()

        return [self.__convert_to_fantasy_player(player) for player in players]

    def __convert_to_fantasy_player(self, player):
        player_stat = InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
            player.playerId, "20192020")

        if player_stat is None and player.positionCode != 'G':
            stat = NHLPlayerStatService().get_player_stat_by_playerId_and_seasons(player.playerId, ["20192020"])
            # stat = self.nhl_player_service_facade \
            # .get_player_by_playerId_and_seasons(player.playerId, ["20192020"])
            p = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(player.playerId, ["20192020"])
            if not stat:
                return FantasyPlayer(player.playerId,
                                     player.skaterFullName,
                                     0,
                                     0,
                                     0,
                                     0,
                                     0,
                                     0)

            player_stat = stat[0].stat
            InternalPlayerStatRepository().save_internal_player_stats(p)

        if player.positionCode == 'G':
            return FantasyPlayer(player.playerId,
                                 player.skaterFullName,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0)
        elif player.positionCode == 'D':
            shotPct = self.fantasy_defensemen_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_defensemen_grade_service.getDefenseGrade(player.skaterFullName, player_stat)
        else:
            shotPct = self.fantasy_forward_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_forward_grade_service.getForwardGrade(player.skaterFullName, player_stat)
        return FantasyPlayer(player.playerId,
                             player.skaterFullName,
                             player_stat.games,
                             player_stat.goals,
                             player_stat.assists,
                             player_stat.points,
                             shotPct,
                             grade)
