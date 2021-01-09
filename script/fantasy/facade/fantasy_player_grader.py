from script.fantasy.fantasyhelper.fantasy_defense_grade_helper import FantasyDefenseGradeHelper
from script.fantasy.fantasyhelper.fantasy_forward_grade_helper import FantasyForwardGradeHelper
from script.fantasy.model.fantasy_player import FantasyPlayer
from server.internaldata.repository.player_stat_repository import InternalPlayerStatRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService


class FantasyPlayerGrader:

    def __init__(self,
                 fantasy_skater_grade_helper=FantasyForwardGradeHelper(),
                 fantasy_defense_grade_helper=FantasyDefenseGradeHelper(),
                 nhl_stats_leader_service=NHLStatsLeaderService(),
                 nhl_player_service_facade=NHLPlayerServiceFacade(),
                 fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../../server/internaldata/db/fantasy.db')):

        self.fantasy_forward_grade_service = fantasy_skater_grade_helper
        self.fantasy_defensemen_grade_service = fantasy_defense_grade_helper
        self.nhl_stats_leader_service = nhl_stats_leader_service
        self.nhl_player_service_facade = nhl_player_service_facade
        self.fantasy_nhl_player_service = fantasy_nhl_player_service

    def convert_to_fantasy_player(self, player):
        # years = ["20172018", "20182019", "20192020"]
        fantasy_value_20172018 = self.__convert_to_fantasy_player_by_year(player, "20172018")
        fantasy_value_20182019 = self.__convert_to_fantasy_player_by_year(player, "20182019")
        fantasy_value_20192020 = self.__convert_to_fantasy_player_by_year(player, "20192020")

        grade_20192020 = fantasy_value_20192020["grade"]
        grade_20182019 = grade_20192020 if (
                fantasy_value_20182019["grade"] <= 0 or fantasy_value_20182019["games"] < 10) else \
            fantasy_value_20182019["grade"] * 0.93
        grade_20172018 = grade_20192020 if (
                fantasy_value_20172018["grade"] <= 0 or fantasy_value_20172018["games"] < 10) else \
            fantasy_value_20172018["grade"] * 0.9

        grade = (grade_20192020 * 19 + grade_20182019 * 5 + grade_20172018 * 1) / 25
        print(f"[{player.skaterFullName}] 19-20:{grade_20192020}  18-19:{grade_20182019}  17-18:{grade_20172018} ")
        shotPct = fantasy_value_20192020["shotPct"]

        player_stat = InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
            player.playerId, "20192020")
        if player.positionCode == 'G' or not player_stat:
            return FantasyPlayer(player.playerId,
                                 player.skaterFullName,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0,
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

    def __convert_to_fantasy_player_by_year(self, player, year):
        player_stat = InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
            player.playerId, year)

        if player_stat is None and player.positionCode != 'G':
            stat = NHLPlayerStatService().get_player_stat_by_playerId_and_seasons(player.playerId, [year])
            # stat = self.nhl_player_service_facade \
            # .get_player_by_playerId_and_seasons(player.playerId, ["20192020"])
            p = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(player.playerId, [year])
            if not stat:
                return {"shotPct": 0,
                        "grade": 0,
                        "games": 0}

            player_stat = stat[0].stat
            InternalPlayerStatRepository().save_internal_player_stats(p)

        if player.positionCode == 'G':
            return {"shotPct": 0,
                    "grade": 0,
                    "games": 0}
        elif player.positionCode == 'D':
            shotPct = self.fantasy_defensemen_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_defensemen_grade_service.getDefenseGrade(player.skaterFullName, player_stat)
        else:
            shotPct = self.fantasy_forward_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_forward_grade_service.getForwardGrade(player.skaterFullName, player_stat)

        return {"shotPct": shotPct,
                "grade": grade,
                "games": player_stat.games}

    def __convert_to_fantasy_player_by_year2(self, player, year):
        player_stat = InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
            player.playerId, year)

        if player_stat is None and player.positionCode != 'G':
            stat = NHLPlayerStatService().get_player_stat_by_playerId_and_seasons(player.playerId, ["20192020"])
            # stat = self.nhl_player_service_facade \
            # .get_player_by_playerId_and_seasons(player.playerId, ["20192020"])
            p = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(player.playerId, ["20192020"])
            if not stat:
                return FantasyPlayer(player.playerId,
                                     player.skaterFullName,
                                     0,
                                     0,
                                     0,
                                     0,
                                     0,
                                     0,
                                     0)

            player_stat = stat[0].stat
            InternalPlayerStatRepository().save_internal_player_stats(p)

        if player.positionCode == 'G':
            return FantasyPlayer(player.playerId,
                                 player.skaterFullName,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0)
        elif player.positionCode == 'D':
            shotPct = self.fantasy_defensemen_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_defensemen_grade_service.getDefenseGrade(player.skaterFullName, player_stat)
        else:
            shotPct = self.fantasy_forward_grade_service.shotPctIndex(player_stat)
            grade = self.fantasy_forward_grade_service.getForwardGrade(player.skaterFullName, player_stat)
        return FantasyPlayer(player.playerId,
                             player.skaterFullName,
                             player_stat.games,
                             player_stat.goals,
                             player_stat.assists,
                             player_stat.points,
                             shotPct,
                             grade,
                             player_stat.powerPlayTimeOnIcePerGame)
