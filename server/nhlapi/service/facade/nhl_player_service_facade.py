from server.nhlapi.service.nhl_player_service import NHLPlayerService
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService


class NHLPlayerServiceFacade:

    def __init__(self, nhlPlayerService=NHLPlayerService(),
                 nhlPlayerStatService=NHLPlayerStatService()):
        self.nhlPlayerService = nhlPlayerService
        self.nhlPlayerStatService = nhlPlayerStatService

    def get_player_by_playerId_and_seasons(self, playerId, seasons=[""]):
        # seasons = ["20152016", "20162017", "20172018"]
        player = self.nhlPlayerService.get_player_by_id(playerId)
        if player.position == "G":
            stats = self.nhlPlayerStatService.get_goalie_stat_by_playerId_and_season(playerId, seasons)
        else:
            stats = self.nhlPlayerStatService.get_player_stat_by_playerId_and_seasons(playerId, seasons)

        player.stats = stats

        return player
