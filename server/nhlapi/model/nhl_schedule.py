from dataclasses import dataclass, field
from server.commons.helper.nhl_team_converter import NhlTeamConverter


@dataclass
class Schedule:
    firstDay: str
    lastDay: str
    teams: list


@dataclass
class Team:
    teamId: int
    games: list
    team: str = field(default="", init=False)

    def __post_init__(self):
        self.team = NhlTeamConverter.get_abbreviation_by_teamId(self.teamId)


@dataclass
class NhlGame:
    gamePk: int
    day: int
    date: str
    homeTeam: 'TeamGameInfo'
    awayTeam: 'TeamGameInfo'


@dataclass
class TeamGameInfo:
    teamId: int
    teamName: str
    score: int
    abbreviation: str = field(default="", init=False)

    def __post_init__(self):
        self.abbreviation = NhlTeamConverter.get_abbreviation_by_teamId(self.teamId)
