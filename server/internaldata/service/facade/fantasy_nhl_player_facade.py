from server.commons.fantasygrade.fantasy_percentile_calculator import FantasyPercentileCalculator
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.fantasy_player_streak_index_service import FantasyPlayerStreakIndexService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService


class FantasyNhlPlayerFacade:
    def __init__(self, uri_fantasy=None, uri_internal=None):
        self.uri_fantasy = uri_fantasy
        self.uri_internal = uri_internal

    def getAllFantasySkatersOnHotStreak(self, fantasy_players):

        streak_ids = [s.playerId for s in
                      FantasyPlayerStreakIndexService(self.uri_fantasy).getAllFantasyPlayerStreakIndexes()]

        list = []
        for id in streak_ids:
            try:
                player = next((x for x in fantasy_players if x.playerId == id), None)
                list.append(player)
            except:
                continue
        return list
        # return sorted(fantasy_players, key=lambda x: streak_ids.index(x.playerId))

    def getAllFantasySkaters(self,
                             positions, min_game, percentile_shot, percentile_hit, percentile_block, percentile_goal,
                             percentile_assist, percentile_point, percentile_toi, percentile_pptoi, percentile_evtoi):
        fantasy_players_service = FantasyNhlPlayerService(uri=self.uri_fantasy)
        internal_player_service = InternalPlayerStatService(uri=self.uri_internal)
        if not positions:
            fantasy_players = fantasy_players_service.getAllFantasySkaters()
        elif len(positions) == 1 and positions[0].upper() == 'G':
            fantasy_players = fantasy_players_service.getAllFantasySkatersWithPositionCodesWithStats(positions)
        else:
            fantasy_players = fantasy_players_service.getAllFantasySkatersWithPositionCodesWithStats(positions)
        user_percentile_params = [min_game, percentile_shot, percentile_hit, percentile_block, percentile_goal,
                                  percentile_assist, percentile_point, percentile_toi, percentile_pptoi,
                                  percentile_evtoi]
        if all([elem is None for elem in user_percentile_params]):
            return fantasy_players
        else:
            percentile_values = FantasyPercentileCalculator(fantasy_nhl_player_service=fantasy_players_service,
                                                            internal_player_stat_service=internal_player_service) \
                .get_percentile_stats(
                players=fantasy_players,
                min_game=min_game,
                percentile_shot=percentile_shot,
                percentile_hit=percentile_hit,
                percentile_block=percentile_block,
                percentile_goal=percentile_goal,
                percentile_assist=percentile_assist,
                percentile_point=percentile_point,
                percentile_toi=percentile_toi,
                percentile_pptoi=percentile_pptoi,
                percentile_evtoi=percentile_evtoi)

            print([(attr, value.__dict__) for attr, value in percentile_values.__dict__.items()])
            stats_at_percentiles = internal_player_service.get_internal_players_stats_at_percentile_values_and_seasonId(
                percentile_values,
                "20212022")
            # print([s.__dict__ for s in stats_at_percentiles])
            list_of_player_id = [s.playerId for s in stats_at_percentiles]

            return [player for player in fantasy_players if player.playerId in list_of_player_id]
