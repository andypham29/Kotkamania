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
                      player["primaryNumber"],
                      player["birthDate"],
                      player["currentAge"] if player.get("currentAge") is not None else None,
                      player["birthCity"],
                      player["birthCountry"],
                      player["height"],
                      player["weight"],
                      player["shootsCatches"]
                      )

    @staticmethod
    def __get_player_info_url(id):
        return f"https://statsapi.web.nhl.com/api/v1/people/{id}"


