from datetime import datetime

from server.admin.repository.intenal_log_dao import NhlPlayerStatLog
from server.admin.service.internal_log_service import InternalLogService
from server.commons.fantasygrade.fantasy_player_streak_index_calculator import FantasyPlayerStreakIndexCalculator
from server.commons.helper.calendar_helper import CalendarHelper
from server.commons.helper.csv_reader import CSVReader
from server.commons.helper.fantasy_team_helper import FantasyTeamHelper
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.internaldata.model.fantasy_player_streak_index import FantasyPlayerStreakIndex
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.fantasy_player_streak_index_service import FantasyPlayerStreakIndexService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService


class AdminFacade:

    def __init__(self):
        self.csv = CSVReader("server/commons/fantasygrade/percentile.csv")
        self.sogs_percentiles = self.csv.get_col_by_colname("shots")
        self.hits_percentiles = self.csv.get_col_by_colname("hits")
        self.blk_percentiles = self.csv.get_col_by_colname("blocked")
        pass

    def apply(self, offset):
        offset = int(offset)
        today_date = datetime.now().strftime("%Y-%m-%d")
        log = InternalLogService().getNhlPlayerStatLogByDate(today_date)
        timeExecuted = log.timeExecuted if log is not None else 0
        if offset == 0:
            FantasyPlayerStreakIndexService().deleteAllFantasySkaterStreak()
        if True:
            # if not log or timeExecuted <= 10:

            index_list = []
            players = FantasyNhlPlayerService().getAllFantasySkatersWithPositionCodesWithStats(['C', 'L', 'R', 'D'],
                                                                                               offset)
            print(len(players))
            season = NhlYearConverter.get_current_season()
            for player in players:
                index = self.__get_gamelogs_index(player.playerId, player.skaterFullName, player.positionCode, season)
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

    def execute(self):
        index_list = []
        players = FantasyNhlPlayerService().getAllFantasySkatersWithPositionCodesWithStats(['C', 'L', 'R', 'D'])
        print(len(players))
        season = NhlYearConverter.get_current_season()
        for player in players:
            index = self.__get_gamelogs_index(player.playerId, player.skaterFullName, player.positionCode, season)
            print(index.__dict__)
            FantasyPlayerStreakIndexService().initFantasyPlayerStreakIndexTable()
            FantasyPlayerStreakIndexService().saveOrUpdateFantasyPlayerStreakIndex(index)
            index_list.append(index)

    def __get_gamelogs_index(self, playerId, name, position, season):
        gamelogs = self.get_player_gamelogs_by_id_and_season(playerId, season)
        pts = FantasyPlayerStreakIndexCalculator().get_point_index_for_last_5(gamelogs)
        toi = FantasyPlayerStreakIndexCalculator().get_toi_index_for_last_5(gamelogs)
        pptoi = FantasyPlayerStreakIndexCalculator().get_pptoi_index_for_last_5(gamelogs)
        gper60 = FantasyPlayerStreakIndexCalculator().get_gper60_index_for_last_10(gamelogs)
        pper60 = FantasyPlayerStreakIndexCalculator().get_ptsper60_index_for_last_10(gamelogs)

        peripherals = FantasyPlayerStreakIndexCalculator().get_peripheral_index_for_last_5(
            sogs_percentiles=self.sogs_percentiles,
            hits_percentiles=self.hits_percentiles,
            blocked_percentiles=self.blk_percentiles,
            gamelogs=gamelogs)
        date = CalendarHelper().get_current_day()

        print("peripherals:" + str(peripherals))
        index = (pts * 10 + toi + pptoi * 5 + gper60 + pper60 + peripherals)
        return FantasyPlayerStreakIndex(playerId, name, position, pts, toi, pptoi, round(index, 3), date)

    def __update_fantasy_players_from_nhl_rosters(self):
        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            FantasyNhlPlayerService().saveFantasySkater(player)

    def __save_and_return_players_stats_by_year(self, playerId, position, season):
        stat = NHLPlayerStatService().get_player_stat_by_playerId_and_seasons(playerId, [season])
        if position != 'G':
            InternalPlayerStatService().get_internal_players_stats_by_playerId_and_seasonId(playerId, season)
        return stat

    def get_player_gamelogs_by_id_and_season(self, playerId, season):
        return [data.stat for data in
                NHLPlayerStatService().get_player_gamelogs_by_playerId_and_season(playerId, season)]


if __name__ == '__main__':
    AdminFacade().apply()
