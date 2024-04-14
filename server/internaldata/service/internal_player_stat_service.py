from server.internaldata.repository.internal_player_stat_dao import InternalPlayerStatDao


class InternalPlayerStatService:

    def __init__(self, uri=None):
        self.uri = uri

    def get_internal_all_players_stats_by_seasonId(self, seasonId):
        return InternalPlayerStatDao(uri=self.uri).get_internal_all_players_stats_by_seasonId(seasonId)

    def get_internal_players_stats_by_playerId_and_seasonId(self, playerId, seasonId):
        return InternalPlayerStatDao(uri=self.uri).get_internal_players_stats_by_playerId_and_seasonId(playerId,
                                                                                                       seasonId)

    def get_internal_players_stats_at_percentile_values_and_seasonId(self, percentile_values, seasonId):
        return InternalPlayerStatDao(uri=self.uri).get_internal_players_stats_at_percentile_values_and_seasonId(
            percentile_values, seasonId)

    def insert_internal_players_stats(self, playerId, seasonId, stat):
        try:
            InternalPlayerStatDao(uri=self.uri).insert_internal_players_stats(playerId, seasonId, stat)
            print(f"[{playerId}] Save internal stat {seasonId}")
        except Exception as e:
            print(e)
