from domain.playerstat.model.nhl_player_stat import PlayerStat
from domain.playerstat.nhl_player_stat_cache_service import NhlPlayerStatCacheService
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.time_converter import TimeConverter


class FantasyForwardGraderService:

    def __init__(self):
        self.nhl_player_stat_service = NhlPlayerStatCacheService()
        pass

    def grade_forward(self,player_id, player_name, min_stat=None, max_stat=None):
        season_id = NhlYearConverter.get_current_season()

        player_stat = self.nhl_player_stat_service.get_stat_player_by_id(player_id, season_id)
        if player_stat is None:
            print(f"[{player_name}] Player stat not found for player_id: {player_id}")
            return None
        max_stat = self.nhl_player_stat_service.get_all_max_stat(season_id) if max_stat is None else max_stat
        min_stat = self.nhl_player_stat_service.get_all_min_stat(season_id) if min_stat is None else min_stat

        try:
            offense_score = self.__calculate_offense_score(player_stat, max_stat, min_stat)
            play_driving_score = self.__calculate_play_driving_score(player_stat, max_stat, min_stat)
            usage_score = self.__calculate_usage_score(player_stat, max_stat, min_stat)
            special_teams_score = self.__calculate_special_teams_score(player_stat, max_stat, min_stat)
        except Exception as e:
            print(f"[{player_name}] Error occurred while grading forward: {str(e)}")
            return None

        forward_score = \
          0.60 * offense_score + \
          0.40 * special_teams_score
          # 0.25 * play_driving_score + \
          # 0.20 * usage_score + \

        return round(forward_score, 2)

    def __calculate_offense_score(self, player_stat: PlayerStat, max_stat, min_stat):
        norm_points60 = self.__normalize(
            self.__calculate_stat_per60(player_stat, "points"),
            self.__calculate_stat_per60(max_stat, "points"),
            self.__calculate_stat_per60(min_stat, "points"),
        )
        norm_goals60 = self.__normalize(
            self.__calculate_stat_per60(player_stat, "goals"),
            self.__calculate_stat_per60(max_stat, "goals"),
            self.__calculate_stat_per60(min_stat, "goals")
        )
        norm_assists60 = self.__normalize(
            self.__calculate_stat_per60(player_stat, "assists"),
            self.__calculate_stat_per60(max_stat, "assists"),
            self.__calculate_stat_per60(min_stat, "assists")
        )
        # norm_ixg = self.__normalize(player_stat.ixg, max_stat.ixg, min_stat.ixg)
        norm_shot_attempts = self.__normalize(
            self.__calculate_stat_per60(player_stat, "shots"),
            self.__calculate_stat_per60(max_stat, "shots"),
            self.__calculate_stat_per60(min_stat, "shots")
        )
        norm_shooting_pct = self.__normalize(
            player_stat.shotPct,
            max_stat.shotPct,
            min_stat.shotPct
        )
        return (
            0.35 * norm_points60 +
            0.30 * norm_goals60 +
            0.20 * norm_assists60 +
            # 0.15 * norm_ixg +
            0.10 * norm_shot_attempts +
            0.05 * norm_shooting_pct
        )

    def __calculate_play_driving_score(self, player_stat: PlayerStat, max_stat, min_stat):
        # PlayDrivingScore = (
        #         0.40 * norm_xgf_percent +
        #         0.30 * norm_cf_percent +
        #         0.15 * norm_controlled_entries +
        #         0.15 * norm_controlled_exits
        # )
        pass

    def __calculate_usage_score(self, player_stat: PlayerStat, max_stat, min_stat):
        # UsageScore = (
        #         0.35 * norm_toi +
        #         0.25 * norm_quality_of_competition +
        #         0.20 * norm_dz_start_percent(reverse=True) +
        #         0.20 * norm_penalty_diff
        # )
        pass

    def __calculate_special_teams_score(self, player_stat: PlayerStat, max_stat, min_stat):
        norm_pp_points60 = self.__normalize(
            self.__calculate_stat_per60(player_stat, "powerPlayPoints"),
            self.__calculate_stat_per60(max_stat, "powerPlayPoints"),
            self.__calculate_stat_per60(min_stat, "powerPlayPoints")
        )
        # norm_pp_ixg = self.__normalize(player_stat, max_stat, min_stat)
        # norm_pk_toi = self.__normalize(player_stat, max_stat, min_stat)
        norm_pp_toi = self.__normalize(player_stat.powerPlayTimeOnIce, max_stat.powerPlayTimeOnIce, min_stat.powerPlayTimeOnIce)
        # norm_pk_ga60 = self.__normalize(player_stat, max_stat, min_stat)
        special_teams_score = (
                0.60 * norm_pp_points60 +
                # 0.25 * norm_pp_ixg +
                0.40 * norm_pp_toi
                # 0.20 * norm_pk_toi +
                # 0.15 * norm_pk_ga60(reverse=True)
        )
        return special_teams_score


    def __normalize(self, value, max_v, min_v, reverse=False):
        value = value if value else 0
        if max_v == min_v:
            return 0
        if reverse:
            return 100 * (max_v - float(value)) / (max_v - min_v)
        return 100 * (float(value) - min_v) / (max_v - min_v)

    def __calculate_stat_per60(self, stat, stat_name):
        return getattr(stat, stat_name, 0) / int(stat.timeOnIce) * 60

if __name__ == '__main__':
    grader = FantasyForwardGraderService()
    print(grader.grade_forward(8479772, "John Doe"))