from dataclasses import dataclass

from helper.http_helper import HttpHelper
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.nhl_team_converter import NhlTeamConverter


class NhlTeamRosterProvider:

    def __init__(self):
        pass

    def get_roster_player_ids(self, team_id, season_id=None):
        season_id = NhlYearConverter.get_current_season() if season_id is None else season_id
        team_id_converted = NhlTeamConverter.get_teamId_by_abr(team_id)

        json = HttpHelper.get(f'https://api-web.nhle.com/v1/roster/{team_id_converted}/{season_id}')

        forwards = json.get("forwards", None)
        defenses = json.get("defenses", None)
        goalies = json.get("goalies", None)

        return [player["id"] for player in forwards + defenses + goalies]

    def get_roster_player_ids_forward(self, team_id, season_id=None):
        season_id = NhlYearConverter.get_current_season() if season_id is None else season_id
        team_id_converted = NhlTeamConverter.get_teamId_by_abr(team_id)

        json = HttpHelper.get(f'https://api-web.nhle.com/v1/roster/{team_id_converted}/{season_id}')

        forwards = json.get("forwards", None)

        return [player["id"] for player in forwards]

    def get_roster_player_ids_defense(self, team_id, season_id=None):
        season_id = NhlYearConverter.get_current_season() if season_id is None else season_id
        team_id_converted = NhlTeamConverter.get_teamId_by_abr(team_id)

        json = HttpHelper.get(f'https://api-web.nhle.com/v1/roster/{team_id_converted}/{season_id}')

        defenses = json.get("defense", None)

        return [NhlTeamRosterPlayer(
            id=player["id"],
            fullname=self.__build_skater_fullname(player))
            for player in defenses]

    def __build_skater_fullname(self, player):
        return f"{player['firstName'].get("default")} {player['lastName'].get("default")}"


@dataclass
class NhlTeamRosterPlayer:
    id: int
    fullname: str
