from dataclasses import dataclass, fields, is_dataclass
from typing import Optional

from helper.http_helper import HttpHelper
from infra.spi.nhlapi.model.nhl_roster_player import PlayerInfo, LocalizedString
from server.commons.helper.nhl_season_converter import NhlYearConverter
from server.commons.helper.nhl_team_converter import NhlTeamConverter


class NhlTeamRosterProvider:

    def __init__(self):
        pass

    def get_roster_all_player_infos(self, team_id, season_id=None):
        season_id = NhlYearConverter.get_current_season() if season_id is None else season_id
        team_id_converted = NhlTeamConverter.get_abbreviation_by_teamId(team_id)

        json = HttpHelper.get(f'https://api-web.nhle.com/v1/roster/{team_id_converted}/{season_id}')

        forwards = json.get("forwards", [])
        defenses = json.get("defensemen", [])
        goalies = json.get("goalies", [])

        return [self._to_model(player) for player in forwards + defenses + goalies]

    def get_roster_player_infos_forward(self, team_id, season_id=None):
        season_id = NhlYearConverter.get_current_season() if season_id is None else season_id
        team_id_converted = NhlTeamConverter.get_abbreviation_by_teamId(team_id)

        json = HttpHelper.get(f'https://api-web.nhle.com/v1/roster/{team_id_converted}/{season_id}')

        forwards = json.get("forwards", [])

        return [self._to_model(player) for player in forwards]

    def get_roster_player_infos_defense(self, team_id, season_id=None):
        season_id = NhlYearConverter.get_current_season() if season_id is None else season_id
        team_id_converted = NhlTeamConverter.get_abbreviation_by_teamId(team_id)

        json = HttpHelper.get(f'https://api-web.nhle.com/v1/roster/{team_id_converted}/{season_id}')

        defenses = json.get("defensemen", [])

        return [self._to_model(player) for player in defenses]

    @staticmethod
    def _to_model(row) -> Optional[PlayerInfo]:
        data = {}
        for f in fields(PlayerInfo):
            value = row.get(f.name)
            if is_dataclass(f.type) and isinstance(value, dict):
                data[f.name] = f.type(**value)
            else:
                data[f.name] = value

        return PlayerInfo(**data)
