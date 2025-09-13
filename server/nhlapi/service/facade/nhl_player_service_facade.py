from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.model.nhl_player import SeasonStat
from server.nhlapi.service.nhl_player_service import NHLPlayerService
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService


class NHLPlayerServiceFacade:

    def __init__(self, nhlPlayerService=NHLPlayerService(),
                 nhlPlayerStatService=NHLPlayerStatService(),
                 internalPlayerStatService=InternalPlayerStatService(),
                 fantasyPlayerService=FantasyNhlPlayerService()):
        self.nhlPlayerService = nhlPlayerService
        self.nhlPlayerStatService = nhlPlayerStatService
        self.internalPlayerStatService = internalPlayerStatService
        self.fantasyPlayerService = fantasyPlayerService

    def get_player_by_playerId_and_seasons(self, playerId, seasons=[]):
        season_current = NhlYearConverter.get_current_season()
        season_minus1 = NhlYearConverter.get_previous_season_by_year_removed(1)
        season_minus2 = NhlYearConverter.get_previous_season_by_year_removed(2)
        season_minus3 = NhlYearConverter.get_previous_season_by_year_removed(3)
        season_minus4 = NhlYearConverter.get_previous_season_by_year_removed(4)

        seasons = seasons if seasons else [season_minus4, season_minus3, season_minus2, season_minus1, season_current]
        player = self.nhlPlayerService.get_player_by_id(playerId)
        if player.playerDraftDetails:
            print(player.playerDraftDetails.__dict__)
        if player.position == "G":
            stats = self.nhlPlayerStatService.get_goalie_stat_by_playerId_and_season(playerId, seasons)
        else:
            stats = []
            for seasonId in seasons:
                stat = self.internalPlayerStatService.get_internal_players_stats_by_playerId_and_seasonId(playerId,
                                                                                                          seasonId)
                if stat is None:
                    continue
                stats.append(SeasonStat(seasonId, stat))

        # if len(stats) == 0:
        #     return player

        badge = self.fantasyPlayerService.getFantasySkaterById(playerId).badge
        player.stats = stats
        player.badge = badge

        return player
