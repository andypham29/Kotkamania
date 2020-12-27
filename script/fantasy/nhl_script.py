from script.fantasy.fantasyhelper.excel_helper import ExcelHelper
from script.fantasy.fantasyhelper.fantasy_player_helper import FantasyPlayerHelper
from script.fantasy.fantasyhelper.fantasy_team_helper import FantasyTeamHelper
from server.internaldata.repository.player_repository import InternalPlayerRepository
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService


class FantasyScript:

    def __init__(self, fantasy_player_helper=FantasyPlayerHelper(),
                 excel_helper=ExcelHelper(),
                 internal_player_repository=InternalPlayerRepository()):
        self.fantasy_player_helper = fantasy_player_helper
        self.excel_helper = excel_helper
        self.internal_player_repository = internal_player_repository

    def save_fantasy_nhl_players(self):
        fantasy_nhl_player_service = FantasyNhlPlayerService()
        fantasy_nhl_player_service.initFantasySkaterTable()

        nhl_roster_players = FantasyTeamHelper().get_all_players_in_teams()
        for player in nhl_roster_players:
            print(player)
            fantasy_nhl_player_service.saveFantasySkater(player)

    def save_player_stats_to_internal_db(self):
        self.fantasy_player_helper.save_player_stats()

    def process_forward(self):
        fantasy_skaters = self.fantasy_player_helper.get_fantasy_forward(amount=250)
        fantasy_skaters.sort(key=lambda x: x.score, reverse=True)
        self.excel_helper.write_players_to_excel(sheet='forward', players=fantasy_skaters)

        return self

    def process_defensemen(self):
        fantasy_defensemen = self.fantasy_player_helper.get_fantasy_defensemen(amount=150)
        fantasy_defensemen.sort(key=lambda x: x.score, reverse=True)
        self.excel_helper.write_players_to_excel(sheet='defense', players=fantasy_defensemen)
        return self

    def close(self):
        print("done")
        self.excel_helper.close()


if __name__ == '__main__':
    FantasyScript().save_fantasy_nhl_players()
    # FantasyScript().save_player_stats_to_internal_db()
    # # InternalPlayerRepository().create_database()

    # FantasyScript() \
    #     .process_forward() \
    #     .process_defensemen() \
    #     .close()

    # stats = InternalPlayerStatRepository().get_internal_player_stats_by_playerId(8470187)
    # for stat in stats:
    #     print(stat.__dict__)
