from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_player import Player
import json


class NHLPlayerService:

    def __init__(self):
        pass

    def get_player_by_id(self, id):
        player = HttpHelper.get(self.__get_player_info_url(id))

        return Player(player.get("playerId", None),
                      player.get("fullName", None),
                      player.get("position", None),
                      player.get("currentTeamId", None),
                      player.get("currentTeamAbbrev", None),
                      player.get("sweaterNumber", None),
                      player.get("birthDate", None),
                      player.get("currentAge", None),
                      player.get("birthCity", None),
                      player.get("birthCountry", None),
                      player.get("height", None),
                      player.get("weight", None),
                      player.get("shootsCatches", None),
                      )

    @staticmethod
    def __get_player_info_url(id):
        return f"https://api-web.nhle.com/v1/player/{id}/landing"
