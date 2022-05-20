from server.commons.fantasygrade.fantasy_defense_grade_helper import FantasyDefenseGradeHelper
from server.commons.fantasygrade.fantasy_forward_grade_helper import FantasyForwardGradeHelper
from server.commons.fantasygrade.fantasy_goalie_grade_helper import FantasyGoalieGradeHelper
from server.commons.fantasygrade.fantasy_player_grader import FantasyPlayerGrader, Grade
from server.commons.model.fantasy_player import FantasyPlayer
from server.internaldata.repository.player_stat_repository import InternalPlayerStatRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService


class FantasyPlayerGraderFacade:

    def __init__(self,
                 fantasy_skater_grade_helper=FantasyForwardGradeHelper(),
                 fantasy_defense_grade_helper=FantasyDefenseGradeHelper(),
                 fantasy_goalie_grade_helper=FantasyGoalieGradeHelper(),
                 nhl_stats_leader_service=NHLStatsLeaderService(),
                 nhl_player_service_facade=NHLPlayerServiceFacade(),
                 fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../../server/internaldata/db/fantasy.db')):

        self.fantasy_forward_grade_service = fantasy_skater_grade_helper
        self.fantasy_defensemen_grade_service = fantasy_defense_grade_helper
        self.fantasy_goalie_grade_helper = fantasy_goalie_grade_helper
        self.nhl_stats_leader_service = nhl_stats_leader_service
        self.nhl_player_service_facade = nhl_player_service_facade
        self.fantasy_nhl_player_service = fantasy_nhl_player_service

    def convert_to_fantasy_player(self, player):
        current_year = 2022
        fantasy_value_year1 = self.__get_fantasy_player_by_year(player, f"{current_year - 4}{current_year - 3}")
        fantasy_value_year2 = self.__get_fantasy_player_by_year(player, f"{current_year - 3}{current_year - 2}")
        fantasy_value_year3 = self.__get_fantasy_player_by_year(player, f"{current_year - 2}{current_year - 1}")
        fantasy_value_year4 = self.__get_fantasy_player_by_year(player, f"{current_year - 1}{current_year}")

        playoff_stat = NHLPlayerStatService().get_player_playoff_stat_by_playerId_and_seasons(player.playerId,
                                                                                              "20202021")
        # grade_20202021_p = 0
        # grade_20202021_p = 0 if len(playoff_stat) == 0 else\
        #     self.fantasy_forward_grade_service.getForwardGrade(player.skaterFullName, playoff_stat)

        grade_year4 = fantasy_value_year4["grade"]
        grade_year3 = grade_year4 if (
                fantasy_value_year3["grade"] <= 0 or fantasy_value_year3["games"] < 10) else \
            fantasy_value_year3["grade"] * 1.0125
        grade_year2 = grade_year4 if (
                fantasy_value_year2["grade"] <= 0 or fantasy_value_year2["games"] < 10) else \
            fantasy_value_year2["grade"] * 0.98
        grade_year1 = grade_year4 if (
                fantasy_value_year1["grade"] <= 0 or fantasy_value_year1["games"] < 10) else \
            fantasy_value_year1["grade"] * 0.95

        # grade = 0
        # if (grade_20202021_p > 0):
        #     grade = (grade_20202021_p * 4 +grade_20202021 * 7 + grade_20192020 * 8 + grade_20182019 * 5 + grade_20172018 * 1) / 25
        # else:
        #     grade = (grade_20202021 * 7 + grade_20192020 * 12 + grade_20182019 * 5 + grade_20172018 * 1) / 25
        # grade = round(grade, 2)

        grade = FantasyPlayerGrader.calculate_overall_grade(
            player.skaterFullName,
            Grade(
                grade_year4,
                grade_year3,
                grade_year2,
                grade_year1
            )
        )
        print(
            f"[{player.skaterFullName}] {current_year - 2}{current_year - 1}:{grade_year3}  {current_year - 3}{current_year - 2}:{grade_year2}  {current_year - 4}{current_year - 3}:{grade_year1} ")
        shotPct = fantasy_value_year3["shotPct"]

        player_stat = InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
            player.playerId, f"{current_year - 1}{current_year}")
        if not player_stat:
            return FantasyPlayer(player.playerId,
                                 player.skaterFullName,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0,
                                 grade,
                                 0)

        return FantasyPlayer(player.playerId,
                             player.skaterFullName,
                             player_stat.games,
                             player_stat.goals,
                             player_stat.assists,
                             player_stat.points,
                             round(shotPct, 2),
                             round(grade, 2),
                             player_stat.powerPlayTimeOnIcePerGame)

    def __get_fantasy_player_by_year(self, player, year):
        player_stat = InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
            player.playerId, year)
        if player_stat is None:
            if player.positionCode == 'G':
                stat = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(player.playerId, [year]).stats
            else:
                stat = NHLPlayerStatService().get_player_stat_by_playerId_and_seasons(player.playerId, [year])
                p = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(player.playerId, [year])
                # if year == "20212022":
                #     InternalPlayerStatRepository().save_internal_player_stats(p)

            if not stat:
                return {"shotPct": 0,
                        "grade": 0,
                        "games": 0}

            player_stat = stat[0].stat

        if player.positionCode == 'G':
            shotPct = 0
            grade = self.fantasy_goalie_grade_helper.getGoalieGrade(player.skaterFullName, player_stat)
        elif player.positionCode == 'D':
            shotPct = self.fantasy_defensemen_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_defensemen_grade_service.getDefenseGrade(player.skaterFullName, player_stat)
        else:
            shotPct = self.fantasy_forward_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_forward_grade_service.getForwardGrade(player.skaterFullName, player_stat)

        return {"shotPct": shotPct,
                "grade": round(grade, 2),
                "games": player_stat.games}
