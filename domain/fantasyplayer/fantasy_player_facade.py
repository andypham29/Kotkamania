from domain.fantasyplayer.model.fantasy_nhl_player import FantasyNhlPlayer, index_by_player_id
from infra.spi.sqlite.fantasyplayer.fantasy_player_repository import FantasyPlayerRepository
from infra.spi.sqlite.goaliestat.goalie_stat_repository import GoalieStatRepository
from infra.spi.sqlite.playerstat.nhl_player_stat_repository import NhlPlayerStatRepository
from infra.spi.sqlite.playerstatpercentile.nhl_player_stat_repository import NhlPlayerStatPercentileRepository
from server.commons.helper.nhl_season_converter import NhlYearConverter


class DomainFantasyPlayerFacade:

    def __init__(
        self,
        fantasy_player_repository: FantasyPlayerRepository | None = None,
        nhl_player_stat_repository: NhlPlayerStatRepository | None = None,
        nhl_player_stat_percentile_repository: NhlPlayerStatPercentileRepository | None = None,
        goalie_stat_repository: GoalieStatRepository | None = None,
    ):
        self.fantasy_player_repository = fantasy_player_repository or FantasyPlayerRepository()
        self.nhl_player_stat_repository = nhl_player_stat_repository or NhlPlayerStatRepository()
        self.nhl_player_stat_percentile_repository = (nhl_player_stat_percentile_repository or NhlPlayerStatPercentileRepository())
        self.goalie_stat_repository = goalie_stat_repository or GoalieStatRepository()

    def _current_season_id(self) -> int:
        return NhlYearConverter.get_previous_season_by_year_removed(0)

    def _load_skater_spi_context(self, season_id: int):
        stats = index_by_player_id(self.nhl_player_stat_repository.find_all(season_id))
        percentiles = index_by_player_id(self.nhl_player_stat_percentile_repository.find_all(season_id))
        return stats, percentiles

    def _assemble_players(self, players, stats, percentiles) -> list[FantasyNhlPlayer]:
        return [
            FantasyNhlPlayer.from_spi(
                player,
                stats.get(player_id),
                percentiles.get(player_id),
            )
            for player in players
            if (player_id := FantasyNhlPlayer.resolve_player_id(player)) is not None
        ]

    def getAllFantasySkaters(self) -> list[FantasyNhlPlayer]:
        season_id = self._current_season_id()
        players = self.fantasy_player_repository.getAllFantasySkaters()
        stats, percentiles = self._load_skater_spi_context(season_id)
        return self._assemble_players(players, stats, percentiles)

if __name__ == "__main__":
    facade = DomainFantasyPlayerFacade()
    players = facade.getAllFantasySkaters()
    print([player for player in players if player.positionCode == 'G'])