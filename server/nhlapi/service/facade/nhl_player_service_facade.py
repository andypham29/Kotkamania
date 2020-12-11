from server.internaldata.repository.player_repository import InternalPlayerRepository
from server.internaldata.repository.player_stat_repository import InternalPlayerStatRepository
from server.nhlapi.service.nhl_player_service import NHLPlayerService
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService


class NHLPlayerServiceFacade:

    def __init__(self, nhlPlayerService=NHLPlayerService(),
                 nhlPlayerStatService=NHLPlayerStatService(),
                 internalPlayerRepository=InternalPlayerRepository(),
                 internalPlayerStatRepository=InternalPlayerStatRepository()):
        self.nhlPlayerService = nhlPlayerService
        self.nhlPlayerStatService = nhlPlayerStatService
        self.internalPlayerRepository = internalPlayerRepository
        self.internalPlayerStatRepository = internalPlayerStatRepository

    def get_player_by_playerId_and_seasons(self, playerId, seasons=[""]):
        # seasons = ["20152016", "20162017", "20172018"]
        player = self.nhlPlayerService.get_player_by_id(playerId)
        if player.position == "G":
            stats = self.nhlPlayerStatService.get_goalie_stat_by_playerId_and_season(playerId, seasons)
        else:
            stats = self.nhlPlayerStatService.get_player_stat_by_playerId_and_seasons(playerId, seasons)

        player.stats = stats

        return player

    def get_skater_by_playerId_and_seasons_internally(self, playerId):
        player = self.internalPlayerRepository.get_player_by_id(playerId)
        stats = self.internalPlayerStatRepository.get_internal_player_stats_by_playerId(playerId)

        player.stats = stats

        return player

    def get_skaters_and_seasons_internally(self):
        players = self.internalPlayerRepository.get_all_players()[:100]

        return players
