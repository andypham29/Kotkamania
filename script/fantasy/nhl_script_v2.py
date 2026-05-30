from typing import List

from domain.fantasygrade.fantasy_defense_grader_service import FantasyDefenseGraderService
from domain.fantasygrade.fantasy_forward_grader_service import FantasyForwardGraderService
from domain.fantasyplayer.fantasy_player_service import FantasyPlayerService
from domain.fantasyplayer.model.fantasy_nhl_player import FantasyPlayerUpdateQuery
from domain.playerstat.model.nhl_player_stat import PlayerStat
from domain.playerstat.nhl_player_stat_cache_service import NhlPlayerStatCacheService
from domain.playerstat.nhl_player_stat_service import NhlPlayerStatService
from infra.spi.nhlapi.nhl_team_roster_provider import NhlTeamRosterProvider
from infra.spi.nhlapi.nhl_team_service import NhlTeamService
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.nhl_team_converter import NhlTeamConverter


class NhlScriptV2:
    """Script to refresh player stats team-by-team and bulk-save into the SQLite cache."""

    def __init__(self):
        self.nhl_team_service = NhlTeamService()
        self.stat_facade = NhlPlayerStatService()
        self.cache_service = NhlPlayerStatCacheService()
        self.fantasy_grader = GraderHelper()
        self.fantasy_player_service = FantasyPlayerService(),
        self.nhl_team_roster_provider = NhlTeamRosterProvider()

    def get_players_stat_from_franchise(self, franchise_id: int, season_id: int) -> List[PlayerStat]:
        return self.stat_facade.get_all_players_from_franchise(franchise_id, season_id)

    def get_all_players(self, season_id: int = None) -> int:
        season_id = season_id or NhlYearConverter.get_current_season()
        total = 0
        for team in self.nhl_team_service.getAllTeams():
            stats = self.get_players_stat_from_franchise(team.franchiseId, season_id)
            written = self.cache_service.save_stats(stats)
            print(f"[{team.triCode}] saved {written} player stats")
            total += written
        print(f"\nDone. Total stats saved: {total}")
        return total

    def save_player_grade_for_all_players(self):

        player_ids = []
        for team_id in NhlTeamConverter.get_all_teamIds():
            player_ids += [player.id for player in self.nhl_team_roster_provider.get_roster_player_ids(team_id)]

    # TODO implement FantasyPlayer instantiation to store in db

    def reset_fantasy_players_table(self):
        self.fantasy_player_service.delete_all()
        print("Deleted all fantasy players from the database.")

class GraderHelper:
    def __init__(self):
        self.fantasy_forward_grader_service = FantasyForwardGraderService()
        self.fantasy_defense_grader_service = FantasyDefenseGraderService()
        self.nhl_team_roster_provider = NhlTeamRosterProvider()
        self.fantasy_player_service = FantasyPlayerService()

    def grade_all_players(self, season_id: int = None):
        season_id = season_id or NhlYearConverter.get_current_season()
        for team_id in NhlTeamConverter.get_all_teamIds():
            forward_ids = self.nhl_team_roster_provider.get_roster_player_ids_forward(team_id, season_id)
            defense_ids = self.nhl_team_roster_provider.get_roster_player_ids_defense(team_id, season_id)
            self.grade_all_forwards(forward_ids)
            self.grade_all_defenses(defense_ids)


    def grade_all_defenses(self, players):
        for player in players:
            defense_grade = self.fantasy_defense_grader_service.grade_defense(player.playerId)
            self.fantasy_player_service.update_fantasy_players(FantasyPlayerUpdateQuery(player.playerId, defense_grade))
            print(f"Player: {player.fullName}, Defense Grade: {defense_grade}")

    def grade_all_forwards(self, players):
        for player in players:
            forward_grade = self.fantasy_forward_grader_service.grade_forward(player.playerId)
            self.fantasy_player_service.update_fantasy_players(FantasyPlayerUpdateQuery(player.playerId, forward_grade))
            print(f"Player: {player.fullName}, Forward Grade: {forward_grade}")

if __name__ == '__main__':
    NhlScriptV2().get_all_players()
    NhlScriptV2().get_all_players("20242025")
    NhlScriptV2().get_all_players("20232024")
    NhlScriptV2().get_all_players("20222023")
    NhlScriptV2().get_all_players("20212022")
