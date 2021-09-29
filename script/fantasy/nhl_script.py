from script.fantasy.facade.fantasy_player_grade_facade import FantasyPlayerGradeFacade
from script.fantasy.fantasyhelper.excel_helper import ExcelHelper
from script.fantasy.fantasyhelper.fantasy_team_helper import FantasyTeamHelper
from server.internaldata.repository.player_repository import InternalPlayerRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService


class FantasyScript:

    def __init__(self, fantasy_player_helper=FantasyPlayerGradeFacade('../../server/internaldata/db/fantasy.db'),
                 excel_helper=ExcelHelper(),
                 internal_player_repository=InternalPlayerRepository(),
                 fantasy_nhl_player_service=FantasyNhlPlayerService('../../server/internaldata/db/fantasy.db')):
        self.fantasy_player_helper = fantasy_player_helper
        self.excel_helper = excel_helper
        self.internal_player_repository = internal_player_repository
        self.fantasy_nhl_player_service = fantasy_nhl_player_service

    def save_fantasy_nhl_players(self):
        # self.fantasy_nhl_player_service.initFantasySkaterTable()

        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            self.fantasy_nhl_player_service.saveFantasySkater(player)

        print("done")

    def save_player_grade_for_forwards_to_excel(self):
        fantasy_players = self.fantasy_player_helper.get_all_fantasy_forward_from_internal_db()
        excel_helper = ExcelHelper("new_fantasy.xlsx")
        excel_helper.write_players_to_excel(sheet='all', players=fantasy_players)
        excel_helper.close()

    def save_player_grade_for_all_players_in_internal_db(self):
        fantasy_players = self.fantasy_player_helper.get_all_fantasy_player_from_internal_db()
        for fantasy_player in fantasy_players:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_player.id,
                                                                                     fantasy_player.score)

    def process_forward(self):
        fantasy_skaters = self.fantasy_player_helper.get_fantasy_forward(amount=30)
        fantasy_skaters.sort(key=lambda x: x.score, reverse=True)
        for fantasy_skater in fantasy_skaters:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_skater.id,
                                                                                     fantasy_skater.score)

        self.excel_helper.write_players_to_excel(sheet='forward', players=fantasy_skaters)

        return self

    def process_defensemen(self):
        fantasy_defensemen = self.fantasy_player_helper.get_fantasy_defensemen(amount=1000)
        fantasy_defensemen.sort(key=lambda x: x.score, reverse=True)
        for fantasy_defenseman in fantasy_defensemen:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_defenseman.id,
                                                                                     fantasy_defenseman.score)

        self.excel_helper.write_players_to_excel(sheet='defense', players=fantasy_defensemen)
        return self

    def process_goalies(self):
        fantasy_goalies = self.fantasy_player_helper.get_fantasy_goalie(amount=100)
        fantasy_goalies.sort(key=lambda x: x.score, reverse=True)
        for fantasy_goalie in fantasy_goalies:
            self.fantasy_nhl_player_service.updateFantasyGradeForFantasySkaterWithId(fantasy_goalie.id,
                                                                                     fantasy_goalie.score)

        self.excel_helper.write_players_to_excel(sheet='goalie', players=fantasy_goalies)
        return self

    def close(self):
        print("closing excel")
        self.excel_helper.close()


if __name__ == '__main__':
    # FantasyScript().save_fantasy_nhl_players()
    # FantasyScript().save_player_stats_to_internal_db()
    # # InternalPlayerRepository().create_database()

    # FantasyScript() \
    #     .process_defensemen() \
    #     .process_forward() \
    #     .process_goalies() \
    #     .close()

    FantasyScript().save_player_grade_for_all_players_in_internal_db()
    # FantasyScript().save_player_grade_for_forwards_to_excel()

    # stats = InternalPlayerStatRepository().get_internal_player_stats_by_playerId(8470187)
    # for stat in stats:
    #     print(stat.__dict__)
