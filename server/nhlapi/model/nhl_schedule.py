from server.commons.helper.nhl_team_converter import NhlTeamConverter


class Schedule:

    def __init__(self, firstDay, lastDay, teams):
        self.firstDay = firstDay
        self.lastDay = lastDay
        self.teams = teams


class Team:

    def __init__(self, teamId, games):
        self.teamId = teamId
        self.team = NhlTeamConverter.get_abbreviation_by_teamId(teamId)
        self.games = games


class NhlGame:

    def __init__(self, gamePk, day, date, homeTeam, awayTeam):
        self.gamePk = gamePk
        self.day = day
        self.date = date
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam


class TeamGameInfo:

    def __init__(self, teamId, teamName, score):
        self.teamId = teamId
        self.abbreviation = NhlTeamConverter.get_abbreviation_by_teamId(teamId)
        self.teamName = teamName
        self.score = score
