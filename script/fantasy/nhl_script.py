from script.fantasy.fantasyhelper.excel_helper import ExcelHelper
from script.fantasy.fantasyhelper.fantasy_player_helper import FantasyPlayerHelper
from server.internaldata.repository.player_repository import InternalPlayerRepository


class FantasyScript:

    def __init__(self, fantasy_player_helper=FantasyPlayerHelper(),
                 excel_helper=ExcelHelper(),
                 internal_player_repository=InternalPlayerRepository()):
        self.fantasy_player_helper = fantasy_player_helper
        self.excel_helper = excel_helper
        self.internal_player_repository = internal_player_repository

    def process_forward(self):
        fantasy_skaters = self.fantasy_player_helper.get_forward(amount=5)
        fantasy_skaters.sort(key=lambda x: x.score, reverse=True)
        self.excel_helper.write_players_to_excel(sheet='forward', players=fantasy_skaters)

        return self

    def process_defensemen(self):
        fantasy_defensemen = self.fantasy_player_helper.get_defensemen(amount=5)
        fantasy_defensemen.sort(key=lambda x: x.score, reverse=True)
        self.excel_helper.write_players_to_excel(sheet='defense', players=fantasy_defensemen)
        return self

    def close(self):
        print("done")
        self.excel_helper.close()


if __name__ == '__main__':
    InternalPlayerRepository().create_database()
    FantasyScript() \
        .process_forward() \
        .process_defensemen() \
        .close()
