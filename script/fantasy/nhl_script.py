import os
import asyncio

from script.fantasy.facade.fantasy_player_grade_facade import FantasyPlayerGradeFacade
from script.fantasy.fantasyhelper.excel_helper import ExcelHelper
from script.fantasy.fantasyhelper.fantasy_team_helper import FantasyTeamHelper
from server.commons.fantasybadge.fantasy_player_badge_factory import FantasyPlayerBadgeFactory
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.internaldata.repository.player_stat_repository import InternalPlayerStatRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.service.nhl_statsmisc_service import NHLStatMiscService


class FantasyScript:

    def __init__(self, fantasy_player_helper=None, excel_helper=ExcelHelper(),
                 fantasy_nhl_player_service=None):
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../server/internaldata/db/internal.db'))
        if fantasy_player_helper is None:
            fantasy_player_helper = FantasyPlayerGradeFacade(uri=self.db_path)
        if fantasy_nhl_player_service is None:
            fantasy_nhl_player_service = FantasyNhlPlayerService(uri=self.db_path)
        self.fantasy_player_helper = fantasy_player_helper
        self.excel_helper = excel_helper
        self.fantasy_nhl_player_service = fantasy_nhl_player_service
        self.current_season = NhlYearConverter.get_current_season()

    def save_fantasy_nhl_players(self):
        self.fantasy_nhl_player_service.initFantasySkaterTable()

        # nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            # self.fantasy_nhl_player_service.removeTeamIdFromAllFantasySkates()
            self.fantasy_nhl_player_service.saveFantasySkater(player)

        print("done")

        return self

    def save_player_grade_for_forwards_to_excel(self):
        fantasy_players = self.fantasy_player_helper.get_all_fantasy_forward_from_internal_db()
        excel_helper = ExcelHelper("new_fantasy.xlsx")
        excel_helper.write_players_to_excel(sheet='all', players=fantasy_players)
        excel_helper.close()

        return self

    async def save_player_grade_for_all_players_in_internal_db(self):
        fantasy_players = self.fantasy_player_helper.get_all_fantasy_player_from_internal_db()
        # fantasy_players = self.fantasy_player_helper.get_fantasy_goalie()
        for fantasy_player in fantasy_players:
            await asyncio.run(self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_player.id,
                                                                                     fantasy_player.score))

        return self

    def save_player_badge_for_all_players_in_internal_db(self):
        fantasy_players = self.fantasy_nhl_player_service.getAllFantasySkatersWithPositionCodesWithStats(["L", "C", "R", "D"])
        badge_factory = FantasyPlayerBadgeFactory()
        player_stat_service = InternalPlayerStatService(self.db_path)
        # fantasy_players = self.fantasy_player_helper.get_fantasy_goalie()
        for fantasy_player in fantasy_players:
            player_stat = player_stat_service\
                .get_internal_players_stats_by_playerId_and_seasonId(fantasy_player.playerId, self.current_season)
            if not player_stat:
                continue
            badge = badge_factory.get_badge_for_skater(player_stat, fantasy_player.positionCode)
            print(fantasy_player.skaterFullName, ": ", badge.__dict__, player_stat.__dict__)
            self.fantasy_nhl_player_service.updateFantasyBadgeForFantasySkaterByPlayerId(badge, fantasy_player.playerId)

        return self

    def process_forward(self):
        fantasy_skaters = self.fantasy_player_helper.update_fantasy_grade_forward()
        fantasy_skaters.sort(key=lambda x: x.score, reverse=True)
        # self.fantasy_nhl_player_service.bulkUpdateFantasyGradeForFantasySkaterWithId(players=fantasy_skaters)

        print("start updating in sqlite")
        for fantasy_skater in fantasy_skaters:
            FantasyNhlPlayerService(self.db_path).updateFantasyGradeForFantasySkaterWithId(fantasy_skater.id,
                                                                                     fantasy_skater.score)

        # self.excel_helper.write_players_to_excel(sheet='forward', players=fantasy_skaters)

        return self

    def process_defensemen(self):
        fantasy_defensemen = self.fantasy_player_helper.get_fantasy_defensemen()
        fantasy_defensemen.sort(key=lambda x: x.score, reverse=True)
        # self.fantasy_nhl_player_service.bulkUpdateFantasyGradeForFantasySkaterWithId(players=fantasy_defensemen)
        for fantasy_defenseman in fantasy_defensemen:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_defenseman.id,
                                                                                     fantasy_defenseman.score)

        # self.excel_helper.write_players_to_excel(sheet='defense', players=fantasy_defensemen)
        return self

    def process_goalies(self):
        fantasy_goalies = self.fantasy_player_helper.get_fantasy_goalie()
        # fantasy_goalies.sort(key=lambda x: x.score, reverse=True)
        for fantasy_goalie in fantasy_goalies:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_goalie.id,
                                                                                     fantasy_goalie.score)

        # self.excel_helper.write_players_to_excel(sheet='goalie', players=fantasy_goalies)
        return self

    def get_fantasy_grade_by_id(self, id):
        print(self.fantasy_player_helper.get_fantasy_grade_by_id(id).__dict__)

        return self

    def close(self):
        print("closing excel")
        self.excel_helper.close()

    def save_stat(self):
        season = NhlYearConverter.get_current_season()
        InternalPlayerStatRepository().bulk_save_internal_players_stats_only(NHLStatMiscService().get_all_player_stats(season))

        print("done")

        return self

    def cleanup(self):
        self.fantasy_nhl_player_service.removeTeamIdFromAllFantasySkates()
        self.save_fantasy_nhl_players()
        self.fantasy_nhl_player_service.deleteAllFantasySkatersWithNoTeam()

        return self

class FantasyScriptHandler:

    def __init__(self):
        self.fantasy_script = FantasyScript()

    def process_new_season(self):
        self.fantasy_script\
            .save_fantasy_nhl_players()\
            .process_forward() \
            .process_defensemen() \
            .save_stat()




if __name__ == '__main__':
    # FantasyScript().save_stat()
    # InternalPlayerRepository().create_database()
    # FantasyNhlPlayerDao().initFantasySkaterTable()

    # FantasyScript().get_fantasy_grade_by_id(8477934)
    # FantasyScript().get_fantasy_grade_by_id(8478402)

    # FantasyScript().cleanup()
    # FantasyScript().save_fantasy_nhl_players()
    FantasyScript() \
        .process_forward() \
        .close()

    # .process_defensemen() \
        # .process_goalies()\

    # FantasyScript().get_fantasy_grade_by_id(8476885)
    # FantasyScript().save_player_grade_for_all_players_in_internal_db()
    # FantasyScript().save_player_badge_for_all_players_in_internal_db()
    # FantasyScript().save_player_grade_for_forwards_to_excel()

    # stats = InternalPlayerStatRepository().get_internal_player_stats_by_playerId(8470187)
    # for stat in stats:
    #     print(stat.__dict__)
