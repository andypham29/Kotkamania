from server.commons.fantasygrade.fantasy_percentile_calculator import FantasyPercentileCalculator

from server.commons.fantasygrade.fantasy_player_grader_facade import FantasyPlayerGraderFacade
from server.commons.helper.nhl_season_converter import NhlYearConverter

from server.internaldata.repository.player_stat_repository import InternalPlayerStatRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService


class FantasyPlayerGradeFacade:

    def __init__(self,
                 # fantasy_skater_grade_helper=FantasyForwardGradeHelper(),
                 # fantasy_defense_grade_helper=FantasyDefenseGradeHelper(),
                 nhl_stats_leader_service=NHLStatsLeaderService(),
                 nhl_player_service_facade=NHLPlayerServiceFacade(),
                 fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../server/internaldata/db/internal.db')):
        # self.fantasy_forward_grade_service = fantasy_skater_grade_helper
        # self.fantasy_defensemen_grade_service = fantasy_defense_grade_helper
        self.nhl_stats_leader_service = nhl_stats_leader_service
        self.nhl_player_service_facade = nhl_player_service_facade
        self.fantasy_nhl_player_service = fantasy_nhl_player_service

    def save_player_stats(self):
        season_current = NhlYearConverter.get_current_season()
        # season_minus1 = NhlYearConverter.get_previous_season_by_year_removed(1)
        # season_minus2 = NhlYearConverter.get_previous_season_by_year_removed(2)
        # season_minus3 = NhlYearConverter.get_previous_season_by_year_removed(3)

        # TODO fetch all players (from fantasy or nhl teams)
        internal_players = []
        for player in internal_players:
            print(player.__dict__)
            p = self.nhl_player_service_facade \
                .get_player_by_playerId_and_seasons(playerId=player.playerId,
                                                    seasons=[season_current])
            InternalPlayerStatRepository().save_internal_player_stats(p)

    def update_fantasy_grade_forward(self, amount=100):
        # players = InternalPlayerRepository().get_forwards(amount)
        players = FantasyNhlPlayerService(
            '../../server/internaldata/db/internal.db').getAllFantasySkatersWithPositionCodesWithStats(["L", "C", "R"])[
                  :amount]
        f = FantasyPercentileCalculator(
            internal_player_stat_service=InternalPlayerStatService(uri='../../server/internaldata/db/internal.db'),
            fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../server/internaldata/db/internal.db'))

        return [self.__convert_to_fantasy_skater(player, f.get_all_stats_percentiles()) for player in players]

    def get_fantasy_defensemen(self, amount=100):
        # players = InternalPlayerRepository().get_defensemen(amount)
        players = FantasyNhlPlayerService(
            '../../server/internaldata/db/internal.db').getAllFantasySkatersWithPositionCodesWithStats(["D"])[:amount]

        f = FantasyPercentileCalculator(
            internal_player_stat_service=InternalPlayerStatService(uri='../../server/internaldata/db/internal.db'),
            fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../server/internaldata/db/internal.db'))

        return [self.__convert_to_fantasy_skater(player, f.get_all_stats_percentiles()) for player in players]

    def get_fantasy_goalie(self, amount=100):
        players = FantasyNhlPlayerService(
            '../../server/internaldata/db/internal.db').getAllFantasySkatersWithPositionCodesWithStats(["G"])[:amount]
        return [self.__convert_to_fantasy_player(player) for player in players]

    def get_all_fantasy_player_from_internal_db(self):
        players = self.fantasy_nhl_player_service.getAllFantasySkaters()

        return [self.__convert_to_fantasy_player(player) for player in players]

    def get_all_fantasy_forward_from_internal_db(self):
        players = self.fantasy_nhl_player_service.getAllFantasySkatersWithPositionCodesWithStats(['L', 'C', 'R'])

        return [self.__convert_to_fantasy_player(player) for player in players]

    def get_fantasy_grade_by_id(self, id):
        player = FantasyNhlPlayerService(
            '../../server/internaldata/db/internal.db').getFantasySkaterById(id)
        return FantasyPlayerGraderFacade().convert_to_fantasy_player(player)

    def __convert_to_fantasy_player(self, player):
        return FantasyPlayerGraderFacade().convert_to_fantasy_player(player)

    def __convert_to_fantasy_skater(self, player, percentile_stats_object):
        return FantasyPlayerGraderFacade(percentile_stats_object=percentile_stats_object) \
            .convert_to_fantasy_player(player)
