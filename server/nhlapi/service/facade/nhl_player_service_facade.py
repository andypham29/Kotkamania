from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.model.nhl_player import SeasonStat
from server.nhlapi.service.nhl_player_service import NHLPlayerService
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService


class NHLPlayerServiceFacade:

    def __init__(self, nhlPlayerService=NHLPlayerService(),
                 nhlPlayerStatService=NHLPlayerStatService(),
                 internalPlayerStatService=InternalPlayerStatService()):
        self.nhlPlayerService = nhlPlayerService
        self.nhlPlayerStatService = nhlPlayerStatService
        self.internalPlayerStatService = internalPlayerStatService

    def get_player_by_playerId_and_seasons(self, playerId):
        seasons = ["20162017", "20172018", "20182019", "20192020", "20202021"]
        player = self.nhlPlayerService.get_player_by_id(playerId)
        if player.position == "G":
            stats = self.nhlPlayerStatService.get_goalie_stat_by_playerId_and_season(playerId, seasons)
        else:
            stats = []
            for seasonId in seasons:
                stat = self.internalPlayerStatService.get_internal_players_stats_by_playerId_and_seasonId(playerId,
                                                                                                          seasonId)
                if stat is None:
                    player_stat = self.nhlPlayerStatService.get_player_stat_by_playerId_and_seasons(playerId,
                                                                                                    [seasonId])
                    if len(player_stat) > 0:
                        stat = player_stat[0].stat

                        if seasonId != "20202021":
                            self.internalPlayerStatService.insert_internal_players_stats(playerId, seasonId, stat)
                    print(f"[{playerId}] Statistic for season {seasonId} from NHLAPI")

                if stat is None:
                    continue
                stats.append(SeasonStat(seasonId, stat))

            # stats = self.nhlPlayerStatService.get_player_stat_by_playerId_and_seasons(playerId, seasons)

        player.stats = stats

        return player
