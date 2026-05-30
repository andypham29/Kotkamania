from typing import List

from domain.playerstat.model.nhl_player_stat import PlayerStat
from domain.playerstat.nhl_player_stat_cache_service import NhlPlayerStatCacheService
from domain.playerstat.nhl_player_stat_service import NhlPlayerStatService
from infra.spi.nhlapi.nhl_team_service import NhlTeamService
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.nhl_team_converter import NhlTeamConverter


class NhlScriptV2:
    """Script to refresh player stats team-by-team and bulk-save into the SQLite cache."""

    def __init__(self,
                 nhl_team_service: NhlTeamService = None,
                 stat_facade: NhlPlayerStatService = None,
                 cache_service: NhlPlayerStatCacheService = None):
        self.nhl_team_service = nhl_team_service or NhlTeamService()
        self.stat_facade = stat_facade or NhlPlayerStatService()
        self.cache_service = cache_service or NhlPlayerStatCacheService()

    def get_players_from_franchise(self, franchise_id: int, season_id: int) -> List[PlayerStat]:
        return self.stat_facade.get_all_players_from_franchise(franchise_id, season_id)

    def get_all_players(self, season_id: int = None) -> int:
        season_id = season_id or NhlYearConverter.get_current_season()
        total = 0
        for team in self.nhl_team_service.getAllTeams():
            stats = self.get_players_from_franchise(team.franchiseId, season_id)
            written = self.cache_service.save_stats(stats)
            print(f"[{team.triCode}] saved {written} player stats")
            total += written
        print(f"\nDone. Total stats saved: {total}")
        return total


if __name__ == '__main__':
    NhlScriptV2().get_all_players()
    NhlScriptV2().get_all_players("20242025")
    NhlScriptV2().get_all_players("20232024")
    NhlScriptV2().get_all_players("20222023")
    NhlScriptV2().get_all_players("20212022")
