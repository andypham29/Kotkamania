import numpy as np

from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.time_converter import TimeConverter
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService


class FantasyPercentileCalculator:

    def __init__(self,
                 internal_player_stat_service=InternalPlayerStatService(uri='../../server/internaldata/db/internal.db'),
                 fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../server/internaldata/db/fantasy.db')):
        self.fantasy_nhl_player_service = fantasy_nhl_player_service
        self.internal_player_stat_service = internal_player_stat_service

    def get_percentile_stats(self, players=[], min_game=None, percentile_shot=None, percentile_hit=None,
                             percentile_block=None, percentile_goal=None, percentile_assist=None, percentile_point=None,
                             percentile_toi=None, percentile_pptoi=None, percentile_evtoi=None):
        current_season = NhlYearConverter.get_current_season()
        stats = [self.get_stat_by_playerId_and_season(player.playerId, current_season) for player in players]
        min_game = 30 if not min_game else min_game

        shot = np.array([stat.shots / stat.games for stat in stats if self.__check_condition(stat, min_game)])
        hit = np.array([stat.hits / stat.games for stat in stats if self.__check_condition(stat, min_game)])
        block = np.array([stat.blocked / stat.games for stat in stats if self.__check_condition(stat, min_game)])
        goal = np.array([stat.goals / stat.games for stat in stats if self.__check_condition(stat, min_game)])
        assist = np.array([stat.assists / stat.games for stat in stats if self.__check_condition(stat, min_game)])
        point = np.array([stat.points / stat.games for stat in stats if self.__check_condition(stat, min_game)])
        toi = np.array([TimeConverter.convert_string_to_total_seconds(stat.timeOnIcePerGame) for stat in stats if
                        self.__check_condition(stat, min_game)])
        pptoi = np.array(
            [TimeConverter.convert_string_to_total_seconds(stat.powerPlayTimeOnIcePerGame) for stat in stats if
             self.__check_condition(stat, min_game)])
        evtoi = np.array(
            [TimeConverter.convert_string_to_total_seconds(stat.evenTimeOnIcePerGame) for stat in stats if
             self.__check_condition(stat, min_game)])

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
            percentile_toi_value = None if percentile_toi is None \
                else np.percentile(toi, self.__get_valid_percentile(percentile_toi))
            percentile_pptoi_value = None if percentile_pptoi is None \
                else np.percentile(pptoi, self.__get_valid_percentile(percentile_pptoi))
            percentile_evtoi_value = None if percentile_evtoi is None \
                else np.percentile(evtoi, self.__get_valid_percentile(percentile_evtoi))

            return PercentileObject(shot=PercentileValue(percentile_shot, percentile_shot_value),
                                    hit=PercentileValue(percentile_hit, percentile_hit_value),
                                    block=PercentileValue(percentile_block, percentile_block_value),
                                    goal=PercentileValue(percentile_goal, percentile_goal_value),
                                    assist=PercentileValue(percentile_assist, percentile_assist_value),
                                    point=PercentileValue(percentile_point, percentile_point_value),
                                    toi=PercentileValue(percentile_toi, percentile_toi_value),
                                    pptoi=PercentileValue(percentile_pptoi, percentile_pptoi_value),
                                    evtoi=PercentileValue(percentile_evtoi, percentile_evtoi_value))
        except Exception as e:
            print(e)
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

    def get_stat_by_playerId_and_season(self, playerId, year):
        # return InternalPlayerStatRepository().get_internal_players_stats_by_playerId_and_seasonId(
        #     playerId, year)
        player_stat = self.internal_player_stat_service.get_internal_players_stats_by_playerId_and_seasonId(
            playerId, year)
        return player_stat


class PercentileObject:
    def __init__(self, shot=None, hit=None, block=None, goal=None, assist=None, point=None, toi=None, pptoi=None,
                 evtoi=None):
        self.shots = shot
        self.hits = hit
        self.blocked = block
        self.goals = goal
        self.assists = assist
        self.points = point
        self.timeOnIcePerGame = toi
        self.powerPlayTimeOnIcePerGame = pptoi
        self.evenTimeOnIcePerGame = evtoi


class PercentileValue:
    def __init__(self, percentile, value):
        self.percentile = percentile
        self.value = value


if __name__ == '__main__':
    f = FantasyPercentileCalculator(
        internal_player_stat_service=InternalPlayerStatService(uri='../../internaldata/db/internal.db'),
        fantasy_nhl_player_service=FantasyNhlPlayerService(uri='../../internaldata/db/internal.db'))
    # players = f.fantasy_nhl_player_service.getAllFantasySkatersWithPositionCodes(["L", "C", "R"])
    players = f.fantasy_nhl_player_service.getAllFantasySkatersWithPositionCodes(["D"])
    filtered_players = []

    fi = open("percentile.txt", "a")
    for i in range(10, 100, 5):
        filtered_player = f.get_percentile_stats(players=players, min_game=None, percentile_shot=i, percentile_hit=i,
                                                 percentile_block=i, percentile_goal=i, percentile_assist=i,
                                                 percentile_point=i, percentile_toi=i, percentile_pptoi=i,
                                                 percentile_evtoi=i)
        fi.write(f"{i}: " + str([f"{k}: {v.value}" for k, v in filtered_player.__dict__.items()]) + "\n")
        filtered_players.append(filtered_player)
