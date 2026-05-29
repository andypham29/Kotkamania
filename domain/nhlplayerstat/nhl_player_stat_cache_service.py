from typing import List, Optional

from domain.nhlplayerstat.model.nhl_player_stat import PlayerStat
from infra.spi.sqlite.playerstat.nhl_player_stat_repository import NhlPlayerStatRepository


class NhlPlayerStatCacheService:
    """Cache service for player stats — persists / retrieves through the SQLite repository."""

    def __init__(self, repository: Optional[NhlPlayerStatRepository] = None):
        self.repository = repository or NhlPlayerStatRepository()

    def get_stat_player_by_id(self, player_id: int, season_id: int) -> Optional[PlayerStat]:
        return self.repository.find_by_player_id(player_id, season_id)

    def save_stat(self, player_stat: PlayerStat) -> None:
        self.repository.save(player_stat)

    def save_stats(self, player_stats: List[PlayerStat]) -> int:
        return self.repository.save_all(player_stats)
