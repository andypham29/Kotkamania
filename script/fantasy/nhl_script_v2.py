from typing import List

import script
from application.goaliestats.goalie_stat_facade import GoalieStatFacade
from application.goaliestats.goalie_stat_service import GoalieStatService
from domain.fantasygrade.fantasy_defense_grader_service import FantasyDefenseGraderService
from domain.fantasygrade.fantasy_forward_grader_service import FantasyForwardGraderService
from domain.fantasyplayer.fantasy_player_service import FantasyPlayerService
from domain.fantasyplayer.model.fantasy_nhl_player import FantasyPlayerUpdateQuery
from domain.playerstatpercentile.nhl_player_stat_percentile_calculator import NhlPlayerStatPercentileCalculator
from infra.spi.sqlite.playerstat.model.nhl_player_stat import PlayerStat
from domain.playerstat.nhl_player_stat_cache_service import NhlPlayerStatCacheService
from domain.playerstat.nhl_player_stat_facade import NhlPlayerStatFacade
from infra.spi.nhlapi.nhl_team_roster_provider import NhlTeamRosterProvider
from infra.spi.nhlapi.nhl_team_service import NhlTeamService
from infra.spi.sqlite.fantasyplayer.fantasy_player_repository import FantasyPlayerRepository
from infra.spi.sqlite.playerstatpercentile.nhl_player_stat_repository import NhlPlayerStatPercentileRepository
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.nhl_team_converter import NhlTeamConverter


class MasterScript:
    def __init__(self):
        self.nhl_script = NhlScriptV2()
        self.fantasy_grader = FantasyPlayerGraderScript()
        self.percentile_script = PercentileScript()
        self.goalie_script = GoalieScript()

    def run(self):
        # self.nhl_script.save_all_players()
        self.nhl_script.reset_fantasy_players_table()
        self.nhl_script.save_player_grade_for_all_players()

    def run_score(self):
        self.fantasy_grader.grade_all_players()

    def run_percentile(self):
        self.percentile_script.calculate_percentile_for_all_players()

    def run_goalie(self):
        self.goalie_script.save_all_goalies_stats()


class NhlScriptV2:
    """Script to refresh player stats team-by-team and bulk-save into the SQLite cache."""
    def __init__(self):
        self.nhl_team_service = NhlTeamService()
        self.stat_facade = NhlPlayerStatFacade()
        self.cache_service = NhlPlayerStatCacheService()
        self.fantasy_grader = FantasyPlayerGraderScript()
        self.fantasy_player_repository = FantasyPlayerRepository()
        self.nhl_team_roster_provider = NhlTeamRosterProvider()

    def get_players_stat_from_franchise(self, franchise_id: int, season_id: int) -> List[PlayerStat]:
        return self.stat_facade.get_all_players_from_franchise(franchise_id, season_id)

    def save_all_players(self, season_id: int = None) -> int:
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

        roster_map = {}
        for team_id in NhlTeamConverter.get_all_teamIds():
            try:
                print(f"Getting roster for team: {team_id}")
                roster_map[team_id] = self.nhl_team_roster_provider.get_roster_all_player_infos(team_id)
            except Exception as e:
                print(f"Skip team: {team_id} because of: {str(e)}")

        for team_id in roster_map:
            team_name = NhlTeamConverter.get_abbreviation_by_teamId(team_id)
            for player in roster_map[team_id]:
                fantasy_player = player.to_fantasy_player()
                fantasy_player.teamId = team_id
                fantasy_player.teamName = team_name

                self.fantasy_player_repository.create_fantasy_player(fantasy_player)
                print(f"[{team_name}] Inserting fantasy player into the database: {fantasy_player.skaterFullName}")

    def reset_fantasy_players_table(self):
        self.fantasy_player_repository.delete_all()
        print("Deleted all fantasy players from the database.")


class FantasyPlayerGraderScript:
    def __init__(self):
        self.fantasy_forward_grader_service = FantasyForwardGraderService()
        self.fantasy_defense_grader_service = FantasyDefenseGraderService()
        self.nhl_team_roster_provider = NhlTeamRosterProvider()
        self.fantasy_player_service = FantasyPlayerService()

    def grade_all_players(self, season_id: int = None):
        season_id = season_id or NhlYearConverter.get_current_season()
        for team_id in NhlTeamConverter.get_all_teamIds():
            try:
                print(f"Grading players for team: {team_id}")
                forwards = self.nhl_team_roster_provider.get_roster_player_infos_forward(team_id, season_id)
                defenses = self.nhl_team_roster_provider.get_roster_player_infos_defense(team_id, season_id)
                self.grade_all_forwards(forwards)
                self.grade_all_defenses(defenses)
            except Exception as e:
                print(f"Error occurred while grading players for team {team_id}: {str(e)}")

        print("\nDone grading all players.")

    def grade_all_defenses(self, players):
        queries =[FantasyPlayerUpdateQuery(
            player.id,
            self.fantasy_defense_grader_service.grade_defense(player.id, player.full_name())
        ) for player in players]

        self.fantasy_player_service.update_fantasy_players(queries)

    def grade_all_forwards(self, players):
        queries =[FantasyPlayerUpdateQuery(
            player.id,
            self.fantasy_forward_grader_service.grade_forward(player.id, player.full_name())
        ) for player in players]

        self.fantasy_player_service.update_fantasy_players(queries)

class PercentileScript:
    def __init__(self):
        self.nhl_team_roster_provider = NhlTeamRosterProvider()
        self.fantasy_player_service = FantasyPlayerService()
        self.percentile_calculator = NhlPlayerStatPercentileCalculator()
        self.percentile_player_repository = NhlPlayerStatPercentileRepository()


    def calculate_percentile_for_all_players(self, season_id: int = None):
        season_id = season_id or NhlYearConverter.get_current_season()
        for team_id in NhlTeamConverter.get_all_teamIds():
            try:
                print(f"Calculating percentile for players for team: {team_id}")
                forwards = self.nhl_team_roster_provider.get_roster_player_infos_forward(team_id, season_id)
                defenses = self.nhl_team_roster_provider.get_roster_player_infos_defense(team_id, season_id)

                for player in forwards + defenses:
                    self._calculate_percentile(player.id, season_id)
            except Exception as e:
                print(f"Error occurred saving percentiles for players for team {team_id}: {str(e)}")

    def _calculate_percentile(self, player_id: int, season_id: int):
        percentile = self.percentile_calculator.calculate(player_id=player_id, season_id=season_id)
        print(f"Calculated percentile for player {player_id} in season {season_id}: {percentile}")
        if percentile is not None:
            self.percentile_player_repository.save(percentile)

class GoalieScript:
    def __init__(self):
        self.fantasy_player_service = FantasyPlayerService()
        self.goalie_stat_service = GoalieStatService()
        self.goalie_stat_facade = GoalieStatFacade()

    def save_all_goalies_stats(self, season_id: int = None):
        self.goalie_stat_facade.save_all_goalie_stats()
        print("Done saving all goalie stats.")

if __name__ == '__main__':
    # NhlScriptV2().get_all_players()
    # NhlScriptV2().get_all_players("20242025")
    # NhlScriptV2().get_all_players("20232024")
    # NhlScriptV2().get_all_players("20222023")
    # NhlScriptV2().get_all_players("20212022")

    script = MasterScript()
    # script.run()
    # script.run_score()
    # script.run_percentile()
    script.run_goalie()
