from helper.http_helper import HttpHelper
from server.nhlapi.model.nhl_player import Player


class NHLPlayerService:

    def __init__(self):
        pass

    def get_player_by_id(self, id):
        info_json = HttpHelper.get(self.__get_player_info_url(id))
        player = info_json["people"][0]

        return Player(player["id"],
                      player["fullName"],
                      player["primaryPosition"]["code"],
                      player["currentTeam"]["name"] if player.get("currentTeam") is not None else None,
                      player["primaryNumber"] if player.get("primaryNumber") is not None else None,
                      player["birthDate"] if player.get("birthDate") is not None else None,
                      player["currentAge"] if player.get("currentAge") is not None else None,
                      player["birthCity"] if player.get("birthCity") is not None else None,
                      player["birthCountry"] if player.get("birthCountry") is not None else None,
                      player["height"] if player.get("height") is not None else None,
                      player["weight"] if player.get("weight") is not None else None,
                      player["shootsCatches"] if player.get("shootsCatches") is not None else None
                      )

    @staticmethod
    def __get_player_info_url(id):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}"


