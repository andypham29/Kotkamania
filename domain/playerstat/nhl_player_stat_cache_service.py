from typing import List, Optional

from domain.playerstat.model.nhl_player_stat import PlayerStat
from infra.spi.sqlite.playerstat.nhl_player_stat_repository import NhlPlayerStatRepository


class NhlPlayerStatCacheService:
    """Cache service for player stats — persists / retrieves through the SQLite repository."""

    def __init__(self, repository: Optional[NhlPlayerStatRepository] = None):
        self.repository = repository or NhlPlayerStatRepository()

    def get_all_stats(self, season_id: int) -> list[PlayerStat | None]:
        return self.repository.find_all(season_id)

    def get_stat_player_by_id(self, player_id: int, season_id: int) -> Optional[PlayerStat]:
        return self.repository.find_by_player_id(player_id, season_id)

    def save_stat(self, player_stat: PlayerStat) -> None:
        self.repository.save(player_stat)

    def save_stats(self, player_stats: List[PlayerStat]) -> int:
        return self.repository.save_all(player_stats)

    def get_all_max_stat(self, season_id: int) -> Optional[PlayerStat]:
        return self.repository.find_max_stat(season_id)

    def get_all_min_stat(self, season_id: int) -> Optional[PlayerStat]:
        return self.repository.find_min_stat(season_id)
