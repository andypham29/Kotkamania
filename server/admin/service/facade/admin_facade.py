from datetime import datetime

from server.admin.repository.intenal_log_dao import NhlPlayerStatLog
from server.admin.service.internal_log_service import InternalLogService
from server.commons.fantasygrade.fantasy_player_streak_index_calculator import FantasyPlayerStreakIndexCalculator
from server.commons.helper.calendar_helper import CalendarHelper
from server.commons.helper.fantasy_team_helper import FantasyTeamHelper
from server.internaldata.model.fantasy_player_streak_index import FantasyPlayerStreakIndex
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.fantasy_player_streak_index_service import FantasyPlayerStreakIndexService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService


class AdminFacade:

    def __init__(self):
        pass

    def apply(self, offset):
        offset = int(offset)
        today_date = datetime.now().strftime("%Y-%m-%d")
        log = InternalLogService().getNhlPlayerStatLogByDate(today_date)
        timeExecuted = log.timeExecuted if log is not None else 0
        if not log or timeExecuted <= 10:

            index_list = []
            players = FantasyNhlPlayerService().getAllFantasySkatersWithPositionCodes(['C', 'L', 'R', 'D'], offset)
            print(len(players))
            for player in players:
                index = self.__get_gamelogs_index(player.playerId, player.skaterFullName, player.positionCode)
                print(index.__dict__)
                FantasyPlayerStreakIndexService().initFantasyPlayerStreakIndexTable()
                FantasyPlayerStreakIndexService().saveOrUpdateFantasyPlayerStreakIndex(index)
                index_list.append(index)

            InternalLogService().initNhlPlayerStatLogTable()

            if not log:
                log = NhlPlayerStatLog(today_date, "test", timeExecuted)
                InternalLogService().saveNhlPlayerStatLog(log)
            else:
                log.timeExecuted += 1
                InternalLogService().updateNhlPlayerStatLog(log)

            return sorted(index_list, key=lambda x: x.index, reverse=True)
        return []
        # print(InternalLogService().getNhlPlayerStatLogByDate(today_date))

    def __get_gamelogs_index(self, playerId, name, position):
        gamelogs = self.get_player_gamelogs_by_id_and_season(playerId, "20212022")
        pts = FantasyPlayerStreakIndexCalculator().get_point_index_for_last_5(gamelogs)
        toi = FantasyPlayerStreakIndexCalculator().get_toi_index_for_last_5(gamelogs)
        pptoi = FantasyPlayerStreakIndexCalculator().get_pptoi_index_for_last_5(gamelogs)
        date = CalendarHelper().get_current_day()

        index = (pts * 3 + toi + pptoi) / 5 / 3
        return FantasyPlayerStreakIndex(playerId, name, position, pts, toi, pptoi, round(index, 3), date)

    def __update_fantasy_players_from_nhl_rosters(self):
        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            FantasyNhlPlayerService().saveFantasySkater(player)

    def __save_and_return_players_stats_by_year(self, playerId, position, season="20212022"):
        stat = NHLPlayerStatService().get_player_stat_by_playerId_and_seasons(playerId, [season])
        if position != 'G':
            InternalPlayerStatService().get_internal_players_stats_by_playerId_and_seasonId(playerId, season)
        return stat

    def get_player_gamelogs_by_id_and_season(self, playerId, season="20212022"):
        return [data.stat for data in
                NHLPlayerStatService().get_player_gamelogs_by_playerId_and_season(playerId, season)]


if __name__ == '__main__':
    AdminFacade().apply()
