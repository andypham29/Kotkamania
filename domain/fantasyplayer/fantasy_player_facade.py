from dataclasses import fields
from types import SimpleNamespace

from application.percentilecalculator import PercentileCalculator
from domain.fantasyplayer.model.fantasy_nhl_player import DisplayGoalieStat, FantasyNhlPlayer, index_by_player_id
from infra.spi.sqlite.fantasyplayer.fantasy_player_repository import FantasyPlayerRepository
from infra.spi.sqlite.goaliestat.goalie_stat_repository import GoalieStatRepository
from infra.spi.sqlite.playerstat.nhl_player_stat_repository import NhlPlayerStatRepository
from infra.spi.sqlite.playerstatpercentile.nhl_player_stat_repository import NhlPlayerStatPercentileRepository
from server.commons.helper.nhl_season_converter import NhlYearConverter

_NON_PERCENTILED_GOALIE_FIELDS = {"goalieFullName", "lastName", "shootsCatches", "teamAbbrevs", "playerId", "seasonId"}
_NUMERIC_GOALIE_FIELDS = tuple(
    field.name for field in fields(DisplayGoalieStat) if field.name not in _NON_PERCENTILED_GOALIE_FIELDS
)


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

    def _build_goalie_percentile_lookup(self, goalie_stats) -> dict[int, SimpleNamespace]:
        stats_list = [stat for stat in goalie_stats if stat and getattr(stat, "playerId", None) is not None]
        if not stats_list:
            return {}

        player_ids = [int(stat.playerId) for stat in stats_list]
        percentile_values = {player_id: {} for player_id in player_ids}
        calculator = PercentileCalculator()

        for field_name in _NUMERIC_GOALIE_FIELDS:
            entries = {
                str(stat.playerId): float(getattr(stat, field_name, 0) or 0)
                for stat in stats_list
            }
            field_percentiles = calculator.calculate(entries)
            for player_id in player_ids:
                percentile_values[player_id][field_name] = field_percentiles.get(str(player_id))

        return {
            player_id: SimpleNamespace(**percentile_values[player_id])
            for player_id in player_ids
        }

    def _load_goalie_spi_context(self, season_id: int):
        goalie_stats = self.goalie_stat_repository.find_all_by_season_id(season_id)
        return (
            index_by_player_id(goalie_stats),
            self._build_goalie_percentile_lookup(goalie_stats),
        )

    def _assemble_players(
        self,
        players,
        stats,
        percentiles,
        goalie_stats,
        goalie_percentiles,
    ) -> list[FantasyNhlPlayer]:
        return [
            FantasyNhlPlayer.from_spi(
                player,
                player_stat=stats.get(player_id) if player.positionCode != "G" else None,
                player_percentile=percentiles.get(player_id) if player.positionCode != "G" else None,
                goalie_stat=goalie_stats.get(player_id) if player.positionCode == "G" else None,
                goalie_percentile=goalie_percentiles.get(player_id) if player.positionCode == "G" else None,
            )
            for player in players
            if (player_id := FantasyNhlPlayer.resolve_player_id(player)) is not None
        ]

    def getAllFantasySkaters(self) -> list[FantasyNhlPlayer]:
        season_id = self._current_season_id()
        players = self.fantasy_player_repository.getAllFantasySkaters()
        stats, percentiles = self._load_skater_spi_context(season_id)
        goalie_stats, goalie_percentiles = self._load_goalie_spi_context(season_id)
        return self._assemble_players(players, stats, percentiles, goalie_stats, goalie_percentiles)

if __name__ == "__main__":
    facade = DomainFantasyPlayerFacade()
    players = facade.getAllFantasySkaters()
    # print([player for player in players if player.positionCode == 'G'])
    print([player for player in players if player.positionCode == 'L'])