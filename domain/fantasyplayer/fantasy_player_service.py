from typing import List

from domain.fantasyplayer.model.fantasy_nhl_player import FantasyPlayerUpdateQuery
from infra.spi.sqlite.fantasyplayer.fantasy_player_repository import FantasyPlayerRepository
from server.commons.fantasyplayer.model.fantasy_player import FantasyPlayer


class FantasyPlayerService:

    def __init__(self):
        self.fantasy_player_repository = FantasyPlayerRepository()

    def create_fantasy_player(self, fantasy_player):
        return self.fantasy_player_repository.saveFantasySkater(fantasy_player)

    def get_fantasy_player(self, player_id):
        return self.fantasy_player_repository.getFantasySkaterById(player_id)

    def update_fantasy_players(self, players: List[FantasyPlayerUpdateQuery]):
        return self.fantasy_player_repository.bulkUpdateFantasyGrade(players)

    def delete_fantasy_player(self, player_id):
        return self.fantasy_player_repository.deleteFantasySkaterById(player_id)

    def delete_all(self):
        return self.fantasy_player_repository.deleteAllFantasySkater()
