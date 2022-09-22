from script.fantasy.facade.fantasy_player_grade_facade import FantasyPlayerGradeFacade
from script.fantasy.fantasyhelper.excel_helper import ExcelHelper
from script.fantasy.fantasyhelper.fantasy_team_helper import FantasyTeamHelper
from server.commons.fantasybadge.fantasy_player_badge_factory import FantasyPlayerBadgeFactory
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.internaldata.repository.player_repository import InternalPlayerRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.internal_player_stat_service import InternalPlayerStatService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade


class FantasyScript:

    def __init__(self, fantasy_player_helper=FantasyPlayerGradeFacade('../../server/internaldata/db/internal.db'),
                 excel_helper=ExcelHelper(),
                 internal_player_repository=InternalPlayerRepository(),
                 fantasy_nhl_player_service=FantasyNhlPlayerService('../../server/internaldata/db/internal.db')):
        self.fantasy_player_helper = fantasy_player_helper
        self.excel_helper = excel_helper
        self.internal_player_repository = internal_player_repository
        self.fantasy_nhl_player_service = fantasy_nhl_player_service
        self.current_season = NhlYearConverter.get_current_season()

    def save_fantasy_nhl_players(self):
        # self.fantasy_nhl_player_service.initFantasySkaterTable()

        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            # self.fantasy_nhl_player_service.removeTeamIdFromAllFantasySkates()
            self.fantasy_nhl_player_service.saveFantasySkater(player)

        print("done")

    def save_nhl_players_stats_by_year(self):
        # self.fantasy_nhl_player_service.initFantasySkaterTable()

        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            if player.positionCode != "G":
                NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(player.playerId, [self.current_season])
                # InternalPlayerStatRepository().save_internal_player_stats(p)

        print("done")

    def save_player_grade_for_forwards_to_excel(self):
        fantasy_players = self.fantasy_player_helper.get_all_fantasy_forward_from_internal_db()
        excel_helper = ExcelHelper("new_fantasy.xlsx")
        excel_helper.write_players_to_excel(sheet='all', players=fantasy_players)
        excel_helper.close()

    def save_player_grade_for_all_players_in_internal_db(self):
        fantasy_players = self.fantasy_player_helper.get_all_fantasy_player_from_internal_db()
        # fantasy_players = self.fantasy_player_helper.get_fantasy_goalie()
        for fantasy_player in fantasy_players:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_player.id,
                                                                                     fantasy_player.score)

    def save_player_badge_for_all_players_in_internal_db(self):
        fantasy_players = self.fantasy_nhl_player_service.getAllFantasySkatersWithPositionCodesWithStats(["L", "C", "R", "D"])
        badge_factory = FantasyPlayerBadgeFactory()
        player_stat_service = InternalPlayerStatService("../../server/internaldata/db/internal.db")
        # fantasy_players = self.fantasy_player_helper.get_fantasy_goalie()
        for fantasy_player in fantasy_players:
            player_stat = player_stat_service\
                .get_internal_players_stats_by_playerId_and_seasonId(fantasy_player.playerId, self.current_season)
            if not player_stat:
                continue
            badge = badge_factory.get_badge_for_skater(player_stat, fantasy_player.positionCode)
            print(fantasy_player.skaterFullName, ": ", badge.__dict__, player_stat.__dict__)
            self.fantasy_nhl_player_service.updateFantasyBadgeForFantasySkaterByPlayerId(badge, fantasy_player.playerId)

    def process_forward(self):
        fantasy_skaters = self.fantasy_player_helper.get_fantasy_forward(amount=10)
        fantasy_skaters.sort(key=lambda x: x.score, reverse=True)
        # for fantasy_skater in fantasy_skaters:
        #     self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_skater.id,
        #                                                                              fantasy_skater.score)

        self.excel_helper.write_players_to_excel(sheet='forward', players=fantasy_skaters)

        return self

    def process_defensemen(self):
        fantasy_defensemen = self.fantasy_player_helper.get_fantasy_defensemen(amount=20)
        fantasy_defensemen.sort(key=lambda x: x.score, reverse=True)
        # for fantasy_defenseman in fantasy_defensemen:
        #     self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_defenseman.id,
        #                                                                              fantasy_defenseman.score)

        self.excel_helper.write_players_to_excel(sheet='defense', players=fantasy_defensemen)
        return self

    def process_goalies(self):
        fantasy_goalies = self.fantasy_player_helper.get_fantasy_goalie(amount=100)
        fantasy_goalies.sort(key=lambda x: x.score, reverse=True)
        # for fantasy_goalie in fantasy_goalies:
        #     self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_goalie.id,
        #                                                                              fantasy_goalie.score)

        self.excel_helper.write_players_to_excel(sheet='goalie', players=fantasy_goalies)
        return self

    def get_fantasy_grade_by_id(self, id):
        print(self.fantasy_player_helper.get_fantasy_grade_by_id(id).__dict__)

    def close(self):
        print("closing excel")
        self.excel_helper.close()


if __name__ == '__main__':
    # FantasyScript().save_nhl_players_stats_by_year()
    # FantasyScript().save_fantasy_nhl_players()
    # FantasyScript().save_player_stats_to_internal_db()
    # InternalPlayerRepository().create_database()
    # FantasyNhlPlayerDao().initFantasySkaterTable()

    # FantasyScript() \
    #     .process_defensemen() \
    #     .process_forward() \
    #     .process_goalies() \
    #     .close()

    # FantasyScript().get_fantasy_grade_by_id(8476885)
    FantasyScript().save_fantasy_nhl_players()
    # FantasyScript().save_player_grade_for_all_players_in_internal_db()
    # FantasyScript().save_player_badge_for_all_players_in_internal_db()
    # FantasyScript().save_player_grade_for_forwards_to_excel()

    # stats = InternalPlayerStatRepository().get_internal_player_stats_by_playerId(8470187)
    # for stat in stats:
    #     print(stat.__dict__)
