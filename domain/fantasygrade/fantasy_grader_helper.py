from dataclasses import asdict

from infra.spi.sqlite.playerstat.model.nhl_player_stat import PlayerStat
from domain.playerstat.nhl_player_stat_cache_service import NhlPlayerStatCacheService
from server.commons.helper.nhl_season_converter import NhlYearConverter


class FantasyGraderHelper:

    def __init__(self):
        self.nhl_player_stat_service = NhlPlayerStatCacheService()
        pass

    def get_max_stat(self, season_id):
        return self.nhl_player_stat_service.get_all_max_stat(season_id)

    def get_min_stat(self, season_id):
        return self.nhl_player_stat_service.get_all_min_stat(season_id)

    def get_average_stat(self, season_id):
        stats_list = self.nhl_player_stat_service.get_all_stats(season_id)
        n = len(stats_list)
        dicts = [asdict(s) for s in stats_list]

        summed = {}
        for d in dicts:
            for key, value in d.items():
                summed[key] = summed.get(key, 0) + (value or 0)

        averaged = {key: value / n for key, value in summed.items()}

        return PlayerStat(**averaged)

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


    def normalize(self, value, max_v, min_v, reverse=False):
        value = value if value else 0
        if max_v == min_v:
            return 0
        if reverse:
            return 100 * (max_v - float(value)) / (max_v - min_v)
        return 100 * (float(value) - min_v) / (max_v - min_v)

    def calculate_stat_per60(self, stat, stat_name):
        return getattr(stat, stat_name, 0) / int(stat.timeOnIce) * 60

    def bayesian_shrinkage(value, games, max_v, min_v, prior_games=10):
        # Prior expectation based on league average
        median = (max_v - min_v) / 2
        prior_points = median * prior_games

        # Avoid division by zero
        if games == 0:
            return median

        # Shrink toward league average
        return (value + prior_points) / (games + prior_games)


if __name__ == '__main__':
    helper = FantasyGraderHelper()
    season_id = NhlYearConverter.get_current_season()
    max_stat = helper.get_max_stat(season_id)
    min_stat = helper.get_min_stat(season_id)
    average_stat = helper.get_average_stat(season_id)
    print("Max stat:", max_stat)
    print("Min stat:", min_stat)
    print("Average stat:", average_stat)