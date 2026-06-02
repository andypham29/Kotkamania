from dataclasses import fields
from typing import List, Optional

import numpy as np

from domain.playerstat.nhl_player_stat_cache_service import NhlPlayerStatCacheService
from infra.spi.sqlite.playerstat.model.nhl_player_stat import PlayerStat
from infra.spi.sqlite.playerstatpercentile.model.nhl_player_stat_percentile import PlayerStatPercentile

_IDENTIFIER_FIELDS = {"playerId", "seasonId"}

_PERCENTILE_FIELDS = [
    f.name for f in fields(PlayerStatPercentile) if f.name not in _IDENTIFIER_FIELDS
]


class NhlPlayerStatPercentileCalculator:
    """Computes percentile ranks for a single (playerId, seasonId) against the season cohort."""

    def __init__(self, stat_cache_service: Optional[NhlPlayerStatCacheService] = None):
        self.stat_cache_service = stat_cache_service or NhlPlayerStatCacheService()

    def calculate(self, player_id: int, season_id: int) -> Optional[PlayerStatPercentile]:
        target = self.stat_cache_service.get_stat_player_by_id(player_id, season_id)
        if target is None:
            return None

        cohort: List[PlayerStat] = [
            s for s in self.stat_cache_service.get_all_stats(season_id) if s is not None
        ]
        if not cohort:
            return None

        result = PlayerStatPercentile(playerId=player_id, seasonId=season_id)

        for field_name in _PERCENTILE_FIELDS:
            target_value = self._numeric(target, field_name)
            if target_value is None:
                continue

            population = [self._numeric(s, field_name) for s in cohort]
            population = [v for v in population if v is not None]
            if not population:
                continue

            arr = np.asarray(population, dtype=float)
            rank = float(np.sum(arr <= target_value)) / len(arr) * 100.0
            setattr(result, field_name, int(round(rank)))

        return result



    @staticmethod
    def _numeric(stat: PlayerStat, field_name: str) -> Optional[float]:
        value = getattr(stat, field_name, None)
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

if __name__ == "__main__":
    calculator = NhlPlayerStatPercentileCalculator()
    percentile = calculator.calculate(player_id=8478402, season_id=20252026)
    print(percentile)