import numpy as np

from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService


class FantasyPercentileCalculator:

    def __init__(self,
                 internal_player_stat_service=InternalPlayerStatService(uri='../../server/internaldata/db/internal.db'),
                 fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../server/internaldata/db/fantasy.db')):
        self.fantasy_nhl_player_service = fantasy_nhl_player_service
        self.internal_player_stat_service = internal_player_stat_service

    def get_percentile_stats(self, players=[], min_game=None, percentile_shot=None, percentile_hit=None,
                             percentile_block=None, percentile_goal=None,
                             percentile_assist=None, percentile_point=None):
        stats = [self.get_stat_by_playerId_and_season(player.playerId, "20192020") for player in players]
        min_game = 30 if not min_game else min_game

        shot = np.array([stat.shots / stat.games * 82 for stat in stats if self.__check_condition(stat, min_game)])
        hit = np.array([stat.hits / stat.games * 82 for stat in stats if self.__check_condition(stat, min_game)])
        block = np.array([stat.blocked / stat.games * 82 for stat in stats if self.__check_condition(stat, min_game)])
        goal = np.array([stat.goals / stat.games * 82 for stat in stats if self.__check_condition(stat, min_game)])
        assist = np.array([stat.assists / stat.games * 82 for stat in stats if self.__check_condition(stat, min_game)])
        point = np.array([stat.points / stat.games * 82 for stat in stats if self.__check_condition(stat, min_game)])

        try:

            percentile_shot_value = None if percentile_shot is None \
                else np.percentile(shot, self.__get_valid_percentile(percentile_shot))
            percentile_hit_value = None if percentile_hit is None \
                else np.percentile(hit, self.__get_valid_percentile(percentile_hit))
            percentile_block_value = None if percentile_block is None \
                else np.percentile(block, self.__get_valid_percentile(percentile_block))
            percentile_goal_value = None if percentile_goal is None \
                else np.percentile(goal, self.__get_valid_percentile(percentile_goal))
            percentile_assist_value = None if percentile_assist is None \
                else np.percentile(assist, self.__get_valid_percentile(percentile_assist))
            percentile_point_value = None if percentile_point is None \
                else np.percentile(point, self.__get_valid_percentile(percentile_point))

            return PercentileObject(shot=PercentileValue(percentile_shot, percentile_shot_value),
                                    hit=PercentileValue(percentile_hit, percentile_hit_value),
                                    block=PercentileValue(percentile_block, percentile_block_value),
                                    goal=PercentileValue(percentile_goal, percentile_goal_value),
                                    assist=PercentileValue(percentile_assist, percentile_assist_value),
                                    point=PercentileValue(percentile_point, percentile_point_value))
        except:
            return None

    @staticmethod
    def __get_valid_percentile(percentile):
        try:
            percentile = int(percentile)
            if 0 < percentile < 100:
                return percentile
            raise Exception("Percentile out of bound")
        except Exception as e:
            print("FantasyPercentileCalculator: ", e)
            return 0

    @staticmethod
    def __check_condition(stat, min_game):
        if not stat:
            return False

        return stat.games and stat.games > min_game

    def get_all_players_stats(self, players):
        # forwards = self.fantasy_nhl_player_service.getAllFantasySkatersWithPositionCodes(positions)
        # print(forwards)
        return [self.get_stat_by_playerId_and_season(player.playerId, "20192020") for player in players]

    def get_stat_by_playerId_and_season(self, playerId, year):
        # return InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
        #     playerId, year)
        player_stat = self.internal_player_stat_service.get_internal_players_stats_by_playerId_and_seasonId(
            playerId, year)
        return player_stat


class PercentileObject:
    def __init__(self, shot=None, hit=None, block=None, goal=None, assist=None, point=None):
        self.shots = shot
        self.hits = hit
        self.blocked = block
        self.goals = goal
        self.assists = assist
        self.points = point


class PercentileValue:
    def __init__(self, percentile, value):
        self.percentile = percentile
        self.value = value


if __name__ == '__main__':
    FantasyPercentileCalculator().get_percentile_stats(min_game=41, percentile_shot=50, percentile_hit=50,
                                                       percentile_block=50, percentile_goal=50, percentile_assist=50,
                                                       percentile_point=50)
